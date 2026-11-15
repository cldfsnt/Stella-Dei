#include <stdio.h>
#include <stdint.h>
extern unsigned qa_run(void);extern uint64_t qa_hash(void);extern unsigned qa_count(void);
int main(void){unsigned f=qa_run();printf("NEAREST_TARGET failures=%u cases=%u hash=%016llx\n",f,qa_count(),(unsigned long long)qa_hash());return f?1:0;}
