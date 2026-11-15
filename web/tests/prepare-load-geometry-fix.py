"""Apply the narrow CPU-only geometry repair to an isolated copied src tree."""
from pathlib import Path
import sys
root=Path(sys.argv[1]);p=root/'simulation/planet.zig';s=p.read_text()
legacy='''                const totalElevation = self.elevation[i];
                const exaggeratedElev = (totalElevation - self.radius) * HEIGHT_EXAGGERATION_FACTOR + self.radius;
                const scaledPoint = point.scale(exaggeratedElev);
                const transformedPoint = mulByVec3(rotationMatrix, scaledPoint);'''
if 'pub fn refreshTransformedPoints' in s:
 assert 'const transformedPoint = self.terrainPoint(point, i, rotationMatrix);' in s
 assert 'p.refreshTransformedPoints(state.axialTilt);' in (root/'save_game.zig').read_text()
 raise SystemExit(0)
assert s.count(legacy)==1
helper='''    /// Deterministic terrain geometry shared by rendering and save restoration.
    /// No GL calls, jobs, allocation, saved resource mutation or frame advancement.
    inline fn terrainPoint(self: *const Planet, point: Vec3, index: usize, rotationMatrix: za.Mat4) Vec3 {
        @setFloatMode(.optimized);
        const totalElevation = self.elevation[index];
        const exaggeratedElev = (totalElevation - self.radius) * HEIGHT_EXAGGERATION_FACTOR + self.radius;
        const scaledPoint = point.scale(exaggeratedElev);
        return mulByVec3(rotationMatrix, scaledPoint);
    }

    pub fn refreshTransformedPoints(self: *Planet, axialTilt: f32) void {
        @setFloatMode(.optimized);
        const rotationMatrix = za.Mat4.fromRotation(axialTilt, Vec3.right());
        for (self.vertices, 0..) |point, i| self.transformedPoints[i] = self.terrainPoint(point, i, rotationMatrix);
    }

'''
s=s.replace('    /// Upload all changes to the GPU\n',helper+'    /// Upload all changes to the GPU\n',1)
s=s.replace(legacy,'                const transformedPoint = self.terrainPoint(point, i, rotationMatrix);')
p.write_text(s)
p=root/'save_game.zig';s=p.read_text();needle='    state.axialTilt = saved.axial_tilt;';assert s.count(needle)==1;s=s.replace(needle,needle+'\n    // Physics can run before the next render; never retain the prior world\'s geometry.\n    p.refreshTransformedPoints(state.axialTilt);');p.write_text(s)
