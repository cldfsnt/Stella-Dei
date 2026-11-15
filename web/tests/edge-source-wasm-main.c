#include <stdio.h>
extern unsigned qa_run(void);
int main(void){unsigned f=qa_run();printf("EDGE_SOURCE_WASM failures=%u random=100000 special=81 zero_length=1 exact_bits=true\n",f);return f?1:0;}
