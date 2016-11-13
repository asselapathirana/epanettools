#ifndef CALLADF_H
#define CALLADF_H


#define _CRT_SECURE_NO_DEPRECATE // to avoid visual studio screaming 'bloody murder'. 
#include <stdio.h>
#include <epanet2.h>
#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <fstream>
#include <time.h>
#include <iomanip>
#include <cstring>
using namespace std;

/* macros and variables  used by ReDirectStdout function */
//  
#ifdef _WIN32  
#define _CRT_SECURE_NO_WARNINGS 1
#include <io.h>
#define _DUP_ _dup  
#define _DUP2_ _dup2  
#define _CLOSE_ _close 
#define _FILENO_ _fileno
#else
#include <unistd.h>
#define _DUP_ dup  
#define _DUP2_ dup2  
#define fopen_s fopen 
#define _CLOSE_ close 
#define _FILENO_ fileno
#endif
#include <stdlib.h>  
#include <stdio.h>  
#include <iostream>  
int stdout_dupfd;
FILE *temp_out;
/* end macros and variables  used by ReDirectStdout function */


/* Structures */
struct pr {
	float p;
	float d;
	float bd;
	float head;
	int type;
};

struct res {
	float adf1;
	float adf2;
	float energy_in;
	float energy_out;
};
/* end structures */

/* function prototypes */
void eoutcheck(int);
void HydrantRating(char *, int, float[], float[]);
void GetNodeP(int, vector<float>&, int);
float penalty_score(int);
float penalty(float, float);
res without_link(int);
void init(char*);
void costCalc();
void BaselineCalc();
vector<vector<pr> > getResults(bool);
void help(char *);
string linkid(int);
float diam(int);
float length(int);
float pen_s(float, float);
float pen(float, float);
float pen_l(float, float);
void no_objects();
res compute_results(vector<vector< pr > >, vector<vector< pr > >, vector<vector< pr > >);
void open(bool);
void close(bool);
void writeoutputforpipe(int, res &);
void fillinemptyresultsobject(vector<vector< pr> > &);
void getValuesForNode(int, int, vector<vector <pr> > &, bool);
void ReDirectStdout(bool);
void initLinkArray();
/* end fuction prototypes */

/* Global variables used in callepanet.cc */
float ecupValue;
float eexpValue;
ofstream ResultsFile; //output file.
vector<vector<pr> > emitterbaseline;
vector<vector<pr> > regularbaseline;
bool epanet_error = false;
vector<string> linksOfNetwork; // a vector containing the ids of links ordered by index
char* inpfile;
float DIAFACTOR = 5;
/* end of global variables */

/* Constants used in callepanet.cc */
#define LOGFILENAME "log.txt" /* the file we used to redirect stdout when it becomes to much for comfort! */
#define SMALLDIA 0.01f /* negligibly small diameter (in mm or inches) */
#define EN_REPORTFILEEXTENSION ".rpt" /* Extension for the report file of epanet */
#define EN_BINARYOUTFILENAME ""       /* Name of the binary result file. Empty - no binary results */
#define RESULTFILEEXTENSION ".results.txt" /* Extension for the results file*/
#define DUMBSTRING "-1" /* A string that indicates dumb value */
/* end constants */
#endif
