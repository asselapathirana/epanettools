#include <stdio.h>
#include <epanet2.h>
int main(){
    printf("Hello\n");
    int k=ENopen("../../epanettools/examples/simple/Net3.inp","tmp.rpt","");
    printf("Returned %i\n", k);
    k=ENsaveinpfile("a.inp");
    printf("Returned %i\n", k);
    k=ENsetlinkvalue(81,0,9999);
    printf("Returned %i\n", k);
    k=ENsaveinpfile("b.inp");
    printf("Returned %i\n", k);
}
