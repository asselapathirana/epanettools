/* 1.Include input-output library files */
/* The spurious memory effect was gone once the zero assignments were replace by a very small number
for emitter and Base demand values */

/* 20081122 -- Now, the program seem to be working, even works well with the GUI.
Problems: There is a spurious memory effect in the flow. When pressure turns from
positive to negative, there remains a fixed demand??
*/

/* Lesson about emitters:
epanet computes a quanity called E[i] for each node, that will be set to 1 if there is an emitter in
that node AT INITIALIZATION time_ (ENinitH). If emitters are assigned to a node later, this will not happen and
division by zero error will occure (a bug?)
*/

/* Lesson about instability:
Symptom: Erratically, sometime_s the demand just before reaching zero would go very high: (e.g. a)
.     .a
  .
    .
--------.-.-.-
Reason: There is a pressure fluctuation.
When in low_pressures(), pressure is negative, so the situation escapes it.
When in negative_pressrues(), pressure is positive, so that also is escaped.
Solution: Do not run epanet between calls of low_pressure, negative_pressure etc.
Call read_newvalues() only after all checks, just before resuming the next loop cycle.
*/


#include <epanet2.h>
#include <iostream>
#include <math.h>
#include "include.h"
#include <iomanip>
#include <sstream>
#include <fstream>
#include <limits>
#include <float.h>
#include <cstring>
#include <stdlib.h>

using namespace std;
long time_;
void teststate();


float TOLERANCE=(float)1E-2;
float TOLERFACT=(float)1.E25;
vector<node> nodes;
int debug2=false;
int debug1=false;
int MAXTRIALS=1000;
int NOCONVERGE=1;
float ZEROEMIT=TOLERANCE/TOLERFACT; // this seems to kill the memory effect on demand.
float ZEROBD    =TOLERANCE/TOLERFACT;
float NONZERO_SMALL_EMITTER =FLT_MIN; //TOLERANCE/TOLERFACT;
float NEGLDEMAND=TOLERANCE; // negligible demand.
float ACCURACY;
float eexp, // emitter exponent,
	  ecup; // emitter cutoff pressure m or psi or the pressure units used.
int NITER;

bool comp(float v1, float v2){
	 if(min(abs(v1),abs(v2))<TOLERANCE){	//June-2010
		return false;						//June-2010
	}										//June-2010
	return 2*abs(v1-v2)/abs(v1+v2)>TOLERANCE;
}

bool error(int i,int value)
{
	if(value!=0)
	{
		char msg[512];
		ENgeterror(value,msg,512);
		//if(debug2||value>100) sprintf ( err," epanet returned :%i: %s ",value, msg);
		if(i>0){
			//if(debug2||value>100) printf( err,"(Calling index: %i)\n",i);
		}else{
			//if(debug2||value>100) printf(err,"\n");
		}
		ENwriteline(msg); // when called from GUI.
		//cout << msg; // When called on command line.
		if(value>100){
				//cout << "Press any key ...\n"; cin.get();
				cout << msg;
		}
		return true;

	}
		return false;
}
bool error(int value){
	return error(-1,value);
}

/* Run the current hydraulic step again, and read the new demand and pressures to the nodes array */
void read_newvalues(){
	long time_;
	error(ENrunH(&time_));
	for(unsigned  i=0;i< nodes.size(); i++){

		float dem, pres, bd;
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_DEMAND, &dem));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE, &pres));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_BASEDEMAND, &bd));
		nodes.at(i).demand=dem;
		if(i==6){
			cout << "";
		}

		nodes.at(i).pressure=pres;

	}
	//if(debug2) cout ;
}

/*
All nodes with pressure > critical pressure
1. Should not have emitters
2. Should have original demand
*/
bool large_pressures(){
	int ret=0;
	bool sign=false;
	for(unsigned  i=0;i< nodes.size(); i++){
		float ec, pres, dem;
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE , &pres));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_EMITTER, &ec));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_DEMAND, &dem));
		if(pres>ecup &&  abs(nodes.at(i).orig_demand) > abs(TOLERANCE) && comp(dem,nodes.at(i).orig_demand)){
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_BASEDEMAND, nodes.at(i).orig_basedemand));
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_EMITTER, (float)ZEROEMIT));
			sign=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;

		}

	}
	//DO NOT CALL THIS HERE. read_newvalues();
	return sign;
}

void set_emitter(int loc){
			error(nodes.at(loc).index,ENsetnodevalue(nodes.at(loc).index, EN_EMITTER , nodes.at(loc).ec));
			error(nodes.at(loc).index,ENsetnodevalue(nodes.at(loc).index, EN_BASEDEMAND , (float)ZEROBD));

}

