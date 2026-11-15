from pathlib import Path
import shutil,sys,re
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);assert not dst.exists();shutil.copytree(src,dst)
p=dst/'simulation/planet.zig';s=p.read_text();needle='    pub fn refreshTransformedPoints(self: *Planet, axialTilt: f32) void {';assert s.count(needle)==1
s=s.replace(needle,'''    /// Tool-local geometry update before any same-frame physics or navigation.
    /// No world scan, allocation, job, or work for a clamped/no-change edit.
    pub fn setTerrainElevation(self:*Planet,index:usize,value:f32,axialTilt:f32) void {
        if(self.elevation[index]==value)return;
        self.elevation[index]=value;
        self.refreshTerrainPoint(index,axialTilt);
    }
    fn refreshTerrainPoint(self:*Planet,index:usize,axialTilt:f32) void {
        @setFloatMode(.optimized);
        const rotationMatrix=za.Mat4.fromRotation(axialTilt,Vec3.right());
        self.transformedPoints[index]=self.terrainPoint(self.vertices[index],index,rotationMatrix);
    }

'''+needle);p.write_text(s)
p=dst/'states/play.zig';s=p.read_text();a=s.index('        if (tool == .RaiseTerrain) {');z=s.index('        self.mobileFeedback = switch (tool)',a);part=s[a:z]
part,n=re.subn(r'planet.elevation\[(self.selectedPoint|idx)\] = ([^;]+);',r'planet.setTerrainElevation(\1, \2, self.axialTilt);',part);assert n==4;s=s[:a]+part+s[z:];p.write_text(s)
print(dst)
