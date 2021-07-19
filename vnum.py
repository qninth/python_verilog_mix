# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 23:52:44 2021

@author: q
"""
from functools import reduce
class Vnum():
    def __init__(self, bits, num):
        assert bits > 0
        self.bits = bits
        self.num = num
        self.w = 0
        
    def parseSlice(self,slc):
        pass
    
    def __setitem__(self,key,value):
        s = f'{self.num:0{self.bits}b}'
        s[key] = value
        self.num = int(s, 2)
    
    def __getitem__(self, key):
        if isinstance(key, int):
            self.w = 1;
            if key >= self.bits or key < -self.bits:
                raise(IndexError("Vnum index out of range"))
            else :
                if key >= 0:
                    return self.num & (2**key)
                else :
                    return self.num & (2**(key + self.bits))
                
        if isinstance(key, slice):
            def bitAnd (t, x): 
                return t + (self.num & (2**x))

            if key.stop == None and key.step == None:
                self.w = key.start+1;
                if key.start >= self.bits or key.start < -self.bits:
                    raise(IndexError("Vnum index out of range"))
                if key.start >= 0:
                    return reduce(bitAnd, range(0, key.start+1), 0) // (2**0)
                else :
                    return reduce(bitAnd, range(key.start + self.bits, self.bits), 0) // (2**(key.start + self.bits))
            elif key.start > key.stop and key.step == None:
                self.w = key.start-key.stop+1;
                if key.start > self.bits or key.stop < 0:
                    raise(IndexError("Vnum index out of range"))
                return reduce(bitAnd, range(key.stop, key.start + 1), 0) // (2**key.stop)
            elif key.start == key.stop and key.step == None:
                return self[key.start]
            elif key.step == None :
                self.w = key.stop-key.start+1;
                if key.stop >= self.bits or key.start < 0:
                    raise(IndexError("Vnum index out of range"))
                return reduce(bitAnd, range(key.start, key.stop + 1), 0) // (2**key.start)
            else:
                return reduce(bitAnd, range(key.start, key.stop + 1, key.step), 0) // (2**key.start)
            
        if isinstance(key, list):
            s = ''
            for k in key:
                n = self[k]
                w = self.w
                s += f'{n:0{w}b}'
            return int(s, 2)
                

v = Vnum(8, 5)

# 7:0 5
# 00000101

# int
print(v[-1]) # 0
print(v[0]) # 1
print(v[1]) # 0
# print(v[8]) # index error

# slice
print(v[7:]) # [7:0] 00000101
print(v[-1:]) # [-1:0] 0
print(v[-7:]) # 0000010
print(v[-8:]) # 00000101

print(v[2:0]) # 101
print(v[2:1]) # 10

print(v[1:4]) # 0010
