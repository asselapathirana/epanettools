/****************************************************************************
*** EPANET-Emitter reference application
*** Author: Assela Pathirana    2016Nov
*** Routines: entry point : ADF_and_energy_calculation
*** *************************************************************************
*** Modification history:
*** Name           Date     Description 
*****************************************************************************/
#include <callepanet.h>
#include <epanet2.h>
#include <wrapper.h>

void getValuesForNode(int ii, int jj, vector<vector <pr> > &results, bool emitter) 
/** reads the results from epanet system for the current calculation step and stores in the vector results
arguments: 
		jj, ii  - locations of results vector the values should be stored. 
		results - the results vector
		emitter - whether we are in the middle of an emitter based analysis (True)
**/
{
	pr tmp2;
	float val;
	results.at(jj).push_back(tmp2);
	eoutcheck(emitter?ENgetnodevalue_wrap(jj, EN_PRESSURE, &val):ENgetnodevalue(jj, EN_PRESSURE, &val));
	results.at(jj).at(ii).p=val;
	eoutcheck(emitter?ENgetnodevalue_wrap(jj, EN_DEMAND, &val):ENgetnodevalue(jj, EN_DEMAND, &val));
	results.at(jj).at(ii).d=val;
	eoutcheck(emitter?ENgetnodevalue_wrap(jj, EN_HEAD, &val):ENgetnodevalue(jj, EN_HEAD, &val));
	results.at(jj).at(ii).head=val;
	int ty;
	eoutcheck(ENgetnodetype(jj,&ty));
	results.at(jj).at(ii).type=ty;
}

void ADF_calculation(char * _inpfile, char * outfile, float _DIAFACTOR)
/** Computes the ADF calculation of the given network file
arguments:
	_inpfile	:	name of the epanet .inp file

*/
{
	DIAFACTOR = _DIAFACTOR;
	inpfile=new char[500];
	char ResultsFileName[500];
	strcpy(inpfile,_inpfile);
	strcpy(ResultsFileName,outfile);
	//strcat(ResultsFileName,RESULTFILEEXTENSION);
	init(ResultsFileName); // , open the output file
	initLinkArray(); // store the number of links and nodes in global variables. 
	BaselineCalc();
	costCalc();
	ResultsFile.close();
}

void BaselineCalc()
/** Does the epanet simulation without any pipes closed (normal operation), with and without emitter modification. 
emitterbaseline and emitterbaseline are the two vectors holding results for emitter, no-emitter simulations respectively
arguments:
	none
**/
{
	open(true);
	emitterbaseline=getResults(true);
	close(true);
	open(false);
	regularbaseline=getResults(false);
	close(false);
}


void writeoutputforpipe( int ii, res &r ) 
/** Writes the output to stdout and the file opened at 'ResultsFile' if possible. 
arguments:
	ii	:	pipe index
	r	:	struct res containing the results
*/
{
	/* cout.precision(3);
	cout << setw(3) << ii<<
		'\t'<<linkid(ii).c_str()<<
		fixed <<
		'\t'<<r.adf1<<
		'\t'<<r.adf2<<
		scientific <<
		'\t'<<r.energy_in<<
		'\t'<<r.energy_out<< 
		'\n'; */
	if(ResultsFile.is_open()){
		ResultsFile << setw(3)<< ii<<
			fixed << 
			'\t'<<linkid(ii).c_str()<<
			'\t'<<r.adf1<<
			/*'\t'<<r.adf2<<
			scientific <<
			'\t'<<r.energy_in<<
			'\t'<<r.energy_out<<*/
			'\n';
	}
	cout << fixed << setw(3);
	ResultsFile << fixed << setw(3);
}


void costCalc()
/** Closes each link and calculates nodal values of pressure, demend, and writes results.
arguments:
	none
**/
{
	//cout << "LINK#\tLNKID\tSIGNF\n";
	for (unsigned int ii=1;ii<linksOfNetwork.size();ii++){
		res r=without_link(ii);
		writeoutputforpipe(ii, r);
	}
}

void InitiateLogFile() 
/** 
Strats a fresh log file, which will be used to redirect stdout, so that the user will not be 
overwhelmed by pages and pages of console output. 
arguments:
	none
**/
{
	FILE * pFile=fopen(LOGFILENAME,"w");
	char dateStr [9];
	char timeStr [9];

	time_t rawtime;
        struct tm * timeinfo;
	char buffer [80];

        time (&rawtime);
        timeinfo = localtime (&rawtime);

        strftime (buffer,80," %I:%M%p.",timeinfo);

	fputs ("Date-Time",pFile);
	fputs (buffer,pFile);
	fputs ("\n",pFile);
	fclose(pFile);
}

