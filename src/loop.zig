const std = @import("std");
const is_web = @import("builtin").target.cpu.arch == .wasm32;
const TaskStack = std.DoublyLinkedList(Task);
const Thread = std.Thread;
const Allocator = std.mem.Allocator;
const tracy = @import("vendor/tracy.zig");

const Task = struct {
    fnPtr: *const fn (userdata: ?*anyopaque) void,
    userdata: ?*anyopaque,
};

pub fn Job(comptime ResultType: type) type {
    return struct {
        loop: *EventLoop,
        result: ResultType,
        completed: std.atomic.Value(bool),
        /// If the call() function was used, this contains the async frame
        //asyncBuffer: ?[]u8 = null,
        toNotify: ?*Self = null,
        node: TaskStack.Node = undefined,
        has_node: bool = false,

        const Self = @This();

        pub fn create(loop: *EventLoop) !*Self {
            const jobPtr = try loop.allocator.create(Self);
            jobPtr.* = .{ .loop = loop, .result = undefined, .completed = std.atomic.Value(bool).init(false) };
            return jobPtr;
        }

        pub fn completed(loop: *EventLoop, result: ResultType) !*Self {
            const jobPtr = try loop.allocator.create(Self);
            jobPtr.* = .{ .loop = loop, .result = result, .completed = std.atomic.Value(bool).init(true) };
            return jobPtr;
        }

        pub fn call(self: *Self, comptime func: anytype, args: anytype) !void {
            if (self.has_node) {
                @panic("Cannot use Job.call() more than once!");
            }
            const Fn = switch (@typeInfo(@TypeOf(func))) {
                .Fn => |info| info,
                else => @compileError("Type " ++ @typeName(@TypeOf(func)) ++ " is not a function"),
            };
            const ReturnType = Fn.return_type.?;
            if (ReturnType == ResultType) {
                const ArgsType = @TypeOf(args);
                const WrapperArgsType = struct { job: *Self, funcArgs: ArgsType, allocator: std.mem.Allocator };
                const wrapper = struct {
                    pub fn wrapper(userdata: ?*anyopaque) callconv(.Unspecified) void {
                        const wrapperArgs = @as(*WrapperArgsType, @ptrCast(@alignCast(userdata)));
                        const job = wrapperArgs.job;
                        const funcArgs = wrapperArgs.funcArgs;
                        const result = @call(.auto, func, funcArgs);
                        job.notify(result);

                        const allocator = wrapperArgs.allocator;
                        allocator.destroy(wrapperArgs);
                    }
                }.wrapper;
                //const buffer = try self.loop.allocator.alignedAlloc(u8, @alignOf(@Frame(wrapper)), @frameSize(wrapper));
                //self.asyncBuffer = buffer;
                //_ = @asyncCall(buffer, undefined, wrapper, .{ self, args });
                const args_ptr = try self.loop.allocator.create(WrapperArgsType);
                args_ptr.* = .{ .job = self, .funcArgs = args, .allocator = self.loop.allocator };
                self.node = .{
                    .data = .{ .fnPtr = wrapper, .userdata = args_ptr },
                    .next = null,
                };
                self.has_node = true;

                self.loop.taskStackMutex.lock();
                defer self.loop.taskStackMutex.unlock();
                self.loop.taskStack.append(&self.node);
            } else {
                @compileError("The function's return type doesn't match the job's result type");
            }
        }

        /// Get result
        pub fn get(self: *const Self) ResultType {
            while (self.completed.load(.acquire) == false) {
                if (is_web) {
                    // Browser jobs run on the UI thread. A nested wait must run
                    // pending work, never block waiting for an absent worker.
                    if (!self.loop.runOne()) @panic("Waiting for a browser job with no queued work");
                } else {
                    std.time.sleep(1000);
                }
            }
            return self.result;
        }

        pub fn peek(self: *const Self) ?ResultType {
            if (self.completed.load(.acquire) == true) {
                return self.result;
            } else {
                return null;
            }
        }

        pub fn isCompleted(self: *const Self) bool {
            return self.completed.load(.acquire);
        }

        pub fn then(self: *Self, next: *Self) void {
            if (self.toNotify != null) {
                @panic("Trying to set a job to notify twice"); // TODO: support multiple notified jobs
            } else {
                self.toNotify = next;
            }
        }

        /// Get result and deinit the job.
        pub fn wait(self: *Self) ResultType {
            const result = self.get();
            self.deinit();

            return result;
        }

        pub fn notify(self: *Self, value: ResultType) void {
            self.result = value;
            defer self.completed.store(true, .release);

            if (self.toNotify) |job| {
                job.notify(value);
            }
        }

        pub fn deinit(self: *Self) void {
            self.loop.allocator.destroy(self);
        }
    };
}

