"""Original procedural aquatic archetypes, generated in Blender. No external art."""
import bpy, math, os, json
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__));os.makedirs(OUT+'/renders',exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=32;scene.cycles.use_denoising=False
scene.render.resolution_x=192;scene.render.resolution_y=192;scene.render.resolution_percentage=100
scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA'
scene.world.color=(.18,.18,.18);scene.view_settings.view_transform='Standard'
def material(name,color):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);return m
leaf=material('Aquatic jade',(.13,.52,.30));tip=material('New collector tissue',(.35,.8,.48));base=material('Dense support',(.11,.36,.25))
forms={}
def sphere(p,scale,mat=leaf):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=8,ring_count=4,location=p);o=bpy.context.object;o.scale=scale;o.data.materials.append(mat);return o
def stem(a,b,r=.025):
 d=Vector(b)-Vector(a);bpy.ops.mesh.primitive_cone_add(vertices=6,radius1=r,radius2=r*.65,depth=d.length,location=(Vector(a)+Vector(b))/2);o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();o.data.materials.append(base);return o
def blade(angle,length,width,raisez,twist=0):
 vertices=[]
 for i in range(5):
  t=i/4;r=length*t;z=raisez*math.sin(t*math.pi*.65);w=width*math.sin(math.pi*t)**.6
  for side in [-1,1]:
   off=side*w/2;vertices.append((math.cos(angle)*r-math.sin(angle)*off,math.sin(angle)*r+math.cos(angle)*off,z+twist*side*math.sin(t*math.pi)))
 faces=[]
 for i in range(4):faces.extend([(2*i,2*i+1,2*i+2),(2*i+1,2*i+3,2*i+2)])
 me=bpy.data.meshes.new('Collector ribbon');me.from_pydata(vertices,[],faces);me.update();o=bpy.data.objects.new('Collector',me);bpy.context.collection.objects.link(o);o.data.materials.append(leaf)
 sol=o.modifiers.new('Thin tissue','SOLIDIFY');sol.thickness=.012
 return o
for name in ['mat','cushion','rosette','ribbon','branching','canopy']:
 before=set(bpy.data.objects)
 if name=='mat':
  for x,y,z,s in [(-.14,0,.035,.22),(.13,.08,.045,.19),(0,-.1,.025,.18)]:sphere((x,y,z),(s,s*.7,.05),leaf)
 elif name=='cushion':
  for a in range(6):sphere((.14*math.cos(a*math.tau/6),.14*math.sin(a*math.tau/6),.11),(.13,.13,.14),leaf)
  sphere((0,0,.19),(.16,.16,.16),tip)
 elif name=='rosette':
  for a in range(7):blade(a*math.tau/7,.35,.14,.13)
  sphere((0,0,.06),(.07,.07,.07),tip)
 elif name=='ribbon':
  for a in range(4):blade(a*math.tau/4,.28,.12,.47,.035)
 elif name=='branching':
  for a in range(5):
   ang=a*math.tau/5;end=(.18*math.cos(ang),.18*math.sin(ang),.25);stem((0,0,0),end,.035)
   for delta in [-.65,.65]:
    p=(end[0]+.1*math.cos(ang+delta),end[1]+.1*math.sin(ang+delta),.37);stem(end,p,.025);sphere(p,(.035,.035,.065),tip)
 elif name=='canopy':
  stem((0,0,0),(0,0,.43),.04)
  for a in range(6):
   ang=a*math.tau/6;end=(.19*math.cos(ang),.19*math.sin(ang),.30+.13*(a%2));stem((0,0,.18),end,.025);sphere(end,(.125,.10,.045),tip)
 objects=list(set(bpy.data.objects)-before)
 for o in objects:o.name=name+'_'+o.name
 forms[name]=objects
# fixed camera/light used for every archetype
bpy.ops.object.camera_add(location=(1.1,-1.6,1.45));camera=bpy.context.object;camera.rotation_euler=(Vector((0,0,.16))-camera.location).to_track_quat('-Z','Y').to_euler();camera.data.type='ORTHO';camera.data.ortho_scale=1.02;scene.camera=camera
for loc,power,size in [((-.8,-1,2),110,1.4),((1,1,1.2),50,1)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,.2))-o.location).to_track_quat('-Z','Y').to_euler()
report={}
for name,objects in forms.items():
 for nm,objs in forms.items():
  for o in objs:o.hide_render=nm!=name
 scene.render.filepath=OUT+'/renders/'+name+'.png';bpy.ops.render.render(write_still=True)
 deps=bpy.context.evaluated_depsgraph_get();tris=0
 for o in objects:
  mesh=o.evaluated_get(deps).to_mesh();mesh.calc_loop_triangles();tris+=len(mesh.loop_triangles);o.evaluated_get(deps).to_mesh_clear()
 report[name]={'render_triangles':tris}
for objects in forms.values():
 for o in objects:o.hide_render=False
bpy.ops.wm.save_as_mainfile(filepath=OUT+'/aquatic-forms.blend')
with open(OUT+'/geometry-report.json','w') as f:json.dump(report,f,indent=2)
