#ifndef WRAP_H
#define WRAP_H

#define WRAPPER_ERROR_FILE_OPEN 900000
#define WRAPPER_ERROR_NOT_IMPLEMENTED 910000

#undef WINDOWS
#undef __WIN32__

// --- define DLLEXPORT
#ifndef DLLEXPORT
 #ifdef __cplusplus
  #define DLLEXPORT extern "C" int
 #else
  #define DLLEXPORT extern int
 #endif
#endif



#include <string>
using namespace std;

 /* 26-Aug-2016 : IMPORTANT: all output parameters in wrapper.h has to be named and then declared below. See epanet2.h and epanet2.i files for examples.
At the moment only a few were done to test.  
*/


DLLEXPORT ENepanet_wrap(char * f1,  char * f2,  char * f3,  void (*pviewprog) (char *));
DLLEXPORT ENopen_wrap(char * a1,  char * a2,  char * a3);
DLLEXPORT ENsaveinpfile_wrap(char *a1);
DLLEXPORT ENclose_wrap(void);
DLLEXPORT ENsolveH_wrap(void);
DLLEXPORT ENsaveH_wrap(void);
DLLEXPORT ENopenH_wrap(void);
DLLEXPORT ENinitH_wrap(int a1);
DLLEXPORT ENrunH_wrap(long *result);
DLLEXPORT ENnextH_wrap(long *result);
DLLEXPORT ENcloseH_wrap(void);
DLLEXPORT ENsavehydfile_wrap(char *a1);
DLLEXPORT ENusehydfile_wrap(char *a1);
DLLEXPORT ENsolveQ_wrap(void);
DLLEXPORT ENopenQ_wrap(void);
DLLEXPORT ENinitQ_wrap(int a1);
DLLEXPORT ENrunQ_wrap(long *result);
DLLEXPORT ENnextQ_wrap(long *result) ;
DLLEXPORT ENstepQ_wrap(long *result) ;
DLLEXPORT ENcloseQ_wrap(void);
DLLEXPORT ENwriteline_wrap(char *a1) ;
DLLEXPORT ENreport_wrap(void);
DLLEXPORT ENresetreport_wrap(void);
DLLEXPORT ENsetreport_wrap(char *a1) ;
DLLEXPORT ENgetcontrol_wrap(int ,  int * ci1,  int * ci2,  float * c1,
			     int* ci3, float * c2)  ;
DLLEXPORT ENgetcount_wrap(int a1,  int * result) ;
DLLEXPORT ENgetoption_wrap(int a1,  float * result) ;
DLLEXPORT ENgettimeparam_wrap(int a1,  long * result) ;
DLLEXPORT ENgetflowunits_wrap(int *result) ;
DLLEXPORT ENgetpatternindex_wrap(char * a1,  int * result) ;
DLLEXPORT ENgetpatternid_wrap(int a1,  char * result) ;
DLLEXPORT ENgetpatternlen_wrap(int a1,  int * result) ;
DLLEXPORT ENgetpatternvalue_wrap(int a1,  int a2,  float *result) ;
DLLEXPORT ENgetqualtype_wrap(int * result1,  int * result) ;
DLLEXPORT ENgeterror_wrap(int a1,  char * a2,  int a3);
DLLEXPORT ENgetnodeindex_wrap(char * result,  int *a2) ;
DLLEXPORT ENgetnodeid_wrap(int a1,  char * result); 
DLLEXPORT ENgetnodetype_wrap(int a1,  int * result) ;
DLLEXPORT ENgetnodevalue_wrap(int a1,  int a2,  float *result) ;
DLLEXPORT ENgetlinkindex_wrap(char * a1,  int *result) ;
DLLEXPORT ENgetlinkid_wrap(int a1,  char *result) ;
DLLEXPORT ENgetlinktype_wrap(int a1,  int *result) ;
DLLEXPORT ENgetlinknodes_wrap(int a1,  int * result1,  int *result2) ;
DLLEXPORT ENgetlinkvalue_wrap(int a1,  int a2,  float *result) ;
DLLEXPORT ENgetversion_wrap(int *a1) ;
DLLEXPORT ENsetcontrol_wrap(int a1,  int a2,  int a3,  float a4,  int a5,  float a6);
DLLEXPORT ENsetnodevalue_wrap(int a1,  int a2,  float a3);
DLLEXPORT ENsetlinkvalue_wrap(int a1,  int a2,  float a3);
DLLEXPORT ENaddpattern_wrap(char *a1) ;
DLLEXPORT ENsetpattern_wrap(int a1,  float * a2,  int a3);
DLLEXPORT ENsetpatternvalue_wrap(int a1,  int a2,  float a3);
DLLEXPORT ENsettimeparam_wrap(int a1,  long a2);
DLLEXPORT ENsetoption_wrap(int a1,  float a2);
DLLEXPORT ENsetstatusreport_wrap(int a1);
DLLEXPORT ENsetqualtype_wrap(int a1,  char * a2,  char * a3,  char *a4) ;
DLLEXPORT ENsetemitter_wrap(float a1, float a2);
DLLEXPORT ENgetemitter_wrap(float *a1, float *a2);

/* Call this function to write a note to the epanet2 report file */
extern int  write_sign(string str);
extern long getcurrenttime();


extern int run_before_ENopen();
extern int run_before_ENsaveinpfile();
extern int run_before_ENclose();
extern int run_before_ENsaveH();
extern int run_before_ENinitH();
extern int run_before_ENrunH ();
extern int run_before_ENnextH ();
extern int run_before_ENnextH();
extern int run_before_ENcloseH();
extern int run_before_ENsavehydfile();
extern int run_before_ENusehydfile();
extern int run_before_ENsolveQ();
extern int run_before_ENopenQ();
extern int run_before_ENinitQ();
extern int run_before_ENrunQ();
extern int run_before_ENnextQ();
extern int run_before_ENstepQ();
extern int run_before_ENcloseQ();
extern int run_before_ENwriteline();
extern int run_before_ENreport();
extern int run_before_ENresetreport();
extern int run_before_ENsetreport();
extern int run_before_ENgetcontrol();
extern int run_before_ENgetcount();
extern int run_before_ENgetoption();
extern int run_before_ENgettimeparam();
extern int run_before_ENgetflowunits();
extern int run_before_ENgetpatternindex();
extern int run_before_ENgetpatternid();
extern int run_before_ENgetpatternlen();
extern int run_before_ENgetpatternvalue();
extern int run_before_ENgetqualtype();
extern int run_before_ENgeterror();
extern int run_before_ENgetnodeindex();
extern int run_before_ENgetnodeid();
extern int run_before_ENgetnodetype();
extern int run_before_ENgetnodevalue();
extern int run_before_ENgetlinkindex();
extern int run_before_ENgetlinkid();
extern int run_before_ENgetlinktype();
extern int run_before_ENgetlinknodes();
extern int run_before_ENgetlinkvalue();
extern int run_before_ENgetversion();
extern int run_before_ENsetcontrol();
extern int run_before_ENsetnodevalue();
extern int run_before_ENsetlinkvalue();
extern int run_before_ENaddpattern();
extern int run_before_ENsetpattern();
extern int run_before_ENsetpatternvalue();
extern int run_before_ENsettimeparam();
extern int run_before_ENsetoption();
extern int run_before_ENsetstatusreport();
extern int run_before_ENsetqualtype();
	int run_before_ENopenH();
	int run_before_ENrunH ();

	void getEmitterData(float *eexp_, float *ecup_);
	void setEmitterData(float eexp_, float ecup_);


#endif