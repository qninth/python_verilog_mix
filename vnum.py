# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 23:52:44 2021

@author: q
"""

class Vnum():
    def __init__(self, bits, num):
        assert bits > 0
        self.bits = bits
        self.num = num
        
    def parseSlice(self,slc):
        pass
    
    def __setitem__(self,key,value):
        s = f'{self.num:0{self.bits}b}'
        s[key] = value
        self.num = int(s, 2)
    
    def __getitem__(self, key):
        bits = self.bits - 1
        s = f'{self.num:0{self.bits}b}'
        if isinstance(key, int):
            if key >= bits or key < -bits:
                raise(IndexError("Vnum index out of range"))
            elif key >= 0:
                return s[bits - key]
            else :
                return s[ -key-1 ]
        if isinstance(key, slice):
            if key.stop == None and key.step == None:
                return s[slice(bits - key.start, key.stop, 1)]
            elif key.start > key.stop and key.step == None:
                if key.start > bits or key.stop < 0:
                    raise(IndexError("Vnum index out of range"))
                return s[slice(bits - key.start, bits - key.stop, 1)]
            else :
                return s[slice(bits - key.start, bits - key.stop, -1)]


v = Vnum(8, 5)

# 7:0 5
# 00000101

print(v[-1]) # 0
print(v[0]) # 1
print(v[1]) # 0
# print(v[8]) # index error
print(v[2:0]) # 10
print(v[1:4]) # 010
print(v[7:]) # 00000101

