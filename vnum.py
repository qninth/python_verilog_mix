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
        self.width = 0
    
    def rightShift(self, k):
        n, l = self.parseSlice(k)
        return n // (2 ** l)
    
    def parseSlice(self,key):
        if isinstance(key, int):
            self.width = 1
            if key >= self.bits or key < -self.bits:
                raise(IndexError("Vnum index out of range"))
            else :
                if key >= 0:
                    return (self.num & (2**key)), key
                else :
                    return (self.num & (2**(key + self.bits))), key + self.bits
                
        if isinstance(key, slice):
            def bitAnd (t, x): 
                return t + (self.num & (2**x))
            # respectively
            if key.stop == None and key.step == None:
                if key.start >= self.bits or key.start < -self.bits:
                    raise(IndexError("Vnum index out of range"))
                if key.start >= 0:
            # vm[7:]
                    self.width = key.start+1
                    return reduce(bitAnd, range(0, key.start+1), 0), 0
                else :
            # vm[-1:]
                    self.width = -key.start
                    return reduce(bitAnd, range(key.start + self.bits, self.bits), 0), key.start + self.bits
            # vm[4:1]
            elif key.start > key.stop and key.step == None:
                self.width = key.start-key.stop+1;
                if key.start > self.bits or key.stop < 0:
                    raise(IndexError("Vnum index out of range"))
                return reduce(bitAnd, range(key.stop, key.start + 1), 0),key.stop
            # vm[1:1]
            elif key.start == key.stop and key.step == None:
                return self.parseSlice(key.start)
            # vm[1:4]
            elif key.step == None :
                self.width = key.stop-key.start+1;
                if key.stop >= self.bits or key.start < 0:
                    raise(IndexError("Vnum index out of range"))
                slicedNumber = self.rightShift(slice(key.stop, key.start, key.step))
                inversedNumber = int(f'{slicedNumber:0{self.width}b}'[::-1], 2)
                return inversedNumber, 0
            # vm[1:3:1]
            else:
                self.width = (key.stop-key.start+1) // key.step;
                return reduce(bitAnd, range(key.start, key.stop + 1, key.step), 0), key.start
        
        if isinstance(key, tuple):
            s = ''
            w = 0
            for k in key:
                n = self.rightShift(k)
                w += self.width
                s += f'{n:0{self.width}b}'
            self.width = w
            return int(s, 2), 0
    
    def __pow__(self, another):
        num = self.num * 2**another.bits + another.num
        bits = self.bits + another.bits
        return Vnum(bits, num)
    
    def __add__(self):
        pass
    
    def __str__(self):
        return f'Vnum({self.bits},{self.num}) %HEX {self.num:x}'
    
    def __setitem__(self,key,value):
        s = f'{self.num:0{self.bits}b}'
        s[key] = value
        self.num = int(s, 2)
    
    def __getitem__(self, key):
        slicedNumber = self.rightShift(key)
        return Vnum(self.width, slicedNumber)        
                

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

print(v[1:4]) # 0100
print(v[1,2:3]) # 010
print(v[0,2,1,1:2]) # 11010
a1 = v[1]
a2 = v[2]
a3 = v[2]

# print(a1<a2<a3) # 该结果会被解析为下式
# print(a1<a2 and a2<a3) # 该结果打印是最后一个表达式的值，无法实现拼接

print(a1**a2) # 01
print(a2**a3) # 11
print(a1**a2**a3) # 011

class A():
    def __init__(self):
        pass
#想试一下 a = self.b() / self.c
# if c changed in self.b(), a use the previous or the newest?
