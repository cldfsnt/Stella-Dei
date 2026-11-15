from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[2];out=Path(sys.argv[1]);subprocess.run([sys.executable,str(root/'web/tests/egl-load-geometry-prepare.py'),str(out)],check=True)
subprocess.run([sys.executable,str(root/'web/tests/prepare-load-geometry-fix.py'),str(out)],check=True)
p=out/'simulation/planet.zig';s=p.read_text();needle='    /// Upload all changes to the GPU\n';assert s.count(needle)==1
s=s.replace(needle,'''    // QA-only frozen pre-fix upload geometry oracle, no production method.
    pub fn qaLegacyGeometry(self: *Planet, axialTilt: f32) void {
        @setFloatMode(.optimized); @setRuntimeSafety(false);
        const rotationMatrix = za.Mat4.fromRotation(axialTilt, Vec3.right());
        for (self.vertices, 0..) |point, i| {
            const totalElevation = self.elevation[i];
            const exaggeratedElev = (totalElevation - self.radius) * HEIGHT_EXAGGERATION_FACTOR + self.radius;
            const scaledPoint = point.scale(exaggeratedElev);
            const transformedPoint = mulByVec3(rotationMatrix, scaledPoint);
            self.transformedPoints[i] = transformedPoint;
        }
    }
''' +needle);p.write_text(s)
p=out/'main.zig';s=p.read_text();needle='          var results:[2][]const u8=undefined;';assert s.count(needle)==1
s=s.replace(needle,r'''
          for([_]f32{-45,0,23.5,90})|tilt|{
            try saves.apply(state,target.value);state.axialTilt=tilt;state.selectedPoint=12352;state.pointerOnPlanet=true;std.debug.assert(state.testAction(5));
            state.planet.qaLegacyGeometry(tilt);
            const expected=try a.dupe(@TypeOf(state.planet.transformedPoints[0]),state.planet.transformedPoints);
            state.planet.refreshTransformedPoints(tilt);
            for(expected,state.planet.transformedPoints)|x,y|{for(0..3)|axis|std.debug.assert(@as(u32,@bitCast(x.data[axis]))==@as(u32,@bitCast(y.data[axis])));}
            state.planet.upload(game.loop,state.displayMode,tilt);game.loop.pump(1024);
            for(expected,state.planet.transformedPoints)|x,y|{for(0..3)|axis|std.debug.assert(@as(u32,@bitCast(x.data[axis]))==@as(u32,@bitCast(y.data[axis])));}
          }
          std.debug.print("LOAD_GEOMETRY_BITS 4tilts_all_vertices_three_components_exact=true\n",.{});
''' +needle)
needle='          std.debug.print("LOAD_GEOMETRY_RESTORED true\\n",.{});'
assert s.count(needle)==1
s=s.replace(needle,needle+r'''
          // Same-geometry full uninterrupted vs restored continuation, no normalization.
          var continuation:[2][]const u8=undefined;
          for(0..2)|arm|{
            if(arm==1)try saves.apply(state,target.value);
            for(0..10)|_|{state.planet.simulate(game.loop,.{.dt=1440,.timeScale=1,.solarConstant=state.solarConstant,.gameTime=state.gameTime,.planetRotationTime=state.planetRotationTime,.solarVector=state.simulationSolarVector()});state.gameTime+=1440;}
            continuation[arm]=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          }
          std.debug.assert(std.mem.eql(u8,continuation[0],continuation[1]));
          try saves.apply(state,target.value);
          const before=try std.json.stringifyAlloc(a,try saves.capture(a,state),.{});
          const geometry=try a.dupe(@TypeOf(state.planet.transformedPoints[0]),state.planet.transformedPoints);
          var invalid=target.value;invalid.radius=-1;
          if(saves.apply(state,invalid)) |_| return error.InvalidSaveAccepted else |_| {}
          std.debug.assert(std.mem.eql(u8,before,try std.json.stringifyAlloc(a,try saves.capture(a,state),.{})));
          for(geometry,state.planet.transformedPoints)|x,y|for(0..3)|axis|std.debug.assert(@as(u32,@bitCast(x.data[axis]))==@as(u32,@bitCast(y.data[axis])));
          std.debug.print("LOAD_GEOMETRY_FIX_PASS crossgeometry_fullstate_exact={} samegeometry10ticks_exact=true invalid_save_and_geometry_unchanged=true\n",.{std.mem.eql(u8,results[0],results[1])});
          std.debug.assert(std.mem.eql(u8,results[0],results[1]));
''');p.write_text(s)
