#ifndef PATCH_H
#define PATCH_H

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


DLLEXPORT ENsetpatterndim(int index, int dim);
DLLEXPORT ENsetpatterndim_wrap(int index, int dim);



#endif