/*
IF 0<pressure<ecup and current demand value is different from saved demand, set
1. proper emitter value, to get proper demand
2. demand to zero.
*/
bool low_pressures(){
	bool sign=false;
	int ret=0;
	float pres, dem;
	for(unsigned  i=0;i< nodes.size(); i++){
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE , &pres));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_DEMAND , &dem));
		if(
			(!(pres<0.0) && pres < ecup && comp(nodes.at(i).orig_demand,0) &&
			comp(dem,nodes.at(i).ec*pow(pres,eexp))
			)
			//(dem >= nodes.at(i).orig_demand || dem <= NEGLDEMAND) )

			){
			set_emitter(i);
			sign=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;
		}
		if(comp(nodes.at(i).pressure,pres)){
			sign=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;
		}

	}

	////DO NOT CALL THIS HERE. read_newvalues();
	return sign;
}




/* sets all nodes with current pressure <0 and non-zero demand
1. emitter=0,
2. demand=0 */
bool negative_pressures(){
	bool sign=false;
	int ret=0;
	float dem, pres;
	for(unsigned  i=0;i< nodes.size(); i++){
		float bd, ec;
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_DEMAND, &dem));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_BASEDEMAND, &bd));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_EMITTER, &ec));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE, &pres));

		if(pres < 0.0 && dem > TOLERANCE ){
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_EMITTER, (float)ZEROEMIT));
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_BASEDEMAND, (float)ZEROBD));
			sign=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;
		}

		if(dem<-TOLERANCE){
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_EMITTER, (float)ZEROEMIT));
			error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_BASEDEMAND, (float)ZEROBD));
			sign=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;
		}

	}
	////DO NOT CALL THIS HERE. read_newvalues();
	return sign;
}

void print_results(){

		for(unsigned int i=0;i<nodes.size();i++){
			if(i==6){
			float ec, bd;
			error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_EMITTER , &ec));
			error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_BASEDEMAND , &bd));
			if(debug1) printf("NODE : %s\tPres:%8.3f  Dem:%8.3f (BD:%8.3f) Em: %7.4f\n",
				nodes.at(i).id.c_str(),nodes.at(i).pressure, nodes.at(i).demand,bd, ec );
			}
		}

}


/* Obtain the demand for the current node */

float  get_orig_demand(long time_, int i){
	float bd, pat, mult;
	int len;
	long pstep, pstart;
	error(i,ENgetnodevalue(i, EN_BASEDEMAND , &bd));
	error(i,ENgetnodevalue(i, EN_PATTERN , &pat));
	float demand=1.0f;
	if(pat>0){
		error(ENgetpatternlen((int)pat,&len));
		error(ENgettimeparam(EN_PATTERNSTEP,&pstep));
		error(ENgettimeparam(EN_PATTERNSTART,&pstart));
		long patstep=(time_+pstart)/pstep;
		patstep=patstep%len;
		error(ENgetpatternvalue((int)pat,patstep+1,&demand));
	}
	error(ENgetoption(EN_DEMANDMULT,&mult));
	demand=demand*bd*mult;
	return demand;
}

/* Read Original demands, base demands */
void read_originals(){
		int tmp ;
        error(ENgetcount(EN_NODECOUNT, &tmp));
        //if(debug2) printf ( " Number of nodes is  %i\n",tmp);
		float demand;
		error(ENrunH(&time_));
		//if(debug2) cout << "BEFORE ANALYSIS: \n";
        for(int i = 1; i <= tmp; i++)
			{
				int type=-1;
			    error(i,ENgetnodetype(i,&type));
				if(type != EN_JUNCTION)
				{
					continue;
				}
			    char  id[256];
              	float  bd, pres,ec;
				error(i,ENgetnodevalue(i, EN_BASEDEMAND , &bd));
				error(i,ENgetnodevalue(i, EN_PRESSURE , &pres));
				error(i,ENgetnodeid(i, id));
                /* 5.Calculate the emitter coefficients */
				node tmp;
				demand=get_orig_demand(time_,i);
				//now if demand is negative at this stage that means, it is a supply node (e.g. EPANET2 ex.2)
				if(demand < 0.0){
					char msg[256];
					sprintf(msg,"**** The node ID:%s (index %i) has a negative demand. It is not considered in the emitter analysis.",
						id,i);
					ENwriteline(msg);
					continue;
				}
				tmp.orig_demand=demand<0?0.0:demand;
				tmp.demand=tmp.orig_demand;
			//	tmp.demandmult=(bd==0)?(float)0.0:demand/bd;
				tmp.orig_basedemand=bd;
				tmp.id=id;
				tmp.index=i;
				tmp.pressure=pres;
				tmp.ec=tmp.orig_demand/pow((float)ecup,(float)eexp);
				tmp.offender=false;
				nodes.push_back(tmp);
				float   demand;

		}
}

void reset_network(){
	//if(debug2) cout << "AT RESET: \n";
	for(unsigned  i=0;i< nodes.size(); i++){
		error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_BASEDEMAND, nodes.at(i).orig_basedemand));
		error(nodes.at(i).index,ENsetnodevalue(nodes.at(i).index, EN_EMITTER, (float)ZEROEMIT));

		/*if(debug2){
			float  bd, demand, ec;
			error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_BASEDEMAND , &bd));
			error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_EMITTER , &ec));
			error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_DEMAND , &demand));
			cout << nodes.at(i).orig_basedemand << '\t' << bd <<"  \t" << demand <<"  \t" << ec <<'\n';
		}*/
	}
	//if(debug2) cout << endl;

}

