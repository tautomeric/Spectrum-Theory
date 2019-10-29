# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 17:41:57 2019
@author: Thomas
"""
import numpy as np
import choas
class spectrum:
    def __init__(self,a=0,b=0,q=0):
         
         difference_factor = (b-a)/q
         if difference_factor - int(difference_factor) > .00000000001:
             raise ValueError("Invalid values for spectrum")
         
         self.a = a
         self.b = b
         self.q = q
         self.spectrum = []
         self.spectrum_skeleton = {}
        
         start = a
         while start <= b:
            self.spectrum.append(start)
            self.spectrum_skeleton.update({start:start})
            start = start + q
         
    #returns the number of values in a set of numbers for each possible list ceiling    
    def list_ceiling(self,data=np.array([0],dtype=np.int8)):
       
        end = np.size(data) 
        locale = 0
        while locale<end:
            check = data[locale]
            
            if(check<self.a or check >self.b ):
                data = np.delete(data,locale)
                end = end - 1
            else:
                locale = locale + 1
       
        
        list_ceiling = choas.catorgories(self.spectrum_skeleton)
        processed = data
        return list_ceiling.catagorize(processed) 
   
    #returns the number of values in a set of numbers for each possible list ceiling  
    def list_floor(self,data=np.array([0],dtype=np.int8)):
        end = np.size(data) 
        locale = 0
        while locale<end:
            check = data[locale]
            
            if(check<self.a or check >self.b ):
                data = np.delete(data,locale)
                end = end - 1
            else:
                locale = locale + 1
        
        negative_clone = self.spectrum_skeleton.copy()
        negative_clone = sorted(negative_clone,reverse=True)
        
        inverse_skeleton={}
        for i in negative_clone:
            inverse_skeleton.update({i:-i})
        
        negative_data = []
        iters = np.size(data)
        
        for i in range(iters):
           negative_data.append(-data[i])
            
        list_floor = choas.catorgories(inverse_skeleton)
        return list_floor.catagorize(negative_data)
        
    #returns the quantium floor of a number for the spectrum
    def spectrum_floor(self,n):
        if self.a <= n<=self.b:
            left_side = 0
            right_side = len(self.spectrum) - 1
            m = int((left_side + right_side) / 2)
            while left_side <= right_side:
                if self.spectrum[m] < n:
                    left_side= m + 1
                elif self.spectrum[m] > n:
                    right_side = m - 1
                else:
                    break
                m = int((left_side + right_side) / 2)
            
            return self.spectrum[m]
        else:
            return None
       
     #returns the quantium ceiling of a number for a spectrum   
    def spectrum_ceiling(self,n):
      
        if self.a <= n<=self.b:
            for i in self.spectrum:
                if(i>=n):
                  return i  
        else:
            return None
     #returns where in an overloaded spectrum a value is, raises an error if the
     #value is not on the spectrum      
    def overload(self,n):
        if n in self.spectrum:
            return n
        elif n>self.b:
            if abs(n-self.b)%self.q==0:
                return "n"+str(int((n-self.b)/self.q))
            else:
                raise ValueError("Undefined Value")
        elif n<self.a:
            if abs(self.a-n)%self.q==0:
                return "n-"+str(int((self.a-n)/self.q))
            else:
                raise ValueError("Undefined Value")
        else:
            raise ValueError("Undefined Value")
    
    def reset_spectra(self,spectrum = [0,1,5]):
        spectrum.sort()
        self.spectrum = spectrum
        new_skeleton = {}
        
        for i in spectrum:
            new_skeleton.update({i:i})
        self.spectrum_skeleton = new_skeleton
    
    def addition(self, other):
        s_3 = spectrum(1,1,1)
        s_3.reset_spectra(sorted(set(self.spectrum)|set(other.spectrum)))
        return s_3
    
    def subtraction(self,other):
       s_3 = spectrum(1,1,1)
       s_3.reset_spectra(sorted(set(self.spectrum)^set(other.spectrum)))
       return s_3
        
#allows for processing a set of overlayed spectrums          
class overlay: 
    #define spectrums in order of the most independent to least
    def __init__(self,spectra=[spectrum(0,10,2),[0,10,2]]):
        self.spectra = []
        for i in range(len(spectra)):
            if type(spectrum(0,10,2))==type(spectra[i]):
                self.spectra.append(spectra[i])
            elif type([]) == type(spectra[i]):
                appender = spectra[i]
                self.spectra.append(spectrum(appender[0],appender[1],appender[2]))
            else:
                raise TypeError("Only type list or spectrum")
        
        self.locations = [[] for _ in range(len(spectra))]
            
    def set_ranges(self,new_ranges=[[0, 2], [5, 9]]):
        self.ranges = np.array(new_ranges)
    
    #first value in each list notes the spectrum, second the location on the spectrum
    def set_locations(self,location=[[0,8]]):
        for i in range(len(location)):
            locale,spectra = location[i][1],location[i][0]
            
            self.locations[spectra]= np.array(locale)
            
    def defined_spectra(self,spectra=0,all_spectra_mode=False):
        if(not all_spectra_mode):
            is_defined = True
            
            spectra = spectra-1
            while spectra>=0:
                location = self.locations[spectra]
                if not location:
                    raise TypeError("First set the locations the values are at")
                
                ranges = self.ranges[spectra]
                
                if not (ranges[0]<= location <= ranges[1]):
                    is_defined = False
                    break
                spectra = spectra-1
            return is_defined
        
        else:
            spectra = 1
            total_iters = len(self.spectra)-1
            
            spectra_defined = [True]
            while total_iters>=spectra:
                location = self.locations[spectra-1]
                if not location:
                    raise TypeError("First note the locations the values are at on the spectrum")
                
                ranges = self.ranges[spectra]
                if not (ranges[0]<= location <= ranges[1]):
                    break
                
                spectra_defined.append(True)
                spectra = spectra + 1
                
            while total_iters >= spectra:
                spectra_defined.append(False)
                spectra = spectra + 1
             
            return np.array(spectra_defined)


