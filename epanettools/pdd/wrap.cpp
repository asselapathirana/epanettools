#include <epanet2.h> 
#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib>
#include "wrapper.h"
#include <cstring>
static bool usehydfile=false;
static long currenttime=-9999;
using namespace std;

extern long getcurrenttime (){
 	return currenttime;
}

void  writecon (char *s)
/*----------------------------------------------------------------
**  Input:   text string                                         
**  Output:  none                                                
**  Purpose: writes string of characters to console              
**----------------------------------------------------------------
*/
{
#ifdef CLE                                                                     // (2.00.11 - LR)
   fprintf (stdout,s);
   fflush (stdout);
#endif
}

/* Write  a signature to the report file, so that the user knows this is not the original epanet */
extern int   write_sign (string str){
		int ret1=0;    
			string s= ("** Note: <BEGIN> "+str+"<END> **\n").c_str ();
			char * m;
			m = new char[s.length () + 1];
			strcpy (m, s.c_str ());
			ret1+=ENwriteline (m);
	
 		return ret1;

}

DLLEXPORT ENsetemitter_wrap(float a1, float a2){
	setEmitterData(a1,a2);
	return 1;
}
DLLEXPORT ENgetemitter_wrap(float* a1, float* a2){
	 getEmitterData(a1,a2);
	 return 1;

}

DLLEXPORT ENepanet_wrap (char * f1,  char * f2,  char * f3,  void  (*pviewprog)  (char *)){
	write_sign ("ENepanet is not implemented in this custom dll");
    writecon ("This function is not implimented!! ");
 	return (WRAPPER_ERROR_NOT_IMPLEMENTED);
}

DLLEXPORT ENopen_wrap (char * a1,  char * a2,  char * a3){
	usehydfile=false; // don't try to use old hydraulics files. 
	write_sign ("This is a custom epanet2.dll");
	run_before_ENopen();
 	return ENopen (a1,a2,a3);
}

DLLEXPORT ENsaveinpfile_wrap (char *a1){
	run_before_ENsaveinpfile();
 	return ENsaveinpfile ( a1); 
}

DLLEXPORT ENclose_wrap (void){
	run_before_ENclose();
	write_sign(" This was a custom epanet2 run!");
     return ENclose (); 
}



DLLEXPORT ENsolveH_wrap (void){
	write_sign ("ENsolveH is not implemented in this custom dll");
    writecon ("This function is not implimented!! ");
 	return (WRAPPER_ERROR_NOT_IMPLEMENTED);
}

DLLEXPORT ENsaveH_wrap (void){
	run_before_ENsaveH();
     return ENsaveH (); 
}

DLLEXPORT ENopenH_wrap (void){
		int ret1=ENwriteline("================================================================================");
		ret1=ENwriteline    ("===== USING A MODIFIED EPANET, Assela Pathirana, a.pathirana@unesco-ihe.org ====");
		ret1=ENwriteline	("=====    Pay attention to \"Note:\" statements in the report below,          ====");
		ret1=ENwriteline	("=====    particularly the parts between<BEBIN> and <END> tags.              ====");
		ret1=ENwriteline	("================================================================================");
	run_before_ENopenH();
    int ret=ENopenH (); 
	if (ret==0){
		currenttime=0;
	}
 	return ret;
}

DLLEXPORT ENinitH_wrap (int a1){
	run_before_ENinitH();
     return ENinitH (a1); 
}

/* this is the function the interface use to run hydraulics */
DLLEXPORT ENrunH_wrap (long *a1){
	int ret=run_before_ENrunH ();
    int ret1=ENrunH (a1); 
	currenttime= (*a1);
	return ret1==0?ret:ret1;
}

DLLEXPORT ENnextH_wrap (long *a1){
	run_before_ENnextH();
     return ENnextH (a1); 
}

DLLEXPORT ENcloseH_wrap (void){
	run_before_ENcloseH();
     return ENcloseH (); 
}

DLLEXPORT ENsavehydfile_wrap (char *a1){
	run_before_ENsavehydfile();
     return ENsavehydfile (a1); 
}

DLLEXPORT ENusehydfile_wrap (char *a1){
	usehydfile=true;
	run_before_ENusehydfile();
     return ENusehydfile (a1); 
}

DLLEXPORT ENsolveQ_wrap (void){
	run_before_ENsolveQ();
     return ENsolveQ (); 
}

DLLEXPORT ENopenQ_wrap (void){
	run_before_ENopenQ();
     return ENopenQ (); 
}

DLLEXPORT ENinitQ_wrap (int a1){
	run_before_ENinitQ();
     return ENinitQ (a1); 
}

DLLEXPORT ENrunQ_wrap (long *a1){
	run_before_ENrunQ();
     return ENrunQ (a1); 
}

DLLEXPORT ENnextQ_wrap (long *a1) {
	run_before_ENnextQ();
     return ENnextQ (a1); 
}

DLLEXPORT ENstepQ_wrap (long *a1) {
	run_before_ENstepQ();
     return ENstepQ (a1); 
}

DLLEXPORT ENcloseQ_wrap (void){
	run_before_ENcloseQ();
     return ENcloseQ (); 
}


DLLEXPORT ENwriteline_wrap (char *a1) {
	run_before_ENwriteline();
     return ENwriteline (a1); 
}

DLLEXPORT ENreport_wrap (void){
	run_before_ENreport();
     return ENreport (); 
}

DLLEXPORT ENresetreport_wrap (void){
	run_before_ENresetreport();
     return ENresetreport (); 
}

DLLEXPORT ENsetreport_wrap (char *a1) {
	run_before_ENsetreport();
     return ENsetreport (a1); 
}