void getEmitterData(float *eexp_, float *ecup_){
	*eexp_=eexp;
	*ecup_=ecup;
}

void setEmitterData(float eexp_, float ecup_){
	eexp=eexp_;
	ecup=ecup_;
}


int emitter_analysis_prepare(){
		int tmp ;
		getEmitterData(&eexp, &ecup);
		error(ENgetoption(EN_ACCURACY,&ACCURACY));
        error(ENgetcount(EN_NODECOUNT, &tmp));
		for(int i = 1; i <= tmp; i++)
		{
			int type=-1;
			error(i,ENgetnodetype(i,&type));
			if(type != EN_JUNCTION)
			{
				continue;
			}
			error(i,ENsetnodevalue(i, EN_EMITTER, (float)NONZERO_SMALL_EMITTER));
		}

		return 0;

}

bool still_evolving(){
	bool notyet=false;

	for(unsigned  i=0;i< nodes.size(); i++){
		float pres,dem;
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE, &pres));
		error(nodes.at(i).index,ENgetnodevalue(nodes.at(i).index, EN_PRESSURE, &dem));
		if(!(abs(nodes.at(i).saved_pressure-pres)<ACCURACY)
			||!(abs(nodes.at(i).saved_demand-dem)<ACCURACY)
			){
			notyet=true;
			if(NITER > MAXTRIALS)nodes.at(i).offender=true;
		}
		nodes.at(i).saved_pressure=pres;
		nodes.at(i).saved_demand  =dem ;

	}
	return notyet;
}

void set_emitters(){
	for(unsigned  i=0;i< nodes.size(); i++){
		set_emitter(i);
	}

}

int emitter_analysis()
{
        int ret=0;
 		read_originals();
		set_emitters();
		read_newvalues();


        bool flag1=true, flag2=true, flag3=true, flag4=true, last=true;
		NITER=0;
		int lastcount=0;
		do{
			last=flag1||flag2||flag3||flag4;
			flag1=low_pressures();
			flag2=negative_pressures();
			flag3=large_pressures();
			flag4=still_evolving();
			read_newvalues(); //CALL THIS HERE. Not at the end of each test above.
			//if(debug2) cout <<  "looping...\n\n\n";

			if(NITER++ > MAXTRIALS){/* we need to write a message here to the report */
				char msg[500];

				if(lastcount==0){
					sprintf(msg,"\n******************** NON-CONVERGENCE ***************************");
					 ENwriteline(msg);cout << msg;
					sprintf(msg,"\n%7s %7s %7s %7s : offending nodes", "low_pre","neg_pres",  "lar_pres",  "evolv");
					 ENwriteline(msg);cout << msg;

				}
				string str;
				sprintf(msg,"\n%1i%1i%1i%1i : ",
					flag1, flag2, flag3, flag4);
				//cout << msg;
				str+=msg;
				for(unsigned int i=0;i<nodes.size();i++){

				    if(nodes.at(i).offender){
						char val[256]; strcpy(val,nodes.at(i).id.c_str());

						str+=string(val);str+=" "; //cout << val; cout << " ";
					}
				}
				string str2=str.substr(0,5000);
				char p[5001];
				std::strcpy(p,str2.c_str());
				cout << endl << p ;
				ENwriteline(p);
				if(lastcount++>5){
					sprintf(msg,"\n****************************************************************\n");
					cout << msg;
					return NOCONVERGE;
				}
			}
			for(unsigned int i=0;i<nodes.size();i++){nodes.at(i).offender=false;}

		}while(flag1 || flag2|| flag3||last);


		return 0;
}

int getniter(){
	return NITER;
}

int post_analysis_cleanup(){
	    //print_results();
		reset_network(); // need to set base demands.
		nodes.clear(); // clear the nodes array so that new analysis cycle starts fresh.
		return 0;

}

/**int main(int argc, char ** argv){
	long tstep;
	error(ENopen("../data/nid2280.inp","EMIT_STANDALONE.rpt",""));
    error(ENopenH());
	emitter_analysis_prepare();
	error(ENinitH(0));
	/* How the following is done in GUI (Delphi) code (ref: Fsimul.pas)
	   // Solve hydraulics in each period
      repeat
        StatusLabel.Caption := Format('%s %.2f',[slabel,h]);
        Application.ProcessMessages;
        err := ENrunH(t);
        tstep := 0;
        if err <= 100 then err := ENnextH(tstep);
        h := h + tstep/3600;
      until (tstep = 0) or (err > 100) or (RunStatus = rsCancelled);
    end;


	int cc=0;
	do{

		//if(debug2) cout << setw(5);
		if(cc==5){
			cout << "";
		}
		emitter_analysis();
		cout << cc++ << " : ";
		error(ENrunH(&time_));
		post_analysis_cleanup();
		ENnextH(&tstep);
		//cin.get();
	}while (tstep > 0);
	ENreport();
	ENcloseH();

}
*/


