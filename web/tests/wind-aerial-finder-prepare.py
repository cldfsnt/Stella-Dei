from pathlib import Path
import sys
r=Path(sys.argv[1]);src=r/'src';g=(src/'growth_form_finder.zig').read_text();g=g[:g.index('test "')]
a=g.index('pub fn matches(');b=g.index('\npub fn find',a)
g=g[:a]+'''pub fn matches(c:M.Cohort)bool{return c.parent!=0 and c.generation>0 and std.math.isFinite(c.aerial_allocation) and c.aerial_allocation>0 and c.aerial_allocation<=1 and @import("growth_form_finder.zig").matches(c,M.producerForm(c));}
'''+g[b:];g=g.replace(',form:M.ProducerForm)error',')error').replace('matches(c,form)','matches(c)');g=g.replace('//! Explicit read-only current morphology search. No cached census or taxonomy.','//! Explicit living aerial-descendant search. Ancestry/trait, never inferred birth route.')
g+='''test "actual ancestry positive trait minority and dead invalid guards" {
 const Point=struct{data:[3]f32};var cells=[_]M.Cell{.{}};const points=[_]Point{.{.data=.{5000,0,0}}};
 cells[0].cohorts[0]=.{.lineage=1,.biomass=0.5,.aerial_allocation=0.5};cells[0].cohorts[1]=.{.lineage=9007199254740993,.parent=1,.generation=1,.biomass=0.004,.aerial_allocation=0.00001};
 const before=cells;const found=(try find(&cells,&points,.{1,0,0})).?;try std.testing.expectEqual(@as(u64,9007199254740993),found.lineage);try std.testing.expectEqualDeep(before,cells);
 cells[0].cohorts[1].aerial_allocation=0;try std.testing.expect((try find(&cells,&points,.{1,0,0}))==null);
 cells=before;cells[0].cohorts[1].biomass=0;try std.testing.expect((try find(&cells,&points,.{1,0,0}))==null);
 cells=before;cells[0].cohorts[1].aerial_allocation=std.math.nan(f32);try std.testing.expect((try find(&cells,&points,.{1,0,0}))==null);
 cells=before;const polar=[_]Point{.{.data=.{0,0,5000}}};try std.testing.expectError(error.UnsafeView,find(&cells,&polar,.{1,0,0}));
}
''';(src/'aerial_descendant_finder.zig').write_text(g)
p=src/'states/play.zig';s=p.read_text();a=s.index('    pub fn visitGrowthForm(');b=s.index('\n    pub fn findLivingClusterResult',a);method=s[a:b]
method=method.replace('visitGrowthForm(self:*PlayState,world:u32,form:u32,width:f32,height:f32)','findAerialDescendant(self:*PlayState,world:u32,width:f32,height:f32)').replace('if(self.planet.worldMode!=.origin)return -1;','if(self.planet.worldMode!=.origin or !self.planet.windDispersal.enabled)return -1;').replace('        if(form>=6)return -3;\n','').replace('return -4','return -3').replace('../growth_form_finder.zig','../aerial_descendant_finder.zig').replace('self.targetCameraPos.data,@enumFromInt(form)','self.targetCameraPos.data')
method=method.replace('        const point=self.planet.transformedPoints[found.cell];','        var form:Microbes.ProducerForm=.mat;var valid=false;for(self.planet.microbeCells[found.cell].cohorts)|c|{if(c.lineage==found.lineage and F.matches(c)){form=Microbes.producerForm(c);valid=true;break;}}if(!valid)return 0;\n        const point=self.planet.transformedPoints[found.cell];').replace('self.colonyPeek.focused_form=@enumFromInt(form)','self.colonyPeek.focused_form=form').replace('Living growth form found; Details shows this patch\'s colonies','Living aerial descendant found; birth route is not recorded')
s=s[:b]+'\n'+method+s[b:]
a=s.index('                    if (c.biomass > 0) mobileDetailLabel(vg, game, "Structure:');b=s.index('\n                } else {',a);old=s[a:b];new='''                    if(visited!=null and c.generation>0 and c.aerial_allocation>0){
                        if(c.aerial_allocation*100<0.001) mobileDetailLabel(vg,game,"Aerial allocation: <0.001%",.{},px+16,py+232,pw-32) else mobileDetailLabel(vg,game,"Aerial allocation: {d:.3}%",.{c.aerial_allocation*100},px+16,py+232,pw-32);
                        mobileDetailLabel(vg,game,"Birth route unknown · inherited trait",.{},px+16,py+258,pw-32);
                    }else{
'''+old+'\n                    }';s=s[:a]+new+s[b:];p.write_text(s)
p=src/'main.zig';s=p.read_text();s+='''
export fn stella_find_aerial_descendant(world:u32)i32 {
 const state=webPlayState() orelse return -1;if(AdvanceDay.blocksInput())return -2;
 const size=game.window.getFramebufferSize();return state.findAerialDescendant(world,@floatFromInt(size.width),@floatFromInt(size.height));
}
''';p.write_text(s)
p=src/'wind_view.zig';s=p.read_text().replace('var count:usize=0;','var count:usize=0;var focus_buffer:[24]u8=undefined;var focused_lineage:?[]const u8=null;')
s=s.replace('   writer=writerVersion(v);','   if(@hasField(@TypeOf(v.*),"colonyPeek")){if(v.selectedPoint<v.planet.microbeCells.len){var pin=v.colonyPeek;if(pin.focusedCohort(v.selectedPoint,v.planet.microbeCells[v.selectedPoint]))|c|focused_lineage=std.fmt.bufPrint(&focus_buffer,"{d}",.{c.lineage}) catch null;}}\n   writer=writerVersion(v);')
s=s.replace('.cell=cell,.aerial_allocations=', '.cell=cell,.focused_lineage=focused_lineage,.aerial_allocations=');p.write_text(s)
p=r/'web/build.sh';s=p.read_text().replace('_stella_wind_snapshot,','_stella_find_aerial_descendant,_stella_wind_snapshot,');p.write_text(s)