DLLEXPORT ENgetcontrol_wrap (int a1,  int * a2,  int * a3,  float * a4, int* a5, float * a6)  {
	run_before_ENgetcontrol();
     return ENgetcontrol (a1, a2, a3,  a4, a5, a6);  
}


DLLEXPORT ENgetcount_wrap (int a1,  int *a2) {
	run_before_ENgetcount();
     return ENgetcount (a1, a2);
}

DLLEXPORT ENgetoption_wrap (int a1,  float *a2) {
	run_before_ENgetoption();
     return ENgetoption (a1, a2);
}

DLLEXPORT ENgettimeparam_wrap (int a1,  long *a2) {
	run_before_ENgettimeparam();
     return ENgettimeparam (a1, a2);
}

DLLEXPORT ENgetflowunits_wrap (int *a1) {
	run_before_ENgetflowunits();
     return ENgetflowunits (a1); 
}

DLLEXPORT ENgetpatternindex_wrap (char * a1,  int *a2) {
	run_before_ENgetpatternindex();
     return ENgetpatternindex (a1, a2);
}

DLLEXPORT ENgetpatternid_wrap (int a1,  char *a2) {
	run_before_ENgetpatternid();
     return ENgetpatternid (a1, a2);
}

DLLEXPORT ENgetpatternlen_wrap (int a1,  int *a2) {
	run_before_ENgetpatternlen();
     return ENgetpatternlen (a1, a2);
}

DLLEXPORT ENgetpatternvalue_wrap (int a1,  int a2,  float *a3) {
	run_before_ENgetpatternvalue();
     return ENgetpatternvalue (a1, a2, a3);
}

DLLEXPORT ENgetqualtype_wrap (int * a1,  int *a2) {
	run_before_ENgetqualtype();
     return ENgetqualtype (a1,a2); 
}

DLLEXPORT ENgeterror_wrap (int a1,  char * a2,  int a3){
	run_before_ENgeterror();
     return ENgeterror (a1,a2, a3);
}


DLLEXPORT ENgetnodeindex_wrap (char * a1,  int *a2) {
	run_before_ENgetnodeindex();
     return ENgetnodeindex (a1, a2);
}

DLLEXPORT ENgetnodeid_wrap (int a1,  char *a2) {
	run_before_ENgetnodeid();
     return ENgetnodeid (a1, a2);
}

DLLEXPORT ENgetnodetype_wrap (int a1,  int *a2) {
	run_before_ENgetnodetype();
     return ENgetnodetype (a1, a2);
}

DLLEXPORT ENgetnodevalue_wrap (int a1,  int a2,  float *a3) {
	run_before_ENgetnodevalue();
     return ENgetnodevalue (a1,a2,a3);
}

 
DLLEXPORT ENgetlinkindex_wrap (char * a1,  int *a2) {
	run_before_ENgetlinkindex();
     return ENgetlinkindex (a1,a2);
}

DLLEXPORT ENgetlinkid_wrap (int a1,  char *a2) {
	run_before_ENgetlinkid();
     return ENgetlinkid (a1,a2); 
}

DLLEXPORT ENgetlinktype_wrap (int a1,  int *a2) {
	run_before_ENgetlinktype();
     return ENgetlinktype (a1,a2); 
}

DLLEXPORT ENgetlinknodes_wrap (int a1,  int * a2,  int *a3) {
	run_before_ENgetlinknodes();
     return ENgetlinknodes (a1,a2,a3); 
}

DLLEXPORT ENgetlinkvalue_wrap (int a1,  int a2,  float *a3) {
	run_before_ENgetlinkvalue();
     return ENgetlinkvalue (a1,a2,a3); 
}


DLLEXPORT ENgetversion_wrap (int *a1) {
	run_before_ENgetversion();
     return ENgetversion (a1); 
}


DLLEXPORT ENsetcontrol_wrap (int a1,  int a2,  int a3,  float a4,  int a5,  float a6){
	run_before_ENsetcontrol();
     return ENsetcontrol (a1,a2,a3,a4,a5,a6); 
}

DLLEXPORT ENsetnodevalue_wrap (int a1,  int a2,  float a3){
	run_before_ENsetnodevalue();
     return ENsetnodevalue (a1,a2,a3); 
}

DLLEXPORT ENsetlinkvalue_wrap (int a1,  int a2,  float a3){
	run_before_ENsetlinkvalue();
     return ENsetlinkvalue (a1,a2,a3); 
}

DLLEXPORT ENaddpattern_wrap (char *a1) {
	run_before_ENaddpattern();
     return ENaddpattern (a1); 
}

DLLEXPORT ENsetpattern_wrap (int a1,  float * a2,  int a3){
	run_before_ENsetpattern();
     return ENsetpattern (a1,a2,a3); 
}

DLLEXPORT ENsetpatternvalue_wrap (int a1,  int a2,  float a3){
	run_before_ENsetpatternvalue();
     return ENsetpatternvalue (a1,a2,a3); 
}

DLLEXPORT ENsettimeparam_wrap (int a1,  long a2){
	run_before_ENsettimeparam();
     return ENsettimeparam (a1,a2); 
}

DLLEXPORT ENsetoption_wrap (int a1,  float a2){
	run_before_ENsetoption();
     return ENsetoption (a1,a2); 
}

DLLEXPORT ENsetstatusreport_wrap (int a1){
	run_before_ENsetstatusreport();
     return ENsetstatusreport (a1); 
}

DLLEXPORT ENsetqualtype_wrap (int a1,  char * a2,  char * a3,  char *a4) {
	run_before_ENsetqualtype();
     return ENsetqualtype (a1,a2,a3,a4); 
}




/* 
|sed 's/(/ (/g'|awk '{if($1=="return"){print "\trun_before_" $2"();\n", $0}else{print $0}}'
*/
