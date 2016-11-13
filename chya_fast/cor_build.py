from cffi import FFI
ffi = FFI()

ffi.set_source("_cor",
               """
                    #include <sys/types.h>
                    #include "cor.h"
               """,
               libraries=[])

ffi.cdef("""int cor(int a, double* b, int n);
            int cor2(int r, double* x, double* y, int n);
            int cor3(int r, double* x, double* y, double* z, int n);
         """)

if __name__ == "__main__":
    ffi.compile(verbose=True)
