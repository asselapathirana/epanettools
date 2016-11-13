/****************************************************************************
*** EPANET-Emitter reference application
*** Author: Assela Pathirana    2016Nov
*** Calling function main.cc
*** *************************************************************************
*** Modification history:
*** Name           Date     Description 
*****************************************************************************/

#include <adfandenergycalc.h>
#include <iostream>
#include <cstdlib>
using namespace std;

void pause();
void help(char *);
void readargs(char** argv, char* &inpfile, char* &outfile, float &diafactor );

int main(int argc, char **argv){
	if(argc<4){
		help(argv[0]);
		exit(1);
	}
	char* inpfile;
	char* outfile;
	float diafactor;
	readargs(argv,inpfile, outfile, diafactor );
	ADF_calculation(inpfile, outfile, diafactor);
	pause();

}

void help(char *myname){
	cerr<< "\nUsage: "<<myname<<" <inf>  <outf> <diafactor,e.g. 10,5..> \n\n";
	cerr<< "inf - input EPANET file (in *.inp format).\n";
	cerr << "outf - file to write results.";
	cerr << "Press ENTER..\n";
	cin.get();
}

void pause()
{
	cerr << "Press ENTER..\n";
	cin.get();
}

void readargs( char ** argv, char* &inpfile, char * &outfile,float& diafactor)
{
	inpfile=(argv[1]);
	outfile = (argv[2]);
	diafactor = (float)atof(argv[3]);

	cerr << "\nRunning the case with following parameters\n";
	cerr << "(input file,ECUP, EEXP)=";
	//cerr  << "("<<inpfile<<", "<<ECUP <<", " << EEXP << ")\n";
}
