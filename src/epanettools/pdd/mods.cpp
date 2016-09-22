#include <epanet2.h>
#include <wrapper.h>
#include <sstream>
#include <include.h>

float value, EEXP, ECUP;

string itoa_(long num)
{
    stringstream converter;
    converter << num;
    return converter.str();
}


string ftoa_(float num)
{
    stringstream converter;
    converter << num;
    return converter.str();
}

/* Following is a function to access the analysis system before each toolkit function. 
For the sake of completeness, all toolkit functions are addressed. But many could be useless
e.g. run_before_ENget<something> -- what is there to set before getting a network property!)
*/

int run_before_ENopen(){
	return 0;
}
int run_before_ENsaveinpfile(){
	return 0;
}
int run_before_ENclose(){
	return 0;
}
int run_before_ENsaveH(){
	return 0;
}
int run_before_ENinitH(){
	emitter_analysis_prepare(); // this is extremely important
	getEmitterData(&EEXP, &ECUP);
	write_sign("Using P="+ftoa_(ECUP)+ " as cutoff pressure for emitters.");
	write_sign("Using n="+ftoa_(EEXP)+ " as emitter exponent.");
	float val;
	ENgetoption(EN_ACCURACY,&val);
	write_sign("Using n="+ftoa_(val)+ " as accuracy for pressure convergence.");
	return 0;
}

int run_before_ENnextH(){
	//write_sign("... Ended cleanup for hour: "+itoa_(getcurrenttime()/3600)+" xxxxx ");
	post_analysis_cleanup();
	return 0;
}
int run_before_ENcloseH(){
	write_sign("... Ended the custom hydraulic analysis.");
	return 0;
}
int run_before_ENsavehydfile(){
	return 0;
}
int run_before_ENusehydfile(){
	return 0;
}
int run_before_ENsolveQ(){
	return 0;
}
int run_before_ENopenQ(){
	return 0;
}
int run_before_ENinitQ(){
	return 0;
}
int run_before_ENrunQ(){
	return 0;
}
int run_before_ENnextQ(){
	return 0;
}
int run_before_ENstepQ(){
	return 0;
}
int run_before_ENcloseQ(){
	return 0;
}
int run_before_ENwriteline(){
	return 0;
}
int run_before_ENreport(){
	return 0;
}
int run_before_ENresetreport(){
	return 0;
}
int run_before_ENsetreport(){
	return 0;
}
int run_before_ENgetcontrol(){
	return 0;
}
int run_before_ENgetcount(){
	return 0;
}
int run_before_ENgetoption(){
	return 0;
}
int run_before_ENgettimeparam(){
	return 0;
}
int run_before_ENgetflowunits(){
	return 0;
}
int run_before_ENgetpatternindex(){
	return 0;
}
int run_before_ENgetpatternid(){
	return 0;
}
int run_before_ENgetpatternlen(){
	return 0;
}
int run_before_ENgetpatternvalue(){
	return 0;
}
int run_before_ENgetqualtype(){
	return 0;
}
int run_before_ENgeterror(){
	return 0;
}
int run_before_ENgetnodeindex(){
	return 0;
}
int run_before_ENgetnodeid(){
	return 0;
}
int run_before_ENgetnodetype(){
	return 0;
}
int run_before_ENgetnodevalue(){
	return 0;
}
int run_before_ENgetlinkindex(){
	return 0;
}
int run_before_ENgetlinkid(){
	return 0;
}
int run_before_ENgetlinktype(){
	return 0;
}
int run_before_ENgetlinknodes(){
	return 0;
}
int run_before_ENgetlinkvalue(){
	return 0;
}
int run_before_ENgetversion(){
	return 0;
}
int run_before_ENsetcontrol(){
	return 0;
}
int run_before_ENsetnodevalue(){
	return 0;
}
int run_before_ENsetlinkvalue(){
	return 0;
}
int run_before_ENaddpattern(){
	return 0;
}
int run_before_ENsetpattern(){
	return 0;
}
int run_before_ENsetpatternvalue(){
	return 0;
}
int run_before_ENsettimeparam(){
	return 0;
}
int run_before_ENsetoption(){
	return 0;
}
int run_before_ENsetstatusreport(){
	return 0;
}
int run_before_ENsetqualtype(){
	return 0;
}
int run_before_ENopenH(){
	write_sign("Starting the custom hydraulic analysis...");
	return 0;
}
int run_before_ENrunH (){
	int ret=emitter_analysis();
	if(ret!=0){
		write_sign("ERROR: Non-converging emitter analysis!!!");
	}
	write_sign("PDD analysis ended for hour:  "+ftoa_((getcurrenttime()/3600.+1.))+" with "
		+ itoa_(getniter())+ " iterations.");
	/* string name="file-"+itoa_(getcurrenttime())+".inp";
	char * name2;
	strcpy(name2,name.c_str());
	int ret=ENsaveinpfile(name2);
	write_sign("Writing a temp file "+name+"  00000 " + itoa_(ret));
	*/
	
	return ret;
}



