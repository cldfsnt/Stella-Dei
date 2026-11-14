import ctypes as C
from pathlib import Path
E=C.CDLL('libEGL.so.1');G=C.CDLL('libGL.so.1');I=C.c_int;P=C.c_void_p
E.eglGetProcAddress.restype=P
platform=C.CFUNCTYPE(P,C.c_uint,P,C.POINTER(I))(E.eglGetProcAddress(b'eglGetPlatformDisplayEXT'))
d=platform(0x31DD,None,None)
E.eglInitialize.argtypes=[P,C.POINTER(I),C.POINTER(I)];a=I();b=I();assert E.eglInitialize(d,C.byref(a),C.byref(b))
E.eglBindAPI(0x30A0)
E.eglChooseConfig.argtypes=[P,C.POINTER(I),C.POINTER(P),I,C.POINTER(I)]
attrs=(I*7)(0x3033,1,0x3040,0x40,0x3024,8,0x3038);cfg=P();n=I();assert E.eglChooseConfig(d,attrs,C.byref(cfg),1,C.byref(n)) and n.value
E.eglCreatePbufferSurface.argtypes=[P,P,C.POINTER(I)];E.eglCreatePbufferSurface.restype=P
s=E.eglCreatePbufferSurface(d,cfg,(I*5)(0x3057,16,0x3056,16,0x3038))
E.eglCreateContext.argtypes=[P,P,P,C.POINTER(I)];E.eglCreateContext.restype=P
ctx=E.eglCreateContext(d,cfg,None,(I*3)(0x3098,3,0x3038));assert ctx
E.eglMakeCurrent.argtypes=[P,P,P,P];assert E.eglMakeCurrent(d,s,s,ctx)
G.glCreateShader.restype=C.c_uint;G.glShaderSource.argtypes=[C.c_uint,I,C.POINTER(C.c_char_p),C.POINTER(I)]
G.glCreateProgram.restype=C.c_uint;prog=G.glCreateProgram()
for name,kind in [('terrain.vs',0x8B31),('terrain.fs',0x8B30)]:
 src=(Path(__import__('sys').argv[1])/name).read_text().replace('#version 330 core','#version 300 es\nprecision highp float;\nprecision highp int;').encode();sh=G.glCreateShader(kind);ptr=C.c_char_p(src);G.glShaderSource(sh,1,C.byref(ptr),None);G.glCompileShader(sh);ok=I();G.glGetShaderiv(sh,0x8B81,C.byref(ok));log=C.create_string_buffer(8192);G.glGetShaderInfoLog(sh,8192,None,log);print(name,'compile',ok.value,log.value.decode());assert ok.value;G.glAttachShader(prog,sh)
G.glLinkProgram(prog);ok=I();G.glGetProgramiv(prog,0x8B82,C.byref(ok));log=C.create_string_buffer(8192);G.glGetProgramInfoLog(prog,8192,None,log);print('ES300 link',ok.value,log.value.decode());assert ok.value
