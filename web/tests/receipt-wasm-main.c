#include <stdio.h>
extern unsigned qa_run(void);
extern double qa_metric(unsigned);
int main(void){unsigned failures=qa_run();printf("RECEIPT_WASM failure_bits=%u credit_cases=10000 support_cases=16 aggregate_cases=36 neutral48day_controls=4 known_tiny_N_witness_expected=true\n",failures);for(unsigned i=0;i<6;i++)printf("metric[%u]=%.17g\n",i,qa_metric(i));return failures?1:0;}
