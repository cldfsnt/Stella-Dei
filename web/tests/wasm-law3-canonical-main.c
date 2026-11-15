#include <emscripten/heap.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
extern unsigned qa_run(const unsigned char*,size_t,const unsigned char*,size_t,unsigned);
extern void qa_set_candidate(unsigned);
extern const unsigned char*qa_output(void);extern size_t qa_output_len(void);
static unsigned char*read_all(char*path,size_t*n){FILE*f=fopen(path,"rb");if(!f)exit(3);fseek(f,0,SEEK_END);*n=ftell(f);rewind(f);unsigned char*p=malloc(*n);if(!p||fread(p,1,*n,f)!=*n)exit(4);fclose(f);return p;}
int main(int argc,char**argv){if(argc!=6)return 2;size_t n,g;unsigned char*p=read_all(argv[1],&n),*q=read_all(argv[2],&g);qa_set_candidate(atoi(argv[5]));if(qa_run(p,n,q,g,atoi(argv[4])))return 5;fprintf(stderr,"WASM_HEAP_CAPACITY bytes=%zu includes_harness_io=1\n",emscripten_get_heap_size());FILE*f=fopen(argv[3],"wb");if(!f)return 6;size_t z=qa_output_len();if(fwrite(qa_output(),1,z,f)!=z)return 7;fclose(f);return 0;}
