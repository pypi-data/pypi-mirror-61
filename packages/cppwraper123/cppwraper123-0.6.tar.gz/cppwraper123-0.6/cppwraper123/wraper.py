import ctypes as c
import os
import sys
#C++
#int sum(int arg1, int arg2)
#void ref(int arg1, int arg2, int* res)
#void mult_array(int* arg1, int k, int len, int* res)

import pathlib


class dllwraper:

    def __init__(self):
        path = str(pathlib.Path(__file__).parent.absolute()) + "\CppDll.dll"
        print("dll path = " + path)
        self.dll = c.CDLL(path)


    def sum(self, x, y):
        return self.dll.sum(x,y)

    def ref(self, val):
        v = c.c_int(val)
        self.dll.ref(c.byref(v))       
        return v.value

    def mult_array(self, vector, k):
        l  = len(vector)
        v = (c.c_int * l)(*vector)
        res = (c.c_int * l)()
        self.dll.mult_array(v, k, l, res)       
        return list(res)
