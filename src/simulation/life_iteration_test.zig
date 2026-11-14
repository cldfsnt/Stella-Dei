const std = @import("std");
// Regression model for the population mutation contract used in Planet.simulate.
test "reverse original population tolerates deaths and births without revisiting newborns" {
    var population = std.ArrayList(u8).init(std.testing.allocator);
    defer population.deinit();
    try population.appendSlice(&.{ 0, 1, 2, 3 });
    const original = population.items.len;
    try population.ensureTotalCapacity(original * 2);
    var visited = [_]u8{0} ** 4;
    var remaining = original;
    while (remaining > 0) {
        remaining -= 1;
        const id = population.items[remaining];
        visited[id] += 1;
        if (id % 2 == 0) {
            _ = population.orderedRemove(remaining);
        } else {
            population.appendAssumeCapacity(id + 10);
        }
    }
    try std.testing.expectEqualSlices(u8, &.{ 1, 1, 1, 1 }, &visited);
    try std.testing.expectEqualSlices(u8, &.{ 1, 3, 13, 11 }, population.items);
}
