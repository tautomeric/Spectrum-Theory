# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 17:23:16 2019

@author: Thomas
"""
import spectral as s
class uneven_spec(s.spectrum):
    def __init__(self,a,b,q=lambda x:x,pen_mode=False):
        
        if pen_mode:
            if q(a)!=q(0):
                raise ValueError("Improper a value")
        self.a = a
        self.b = b
        
        self.spectrum = []
        self.spectrum_skeleton = {}
        
        start = a
        i = 0
        while start <= b:
            self.spectrum.append(start)
            self.spectrum_skeleton.update({start:start})
            i+=1
            start += q(i)
        
        if pen_mode:
            if q(b)!=q(i):
                raise ValueError("Improper b value")
        
