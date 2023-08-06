from cffi import FFI
import os
import platform
import sys
ffibuilder = FFI()


ffibuilder.cdef(open("../raylib_modified.h").read().replace('RLAPI ', ''))


ffibuilder.set_source("_raylib_cffi",
                      """
                           #include "../raylib.h"   // the C header of the library, supplied by us here
                      """
                      )

# Hack to produce static linked lib using static librarylib.a supplied by us
version = sys.implementation.cache_tag
if version == 'cpython-36' or version == 'cpython-37':
    version += 'm'
command = "clang -bundle -undefined dynamic_lookup ./_raylib_cffi.o -L/usr/local/lib -L/usr/local/opt/openssl/lib -L/usr/local/opt/sqlite/lib ../../libraylib_mac.a -F/System/Library/Frameworks -framework OpenGL -framework Cocoa -framework IOKit -framework CoreFoundation -framework CoreVideo -o ./_raylib_cffi."+version+"-darwin.so"

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
    if platform.system()=="Darwin":
        print(command)
        os.system(command)
