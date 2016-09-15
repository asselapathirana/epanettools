#include <stdio.h>
#include <epanet2.h>
#include <wrapper.h>
int main(){
    printf("Enter the network file (xxxx.inp):\n");
    int k=ENopen_wrap("E:/Projects/2016_Bdesh_training_with_dutch_waterboards/Assela Pathirana/risk_based/Adjumani_network_simplified2.inp",
                      "E:/Projects/2016_Bdesh_training_with_dutch_waterboards/Assela Pathirana/risk_based/Adjumani_network_simplified2.rpt","");
    if(k!=0){printf("Error %i\n", k);}
    int NumNodes;
    k=ENgetcount_wrap(EN_NODECOUNT, &NumNodes);
    if(k!=0){printf("Error %i\n", k);}
    printf("Number of nodes %i\n", NumNodes);
    float eexp, ecup;
    k=ENgetemitter_wrap(&eexp,&ecup);
    printf("Emitter %f %f\n", eexp, ecup);
    if(eexp==0.0 || ecup ==0.0){
        ENsetemitter_wrap(.5,10.0);
    }
    k=ENgetemitter_wrap(&eexp,&ecup);
    printf("Emitter %f %f\n", eexp, ecup);
    getchar();
    ENopenH_wrap();  ENinitH_wrap(0);
    long t,tstep;
    int i;
    float p;
    char id[50];
    do{
        ENrunH_wrap(&t);
        for (i = 1; i <= NumNodes; i++)
        {
            ENgetnodevalue_wrap(i, EN_PRESSURE, &p);
            ENgetnodeid_wrap(i, id);
            printf("pressure: %lu %s %f \n",t, id, p);
        }
        ENnextH_wrap(&tstep);
    } while (tstep > 0);
    ENcloseH_wrap();
    ENclose_wrap();





}