void OpenOutputFile(char* file) 
/** Opens the file given in the aguments at the stream ResultsFile
arguments:
	file	:	filename
**/
{
	ResultsFile.open(file);
	if(!ResultsFile.is_open()){
		cerr << "warning: Unable to open output file ";
	}
}

void init(char* file)
/** Initializes the files needed to write output to
arguments:
	file	:	argument directed passed to OpenOutputFile function 
**/
{
	OpenOutputFile(file);
	InitiateLogFile();
}

string linkid(int ind)
/** retuns the id of link with index given by the argument
arguments:
	ind	:	link index
**/
{
	return linksOfNetwork.at(ind);
}

float diam(int ind)
/** retunrs the diameter of link with index given by the argument
	ind	:	link index
**/
{
	float out;
	eoutcheck(ENgetlinkvalue(ind,EN_DIAMETER,&out));
	return out;
}

float length(int ind)
/** retunrs the length of link with index given by the argument
	ind	:	link index
**/
{
	float out;
	eoutcheck(ENgetlinkvalue(ind,EN_LENGTH,&out));
	return out;
}

res without_link(int li)
/** Closes the link with given index and calls getResults function and resets the closed link back to normal
arguments:
	li	:	link index
*/
{
	open(true);
	float dia;
	eoutcheck(ENgetlinkvalue(li,EN_DIAMETER,&dia));
	eoutcheck(ENsetlinkvalue(li,EN_DIAMETER,dia/DIAFACTOR));
	//
	//now get the results. 
	vector<vector<pr> > results=getResults(true);

	// reset the pipe
	eoutcheck(ENsetlinkvalue(li,EN_DIAMETER,dia));
	close(true);

	return compute_results(results,emitterbaseline,regularbaseline);
}

void open(bool emitter)
/** Opens the epanet system, opens hydraulics for emitter/non-emitter analysis
arguments:
	emitter	:	whether doing emitter-based analysis
**/
{
	char outputfile[1024];
	strcpy(outputfile,inpfile);
	strcat(outputfile,EN_REPORTFILEEXTENSION);
	eoutcheck(emitter?
		ENopen_wrap(inpfile, outputfile, EN_BINARYOUTFILENAME)
		:
		ENopen(inpfile, outputfile, EN_BINARYOUTFILENAME)
			);
	eoutcheck(emitter?ENopenH_wrap():ENopenH());  
}

void close(bool emitter)
/** Closes the epanet system after closing hydraulics of an emitter/non-emitter analysis
arguments:
	emitter	:	whether doing emitter-based analysis
**/
{
	eoutcheck(emitter?ENcloseH_wrap():ENcloseH());
	eoutcheck(emitter?ENclose_wrap():ENclose());
}


void initLinkArray()
/** Reads the number of links in the currently opened network and creates the vector of link ids (linksOfNetwork)
arguments:
	none
**/
{
	open(false);
	int NLINKS;
	ENgetcount(EN_LINKCOUNT,&NLINKS);
	linksOfNetwork.clear(); //BUG FIX 2016NOV13
	linksOfNetwork.push_back(DUMBSTRING);
	for(int i=1;i<=NLINKS;i++){
		char id[50];
		eoutcheck(ENgetlinkid(i,id));
		linksOfNetwork.push_back(id);
	}
	close(false);
}



res compute_results(vector<vector< pr > >r, vector<vector< pr > >emt, vector<vector< pr > > nem )
/** Computes the ADF and energy results and returns as a type res
arguments:
	r	:	results vector for which ADF and energy are calculated. 
	emt	:	results vector from emitter based baseline calculation (corressponding adf res.adf1)
	nem	:	results vector from non-emitter based baseline calculation (corressponding adf res.adf2)
**/
{
	res result;
	float sum1=0, sum2=0;
	result.adf1=result.adf2=result.energy_in=result.energy_out=0.f;
	for(unsigned int i=1;i<r.size();i++){
		for(unsigned int j=1;j<r.at(i).size();j++){

			if(r.at(i).at(j).type==EN_JUNCTION){
				result.energy_out+=r.at(i).at(j).head*r.at(i).at(j).d;
				result.adf1+=r.at(i).at(j).d;
				sum1+=emt.at(i).at(j).d;
				sum2+=nem.at(i).at(j).d;
				//cout << r.at(linkindex).at(j).d << "\t" << emt.at(linkindex).at(j).d << "\t" << 
				//	nem.at(linkindex).at(j).d << endl;
			}else{
				result.energy_in-=r.at(i).at(j).head*r.at(i).at(j).d;
			}			

		}
	}
	result.adf1=result.adf1/sum1;
	result.adf2=result.adf1/sum2; /// yes! this is NOT a mistake it should be adf1/sum2 !!
	return result;
}

