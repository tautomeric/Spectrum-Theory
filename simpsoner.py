# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 09:28:51 2020

@author: Thomas
"""
import spectral as s
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr 

class simpsoner:
    def __init__(self,data=[0,2,3,4,6],splits=[1,3]):
        
        data.sort()
        
        spectra=[]
        correlates=[]
        for i in range(len(splits)):
            spectra.append(s.spectrum(data[0],data[len(data)-1],splits[i]))
          
        self.spectra=spectra
        
        for i in range(len(splits)):
            spectrum=spectra[i]
            appender=[]
            dic=spectrum.list_ceiling(data)
            for j in dic:
                appender.append(dic[j])
            correlates.append(spearmanr(spectrum.spectrum,appender,nan_policy='omit'))
        self.correlates=correlates
        self.data=data
    
    def to_chart(self):
        p_val=[]
        correlations=[]
        spectrums=[]
        
        for i in range(len(self.spectra)):
            p_val.append(self.correlates[i][1])
            correlations.append(self.correlates[i][0])
            spectrums.append(self.spectra[i].spectrum)
        
        chart=pd.DataFrame({'spectra':spectrums,'correlation':correlations,'p-vals':p_val})
        return chart
    
        
    def organizer(self,p_val=.05):
        ordering=[[],[],[]]
        for i in range(len(self.spectra)):
             if self.correlates[i][1]<p_val:
                 if self.correlates[i][1]<0:
                     ordering[0].append(self.spectra[i].spectrum)
                 else:
                    ordering[1].append(self.spectra[i].spectrum)
             else:
                 ordering[2].append(self.spectra[i].spectrum)
                     
        return ordering
