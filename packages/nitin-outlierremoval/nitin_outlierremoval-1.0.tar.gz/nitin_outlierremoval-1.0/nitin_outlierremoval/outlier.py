# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 00:08:30 2020

@author: Dell
"""

import pandas as pd
import numpy as np
import math 
import sys

def outlierremover(dataset,outputdataset):
    dataset=pd.DataFrame(dataset)
    rows=dataset.shape[0]
    columns=dataset.shape[1]
    
    columnlist=list(dataset.columns)
    
    for i in range(columns):
        
        dataset=dataset.sort_values(by=columnlist[i]) #sorting the data values by columns
        dataset=dataset.reset_index(drop=True)
        dataset.index=np.arange(1,len(dataset)+1)
        z=dataset.iloc[:i].values 
        
        rows=dataset.shape[0]
        columns=dataset.shape[1]
        
        
        floor1 = math.floor((rows+1)/4)
        floor2 = math.floor(3*(rows+1)/4)
        ceil1 = math.ceil((rows+1)/4)
        ceil2 = math.ceil(3*(rows+1)/4)
        
        
        #calculating the values of quantiles 
        Quantile1 = (z[floor1] + z[ceil1])/2 
        Quantile3 = (z[floor2] + z[ceil2]) / 2 
        
        #calculating interquamtile range 
        IQR = Quantile3 - Quantile1
        
        #finding minimum and maximum bounds 
        minimum = Quantile1 - 1.5 * IQR
        maximum = Quantile3 + 1.5 * IQR
        
        
        #removing outliers from the data 
        dataset = dataset[dataset[columnlist[i]] > minimum] #for minimum 
        dataset = dataset[dataset[columnlist[i]] < maximum] #for maximum
        dataset.index = np.arange(1,len(dataset)+1)
        
    #putting the new dataset into the outputdataset 
    dataset.to_csv(outputdataset, header = False, index=False)
    

def main():
    dataset = pd.read_csv(sys.argv[1]).values
    outputdataset = sys.argv[2]
    outlierremover(dataset,outputdataset)

if __name__=="__main__":
    main()
        
        


