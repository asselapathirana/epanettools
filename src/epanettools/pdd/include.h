#include <string>
#include <vector>
using namespace std;

struct node{
	string id;
	int index;
	float demand; 
	float orig_demand;
	float orig_basedemand;
	float pressure;
	float saved_pressure; 
	float saved_demand;
	float ec;
	bool offender;
};


int emitter_analysis();
int post_analysis_cleanup();
int emitter_analysis_prepare();
void getEmitterData(float *eexp, float *ecup);
int getniter();
