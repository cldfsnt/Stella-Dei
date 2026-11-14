import ctypes as C, numpy as np,json
from pathlib import Path
D=Path(__file__).resolve().parent
E=C.CDLL('libEGL.so.1');P=C.c_void_p;I=C.c_int;U=C.c_uint
E.eglGetProcAddress.restype=P;E.eglGetProcAddress.argtypes=[C.c_char_p]
def egl(n,rest,args):
 f=getattr(E,n);f.restype=rest;f.argtypes=args;return f
platform=C.CFUNCTYPE(P,U,P,C.POINTER(I))(E.eglGetProcAddress(b'eglGetPlatformDisplayEXT'));d=platform(0x31DD,None,None);a=I();b=I();assert egl('eglInitialize',I,[P,C.POINTER(I),C.POINTER(I)])(d,C.byref(a),C.byref(b));egl('eglBindAPI',I,[U])(0x30A2)
attrs=(I*15)(0x3033,1,0x3040,8,0x3024,8,0x3023,8,0x3022,8,0x3021,8,0x3025,0,0x3038);cfg=P();n=I();assert egl('eglChooseConfig',I,[P,C.POINTER(I),C.POINTER(P),I,C.POINTER(I)])(d,attrs,C.byref(cfg),1,C.byref(n)) and n.value
surf=egl('eglCreatePbufferSurface',P,[P,P,C.POINTER(I)])(d,cfg,(I*5)(0x3057,1,0x3056,1,0x3038));ctx=egl('eglCreateContext',P,[P,P,P,C.POINTER(I)])(d,cfg,None,(I*7)(0x3098,3,0x30FB,3,0x30FD,1,0x3038));assert egl('eglMakeCurrent',I,[P,P,P,P])(d,surf,surf,ctx)
def gl(n,rest,args):return C.CFUNCTYPE(rest,*args)(E.eglGetProcAddress(('gl'+n).encode()))
getString=gl('GetString',C.c_char_p,[U]);print('RENDERER',getString(0x1F01).decode())
createShader=gl('CreateShader',U,[U]);shaderSource=gl('ShaderSource',None,[U,I,C.POINTER(C.c_char_p),C.POINTER(I)]);compileShader=gl('CompileShader',None,[U]);getShaderiv=gl('GetShaderiv',None,[U,U,C.POINTER(I)]);getShaderLog=gl('GetShaderInfoLog',None,[U,I,C.POINTER(I),P]);createProgram=gl('CreateProgram',U,[]);attach=gl('AttachShader',None,[U,U]);link=gl('LinkProgram',None,[U]);getProgram=gl('GetProgramiv',None,[U,U,C.POINTER(I)]);use=gl('UseProgram',None,[U]);loc=gl('GetUniformLocation',I,[U,C.c_char_p]);uniform=gl('Uniform1i',None,[I,I])
def shader(kind,source):
 sh=createShader(kind);x=C.c_char_p(source.encode());shaderSource(sh,1,C.byref(x),None);compileShader(sh);ok=I();getShaderiv(sh,0x8B81,C.byref(ok));buf=C.create_string_buffer(16384);getShaderLog(sh,len(buf),None,buf);assert ok.value,buf.value;return sh
vertex=shader(0x8B31,'#version 330 core\nout vec2 texCoords;void main(){vec2 p=vec2((gl_VertexID<<1)&2,gl_VertexID&2);texCoords=p;gl_Position=vec4(p*2.0-1.0,0,1);}')
def program(path):
 p=createProgram();attach(p,vertex);attach(p,shader(0x8B30,path.read_text()));link(p);ok=I();getProgram(p,0x8B82,C.byref(ok));assert ok.value;return p
