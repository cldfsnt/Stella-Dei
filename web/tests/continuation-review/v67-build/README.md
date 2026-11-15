# v67 combined candidate build

Frozen production83a875cc499195f40cc894df157a5db38e21795e combines exact nearest-point sqrt pruning (bc2b4ee) and explicit Sandbox survivor finders (83a875c). Full92 JS tests pass; final production WASM build exit0. All recorded Zig and shell/controller source hashes unchanged during build. Raw dist hashes retained; coordinator release-label packaging creates its own later manifest. No publication/deployment claim.

Nearest helper native/target-WASM exactness and measured actual native scheduler evidence remain in ../nearest-sqrt-prune. This build does not establish browser/device FPS. Native final combined finder acceptance is a separate required release gate, owned by grazing_traits; this report does not substitute for or presume its outcome.
