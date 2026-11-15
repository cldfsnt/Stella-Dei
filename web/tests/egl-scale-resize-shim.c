#include <string.h>
// Test-only offscreen GLFW shim. Actual game engine + shaders, EGL pbuffer output.
#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>
typedef void* EP; typedef int EI;
static EP d,s,c,lib;static int width=1280,height=720,closed,frames;static double mx,my;static int mouseState;static int rightState;
static GLFWcursorposfun cursorcb;static GLFWmousebuttonfun mousecb;static GLFWkeyfun keycb;static GLFWscrollfun scrollcb;
static void* proc(const char*n){void*(*gp)(const char*)=dlsym(lib,"eglGetProcAddress");return gp(n);}
int glfwInit(void){lib=dlopen("libEGL.so.1",RTLD_NOW);if(!lib)return 0;EP(*platform)(unsigned,EP,const EI*)=proc("eglGetPlatformDisplayEXT");d=platform(0x31DD,NULL,NULL);EI a,b;EI(*init)(EP,EI*,EI*)=dlsym(lib,"eglInitialize");if(!init(d,&a,&b))return 0; EI(*bind)(unsigned)=dlsym(lib,"eglBindAPI");bind(0x30A2);return 1;}
void glfwInitHint(int a,int b){} void glfwDefaultWindowHints(void){} void glfwWindowHint(int a,int b){}
GLFWwindow* glfwCreateWindow(int w,int h,const char*t,GLFWmonitor*m,GLFWwindow*share){w=atoi(getenv("STELLA_ORIGIN_WIDTH")?getenv("STELLA_ORIGIN_WIDTH"):"390");h=atoi(getenv("STELLA_ORIGIN_HEIGHT")?getenv("STELLA_ORIGIN_HEIGHT"):"700");width=w;height=h;EI attrs[]={0x3033,1,0x3040,8,0x3024,8,0x3023,8,0x3022,8,0x3021,8,0x3025,24,0x3026,8,0x3038};EP config;EI count;EI(*choose)(EP,const EI*,EP*,EI,EI*)=dlsym(lib,"eglChooseConfig");if(!choose(d,attrs,&config,1,&count)||!count)return NULL;EI surf[]={0x3057,w,0x3056,h,0x3038};EP(*pb)(EP,EP,const EI*)=dlsym(lib,"eglCreatePbufferSurface");s=pb(d,config,surf);EI ctx[]={0x3098,3,0x30FB,3,0x30FD,1,0x3038};EP(*cc)(EP,EP,EP,const EI*)=dlsym(lib,"eglCreateContext");c=cc(d,config,NULL,ctx);fprintf(stderr,"EGL surface=%p context=%p\n",s,c);return c?(GLFWwindow*)1:NULL;}
void glfwMakeContextCurrent(GLFWwindow*w){EI(*f)(EP,EP,EP,EP)=dlsym(lib,"eglMakeCurrent");f(d,s,s,c);}

static unsigned long long draws=0,subcalls=0,datacalls=0,subbytes=0,databytes=0;
void qa_reset_draws(void){draws=subcalls=datacalls=subbytes=databytes=0;}
void qa_report_draws(void){fprintf(stderr,"GL_CALLS frames=60 draws=%llu bufferSub_calls=%llu bufferSub_bytes=%llu bufferData_calls=%llu bufferData_bytes=%llu\n",draws,subcalls,subbytes,datacalls,databytes);}
static void qa_sub(unsigned t,long o,long n,const void*p){static void(*fn)(unsigned,long,long,const void*);if(!fn)fn=proc("glBufferSubData");subcalls++;if(p&&n>0)subbytes+=n;fn(t,o,n,p);}
static void qa_data(unsigned t,long n,const void*p,unsigned u){static void(*fn)(unsigned,long,const void*,unsigned);if(!fn)fn=proc("glBufferData");datacalls++;if(p&&n>0)databytes+=n;fn(t,n,p,u);}
static void qa_arrays(unsigned m,int f,int n){static void(*fn)(unsigned,int,int);if(!fn)fn=proc("glDrawArrays");draws++;fn(m,f,n);}
static void qa_elements(unsigned m,int n,unsigned t,const void*p){static void(*fn)(unsigned,int,unsigned,const void*);if(!fn)fn=proc("glDrawElements");draws++;fn(m,n,t,p);}
GLFWglproc glfwGetProcAddress(const char*n){if(!strcmp(n,"glBufferSubData"))return(GLFWglproc)qa_sub;if(!strcmp(n,"glBufferData"))return(GLFWglproc)qa_data;if(!strcmp(n,"glDrawArrays"))return(GLFWglproc)qa_arrays;if(!strcmp(n,"glDrawElements"))return(GLFWglproc)qa_elements;return(GLFWglproc)proc(n);}