void fillinemptyresultsobject( vector<vector< pr> > &results ) 
/** Reads the number of nodes of the currently opened network and create the results vector to take up nodal values at each time step later 
arguments: 
	results : reference of the result vector to be used 
**/
{
	vector<pr> tmp;
	results.push_back(tmp); //dumb
	int NNODES;
	ENgetcount(EN_NODECOUNT,&NNODES);
	for(int jj=1;jj<=NNODES;jj++){
		pr tmp2;
		results.push_back(tmp);
		results.at(jj).push_back(tmp2);
	}
}

void setNaN( vector<vector< pr> > &results ) 
/** Sets all the values of a result object to NaN. 
arguments: 
	results : reference of the result vector to be used 
**/
{
	for(unsigned int i=1;i<results.size();i++){
		for(unsigned int j=1;j<results.at(1).size();j++){
			results.at(i).at(j).p=std::numeric_limits<float>::signaling_NaN();
			results.at(i).at(j).d=std::numeric_limits<float>::signaling_NaN();

		}
	}
}


vector<vector< pr> > getResults(bool emitter)
/** runs an analysis with the current input file  and reads demands, and pressures 
Epanet system should be opened (ENopen/_wrap), but initialization would be done inside this function. 
arguments:
	emitter	:	whether to do emitter analysis
**/
{

	ReDirectStdout(true);

	vector<vector< pr> > results;
	long tt;
	epanet_error=false;
	eoutcheck(emitter?ENinitH_wrap(0):ENinitH(0));
	fillinemptyresultsobject(results);
	int ii=0;
	long timestep;
	eoutcheck(emitter?ENgettimeparam_wrap(EN_REPORTSTEP,&timestep):ENgettimeparam(EN_REPORTSTEP,&timestep));
	do{
		eoutcheck(emitter?ENrunH_wrap(&tt):ENrunH(&tt));
		if(tt%timestep==0){
			ii++;
			for(unsigned int jj=1;jj<results.size();jj++){	
				getValuesForNode(ii,jj,results, emitter);

			}
		}
		eoutcheck(emitter?ENnextH_wrap(&tt):ENnextH(&tt));
	}while (tt > 0);  	
	if(epanet_error){
		//setNaN(results);

	}
	ReDirectStdout(false);
	return results;

}


void eoutcheck(int ret)
/** Check the value of argument against epanet error/warning signalling system. 
If there is an error, or some critical warnings, the flag epanet_error (global) 
is set to true, signalling the problem. 
arguments:
	ret	:	value to be checked
**/
{
	//check ret against standard epanet signals and raise hell if anything is wrong
	if(ret>0){
		char enerr[500];
		ENgeterror(ret,enerr,499);
		if(epanet_error){ return;}
		if(ret>100){
			cerr << "Error in epanet..\n" <<ret<<" returned.\n";
			cerr << "Error : " << enerr << endl;
			epanet_error=true;
		}
		if(ret==1 || ret==2){ // these are problems that prevent us from getting reliable answers. 
			cerr << "Warning from epanet..\n" <<ret<<" returned.\n";
			cerr << "Warning : " << enerr << endl;
			epanet_error=true;
		}
		cerr.flush();
	}

}

void ReDirectStdout(bool d)
/** Redirects/undo redirect the stdout to LOGFILENAME
	d	:	if true/false redirection is done/undone. 
**/
{
	

	if(d){
		/* duplicate stdout */
		stdout_dupfd = _DUP_(1);
	    
		temp_out = fopen(LOGFILENAME, "w");
		fflush(stdout);
		/* replace stdout with our output fd */
		_DUP2_(_FILENO_(temp_out), 1);
	}else{

		/* flush output so it goes to our file */
		fflush(stdout);
		fclose(temp_out);
		/* Now restore stdout */
		_DUP2_(stdout_dupfd, 1);
		_CLOSE_(stdout_dupfd);

			    
		    }
	
}
 


/********************************************************************************/
