"""Real surfaceless Mesa GLES3 validation of the game's attachment routing."""
import ctypes as C
E=C.CDLL('libEGL.so.1'); G=None
def f(lib,name,rest,args):
 if lib is None: return C.CFUNCTYPE(rest,*args)(get(name.encode()))
 p=getattr(lib,name);p.restype=rest;p.argtypes=args;return p
ptr=C.c_void_p; I=C.c_int; U=C.c_uint
get=f(E,'eglGetProcAddress',ptr,[C.c_char_p]); platform=C.CFUNCTYPE(ptr,U,ptr,C.POINTER(I))(get(b'eglGetPlatformDisplayEXT'))
d=platform(0x31DD,None,None); major=I();minor=I();assert f(E,'eglInitialize',U,[ptr,C.POINTER(I),C.POINTER(I)])(d,C.byref(major),C.byref(minor))
assert f(E,'eglBindAPI',U,[U])(0x30A0)
a=(I*7)(0x3040,0x0040,0x3033,1,0x3024,8,0x3038);cfg=ptr();n=I()
assert f(E,'eglChooseConfig',U,[ptr,C.POINTER(I),C.POINTER(ptr),I,C.POINTER(I)])(d,a,C.byref(cfg),1,C.byref(n)) and n.value
ca=(I*3)(0x3098,3,0x3038);ctx=f(E,'eglCreateContext',ptr,[ptr,ptr,ptr,C.POINTER(I)])(d,cfg,None,ca)
assert ctx and f(E,'eglMakeCurrent',U,[ptr,ptr,ptr,ptr])(d,None,None,ctx)
print('GL_VERSION:',f(G,'glGetString',C.c_char_p,[U])(0x1F02).decode())
fb=U();f(G,'glGenFramebuffers',None,[I,C.POINTER(U)])(1,C.byref(fb));f(G,'glBindFramebuffer',None,[U,U])(0x8D40,fb)
draw=f(G,'glDrawBuffers',None,[I,C.POINTER(U)]);error=f(G,'glGetError',U,[])
draw(1,(U*1)(0x8CE1));bad=error();print('drawBuffers([COLOR_ATTACHMENT1]) =',hex(bad));assert bad==0x502
draw(1,(U*1)(0x8CE0));good=error();print('drawBuffers([COLOR_ATTACHMENT0]) =',hex(good));assert good==0
print('Confirmed legacy attachment1 mapping invalid; production attachment0 mapping passes actual GLES3.')
