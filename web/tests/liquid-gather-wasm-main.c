#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
extern unsigned qa_run(const unsigned char*,size_t,const unsigned char*,size_t,unsigned);
extern const unsigned char*qa_output(void);extern size_t qa_output_len(void);
static FILE*trace;
static void put(const void*p,size_t z){if(!trace||fwrite(p,1,z,trace)!=z)exit(9);}
void qa_trace(uint32_t n,uint32_t tick,double area,const float*pre,const float*post,const float*edges,const double*accum){
 put(edges?"LQTRACE1":"LQBASE01",8);put(&n,4);put(&tick,4);put(&area,8);put(pre,n*4);put(post,n*4);if(edges){put(edges,n*24);put(accum,n*8);}
}
static unsigned char*read_all(char*path,size_t*n){FILE*f=fopen(path,"rb");if(!f)exit(3);fseek(f,0,SEEK_END);*n=ftell(f);rewind(f);unsigned char*p=malloc(*n);if(!p||fread(p,1,*n,f)!=*n)exit(4);fclose(f);return p;}
int main(int argc,char**argv){if(argc!=5&&argc!=6)return 2;if(argc==6){trace=fopen(argv[5],"wb");if(!trace)return 8;}size_t n,g;unsigned char*p=read_all(argv[1],&n),*q=read_all(argv[2],&g);if(qa_run(p,n,q,g,atoi(argv[4])))return 5;FILE*f=fopen(argv[3],"wb");if(!f)return 6;size_t z=qa_output_len();if(fwrite(qa_output(),1,z,f)!=z)return 7;fclose(f);if(trace)fclose(trace);return 0;}
