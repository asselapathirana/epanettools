#include <epanet2.h>
#include <stdlib.h>


char TmpDir[200];

extern int ENsetpatterndim(int index, int dim){
    int i;    
    float * pat=malloc(sizeof(float)*dim);
    for (i=0;i<dim;i++){
        pat[i]=0.0;
        }
    return (ENsetpattern(index,pat,dim));
    }
    
extern int ENsetpatterndim_wrap(int index, int dim){
    return (ENsetpatterndim(index,dim));
}