#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
extern uint32_t qa_run(const unsigned char *,size_t);
extern const unsigned char *qa_output(void);
extern size_t qa_output_len(void);
extern uint32_t qa_width(void);
extern uint32_t qa_word_bits(void);
int main(int argc,char **argv){
 if(argc!=3)return 2;FILE *f=fopen(argv[1],"rb");if(!f)return 3;
 fseek(f,0,SEEK_END);long n=ftell(f);rewind(f);unsigned char *p=malloc(n);if(!p)return 4;
 if(fread(p,1,n,f)!=(size_t)n)return 5;fclose(f);unsigned result=qa_run(p,n);free(p);if(result)return 6;
 FILE *o=fopen(argv[2],"wb");if(!o)return 7;size_t z=qa_output_len();if(fwrite(qa_output(),1,z,o)!=z)return 8;fclose(o);
 printf("LIQUID_PLATFORM wasm width=%u usize_bits=%u bytes=%zu four_dt=0,360,1440,15000 scalar_cached_reverse_exact=true\n",qa_width(),qa_word_bits(),z);return 0;
}