programs=[program(D/'baseline.fs'),program(D/'candidate.fs')]
genTex=gl('GenTextures',None,[I,C.POINTER(U)]);bindTex=gl('BindTexture',None,[U,U]);texImage=gl('TexImage2D',None,[U,I,I,I,I,I,U,U,P]);texParam=gl('TexParameteri',None,[U,U,I]);active=gl('ActiveTexture',None,[U]);deleteTex=gl('DeleteTextures',None,[I,C.POINTER(U)]);genFbo=gl('GenFramebuffers',None,[I,C.POINTER(U)]);bindFbo=gl('BindFramebuffer',None,[U,U]);attachTex=gl('FramebufferTexture2D',None,[U,U,U,U,I]);status=gl('CheckFramebufferStatus',U,[U]);deleteFbo=gl('DeleteFramebuffers',None,[I,C.POINTER(U)]);viewport=gl('Viewport',None,[I,I,I,I]);draw=gl('DrawArrays',None,[U,I,I]);read=gl('ReadPixels',None,[I,I,I,I,U,U,P]);genVao=gl('GenVertexArrays',None,[I,C.POINTER(U)]);bindVao=gl('BindVertexArray',None,[U]);vao=U();genVao(1,C.byref(vao));bindVao(vao)
def texture(w,h,data=None,fmt=0x881A):
 t=U();genTex(1,C.byref(t));bindTex(0x0DE1,t);texImage(0x0DE1,0,fmt,w,h,0,0x1908,0x1406,None if data is None else data.ctypes.data);texParam(0x0DE1,0x2801,0x2601);texParam(0x0DE1,0x2800,0x2601);texParam(0x0DE1,0x2802,0x812F);texParam(0x0DE1,0x2803,0x812F);return t
fbo=U();genFbo(1,C.byref(fbo));bindFbo(0x8D40,fbo)
def target(t):attachTex(0x8D40,0x8CE0,0x0DE1,t,0);assert status(0x8D40)==0x8CD5

def run(p,src):
 h,w,_=src.shape;inp=texture(w,h,src);ta=texture(w,h);tb=texture(w,h);display=texture(w,h,fmt=0x8058);viewport(0,0,w,h);use(p)
 def ui(k,v):uniform(loc(p,k.encode()),v)
 ui('screenTexture',0);ui('bloomTexture',1);ui('doBrightTexture',0);ui('doBlurring',1);ui('enableAtmosphere',0);ui('enableBloom',1)
 stages=[];source=inp
 for step in range(4):
  dest=[ta,tb][step%2];target(dest);active(0x84C0);bindTex(0x0DE1,source);ui('horizontalBlurring',int(step%2==0));draw(4,0,3);out=np.empty_like(src);read(0,0,w,h,0x1908,0x1406,out.ctypes.data);stages.append(out[:,:,:3].copy());source=dest
 target(display);ui('doBlurring',0);active(0x84C0);bindTex(0x0DE1,inp);active(0x84C1);bindTex(0x0DE1,source);draw(4,0,3);pixels=np.empty((h,w,4),np.uint8);read(0,0,w,h,0x1908,0x1401,pixels.ctypes.data)
 for t in [inp,ta,tb,display]:deleteTex(1,C.byref(t))
 return stages,pixels

def cases(w,h):
 y,x=np.indices((h,w));
 for name,z in [('constant',np.ones((h,w))*10),('checker',(x+y)%2*10),('ramp',(x/w+y/h)*5),('edges',((x==0)|(y==0)|(x==w-1)|(y==h-1))*10),('impulse',((x==w//2)&(y==h//2))*10),('subpixel',np.maximum(0,1-np.abs(x-w*.413-.3))*np.maximum(0,1-np.abs(y-h*.377-.6))*10)]:
  rgba=np.ones((h,w,4),np.float32);rgba[:,:,:3]=np.asarray(z,np.float32)[:,:,None];yield name,rgba
records=[]
for w,h in [(1,1),(2,3),(7,9),(31,33),(390,700),(920,700)]:
 for name,src in cases(w,h):
  a,ap=run(programs[0],src);b,bp=run(programs[1],src);errs=[]
  for aa,bb in zip(a,b):
   diff=np.abs(aa-bb);errs.append({'max':float(diff.max()),'rms':float(np.sqrt(np.mean(diff.astype('float64')**2)))})
  diff=np.abs(ap.astype('int16')-bp.astype('int16'));r={'size':[w,h],'case':name,'stages':errs,'display_max':int(diff.max()),'display_changed_components':int(np.count_nonzero(diff))};records.append(r);print(json.dumps(r),flush=True)
(D.parent/'results/synthetic.json').write_text(json.dumps(records,indent=2))