int glfwGetError(const char**s){if(s)*s="EGL test shim";return 0;}
void glfwSwapInterval(int i){}
int glfwWindowShouldClose(GLFWwindow*w){return closed;}
void glfwSetWindowShouldClose(GLFWwindow*w,int v){closed=v;}
void glfwGetFramebufferSize(GLFWwindow*w,int*a,int*b){*a=width;*b=height;}
void glfwGetWindowSize(GLFWwindow*w,int*a,int*b){*a=width;*b=height;}
void glfwGetCursorPos(GLFWwindow*w,double*x,double*y){*x=mx;*y=my;}
int glfwGetMouseButton(GLFWwindow*w,int b){return b==0?mouseState:(b==1?rightState:0);}int glfwGetKey(GLFWwindow*w,int k){return 0;}
void glfwSetInputMode(GLFWwindow*w,int a,int b){}
GLFWcursorposfun glfwSetCursorPosCallback(GLFWwindow*w,GLFWcursorposfun f){cursorcb=f;return NULL;}
GLFWmousebuttonfun glfwSetMouseButtonCallback(GLFWwindow*w,GLFWmousebuttonfun f){mousecb=f;return NULL;}
GLFWkeyfun glfwSetKeyCallback(GLFWwindow*w,GLFWkeyfun f){keycb=f;return NULL;}
GLFWscrollfun glfwSetScrollCallback(GLFWwindow*w,GLFWscrollfun f){scrollcb=f;return NULL;}
GLFWmonitor* glfwGetWindowMonitor(GLFWwindow*w){return NULL;} GLFWmonitor* glfwGetPrimaryMonitor(void){return (GLFWmonitor*)1;}
const GLFWvidmode* glfwGetVideoMode(GLFWmonitor*m){static GLFWvidmode v={1280,720,8,8,8,60};return &v;}
void glfwSetWindowMonitor(GLFWwindow*w,GLFWmonitor*m,int x,int y,int a,int b,int r){}void glfwSetWindowSize(GLFWwindow*w,int a,int b){width=a;height=b;}
void glfwDestroyWindow(GLFWwindow*w){}void glfwTerminate(void){}
static void pointer(double x,double y,int down){mx=x;my=y;if(cursorcb)cursorcb((GLFWwindow*)1,x,y);mouseState=down;if(mousecb)mousecb((GLFWwindow*)1,0,down,0);}
static void orbit(double x,double y,int down){mx=x;my=y;if(cursorcb)cursorcb((GLFWwindow*)1,x,y);if(rightState!=down&&mousecb)mousecb((GLFWwindow*)1,1,down,0);rightState=down;}
void glfwPollEvents(void){}
extern void egl_trace(int frame) __attribute__((weak));
void glfwSwapBuffers(GLFWwindow*w){frames++;if(frames<=12){if(egl_trace)egl_trace(frames);unsigned char*p=malloc(width*height*3);void(*read)(int,int,int,int,unsigned,unsigned,void*)=proc("glReadPixels");void(*pixelStore)(unsigned,int)=proc("glPixelStorei");pixelStore(0x0D05,1);read(0,0,width,height,0x1907,0x1401,p);char path[128];const char*prefix=getenv("STELLA_EGL_CAPTURE_PREFIX");snprintf(path,sizeof(path),"%s-%03d.ppm",prefix?prefix:"/tmp/stella-egl",frames);FILE*f=fopen(path,"wb");fprintf(f,"P6\n%d %d\n255\n",width,height);for(int y=height-1;y>=0;y--)fwrite(p+y*width*3,1,width*3,f);fclose(f);free(p);fprintf(stderr,"Captured %s\n",path);}}
void glfwWindowHintString(int a,const char*b){}

#include <sys/resource.h>
long stella_bench_peak_rss(void){struct rusage u;getrusage(RUSAGE_SELF,&u);return u.ru_maxrss;}

void qa_click(double x,double y){pointer(x,y,1);pointer(x,y,0);}
void qa_pointer(double x,double y,int down){pointer(x,y,down);}
void qa_capture(const char*path){unsigned char*p=malloc(width*height*3);void(*read)(int,int,int,int,unsigned,unsigned,void*)=proc("glReadPixels");void(*pixelStore)(unsigned,int)=proc("glPixelStorei");pixelStore(0x0D05,1);read(0,0,width,height,0x1907,0x1401,p);FILE*f=fopen(path,"wb");fprintf(f,"P6\n%d %d\n255\n",width,height);for(int y=height-1;y>=0;y--)fwrite(p+y*width*3,1,width*3,f);fclose(f);free(p);}