// TODO: launch new threads if none available
pub const EventLoop = struct {
    allocator: Allocator,
    taskStack: TaskStack,
    taskStackMutex: std.Thread.Mutex = .{},
    //numTasks: std.atomic.Value(u32) = std.atomic.Value(u32).init(0),
    /// The number of 'events', when it hits 0 the run loop is stopped
    events: usize = 0,
    threads: []Thread,

    pub fn init() EventLoop {
        return EventLoop{
            .allocator = undefined,
            .taskStack = TaskStack{},
            .threads = undefined,
        };
    }

    /// This function assumes that the EventLoop pointer will stay
    /// valid during the entire loop's lifetime
    pub fn start(self: *EventLoop, allocator: Allocator) !void {
        self.allocator = allocator;
        if (is_web) {
            self.threads = &.{};
            return;
        }
        const cpuCount = std.math.floorPowerOfTwo(usize, try Thread.getCpuCount());
        const threads = try allocator.alloc(Thread, cpuCount);
        self.threads = threads;
        self.allocator = allocator;

        for (threads, 0..) |*thread, threadId| {
            thread.* = try Thread.spawn(.{}, workerLoop, .{ self, threadId });
        }
    }

    /// Execute one queued job. Pop before calling: jobs may enqueue/wait on
    /// other jobs recursively and their own nodes may be destroyed afterward.
    pub fn runOne(self: *EventLoop) bool {
        self.taskStackMutex.lock();
        const node = self.taskStack.popFirst();
        self.taskStackMutex.unlock();
        if (node) |task| {
            const data = task.data;
            data.fnPtr(data.userdata);
            return true;
        }
        return false;
    }

    /// Bound ordinary frame work, so self-enqueuing jobs cannot starve input.
    /// A synchronous get()/wait() can still complete its dependency tree.
    pub fn pump(self: *EventLoop, max_jobs: usize) void {
        var count: usize = 0;
        while (count < max_jobs and self.runOne()) : (count += 1) {}
    }

    pub fn workerLoop(self: *EventLoop, threadId: usize) void {
        _ = threadId;
        var sleepTime: u64 = 8 * std.time.ns_per_ms;

        while (self.events > 0) {
            self.taskStackMutex.lock();
            if (self.taskStack.popFirst()) |node| {
                self.taskStackMutex.unlock();
                node.data.fnPtr(node.data.userdata);
                sleepTime /= 2;
            } else {
                self.taskStackMutex.unlock();
                // wait until a task is available
                if (sleepTime > 0) std.time.sleep(sleepTime);
                sleepTime += std.time.ns_per_ms / 10;
                sleepTime = @min(sleepTime, 50 * std.time.ns_per_ms);
            }
        }
    }

    pub fn beginEvent(self: *EventLoop) void {
        self.events += 1;
    }

    /// End an event. If the loop now has 0 events,
    /// it will be deinit.
    pub fn endEvent(self: *EventLoop) void {
        self.events -= 1;
        if (self.events == 0) {
            if (is_web) {
                self.pump(std.math.maxInt(usize));
                return;
            }
            for (self.threads) |thread| {
                thread.join();
            }
            self.allocator.free(self.threads);
            self.* = undefined;
        }
    }

    /// The number of frames a task should ideally divide itself into
    pub fn getParallelCount(self: *const EventLoop) usize {
        return if (is_web) 1 else self.threads.len;
    }
};

test "queued jobs execute cooperatively" {
    var loop = EventLoop.init();
    loop.allocator = std.testing.allocator;
    const job = try Job(u32).create(&loop);
    defer job.deinit();
    const add = struct {
        fn run(a: u32, b: u32) u32 {
            return a + b;
        }
    }.run;
    try job.call(add, .{ @as(u32, 20), @as(u32, 22) });
    try std.testing.expect(!job.isCompleted());
    try std.testing.expect(loop.runOne());
    try std.testing.expectEqual(@as(u32, 42), job.get());
    try std.testing.expect(!loop.runOne());
}
