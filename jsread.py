from ctypes import *

def jsread(lib, path, callback, _verbose = False):

    if _verbose:
        verbose = 1
    else:
        verbose = 0

    def converter(a_count, a, b_count, b):

        axes = []
        for i in range(0, a_count):
            axes.append(a[i])

        buttons = []
        for i in range(0, b_count):
            buttons.append(b[i])

        callback(axes, buttons)

        return 0

    jsread = cdll.LoadLibrary(lib)

    CMPFUNC = CFUNCTYPE(c_int, c_int, POINTER(c_int), c_int, POINTER(c_byte))
    cb = CMPFUNC(converter)

    jsread.jsread(path.encode('utf-8'), cb, verbose)

