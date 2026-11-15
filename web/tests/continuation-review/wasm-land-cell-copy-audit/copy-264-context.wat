)
(local.set $149
(call $fmax
(f64.load offset=2512
(local.get $4)
)
(f64.const 0)
)
)
(local.set $147
(call $fmax
(f64.load offset=2504
(local.get $4)
)
(f64.const 0)
)
)
(br_if $label$667
(i32.ge_u
(local.get $8)
(i32.load offset=2552
(local.get $4)
)
)
)
(br_if $label$666
(i32.ge_u
(local.get $8)
(i32.load offset=2612
(local.get $4)
)
)
)
(if
(i32.gt_u
(i32.load offset=2712
(local.get $4)
)
(local.get $8)
)
(then
(local.set $105
(f32.load
(i32.add
(i32.load offset=2608
(local.get $4)
)
(local.get $2)
)
)
)
(local.set $146
(f64.load
(i32.add
(i32.load offset=2548
(local.get $4)
)
(local.get $14)
)
)
)
(drop
(call $__memcpy
(i32.add
(local.get $11)
(i32.const 264)
)
(i32.add
(i32.load offset=2708
(local.get $4)
)
(local.get $7)
)
(i32.const 368)
)
)
(i64.store
(local.get $18)
(i64.const 0)
)
(i64.store offset=248
(local.get $11)
(i64.const 0)
)
(br_if $label$663
(i64.gt_u
(i64.reinterpret_f64
(f64.promote_f32
(f32.abs
(local.get $113)
)
)
)
(i64.const 9218868437227405311)
)
)
(br_if $label$663
(i32.eqz
(f32.ge
(local.get $113)
(f32.const 0)
)
)
)
(br_if $label$663
(i64.gt_u
(i64.and
(i64.reinterpret_f64
(local.get $145)
)
(i64.const 9223372036854775807)
)
(i64.const 9218868437227405311)
)
)
(br_if $label$663
(i32.eqz
(f64.ge
(local.get $145)

