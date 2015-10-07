/* modify epanet2.h file as: 
1. Undefine __win32__ and WINDOWS 
2. for all output parameters, give the name value */
%module epanet2
 %include "typemaps.i"
 %include "cstring.i"
 /* read http://www.swig.org/Doc1.3/Arguments.html */
 %apply int *OUTPUT { int *result };
 %apply int *OUTPUT { int *result1 };
 %apply int *OUTPUT { int *result2 };
 %apply long *OUTPUT { long *result };
 %apply float *OUTPUT { float *result };
 %apply double *OUTPUT { double *result };
 %cstring_bounded_output(char *result,   1024);
 %{
 /* Includes the header in the wrapper code */
 #include "./epanet/epanet2.h"
 %}
 
 /* Parse the header file to generate wrappers */
 %include "./epanet/epanet2.h"
