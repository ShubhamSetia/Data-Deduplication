#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 15:48:34 2018

@author: shubham
"""

import similarity_evalutation
import pandas as pd

data = pd.read_csv('Deduplication Problem - Sample Dataset.csv')

fName = []
lName = []
dob = []
gender = []
fullName = []
for index,row in data.iterrows():
    fName.append(row['fn'])
    lName.append(row['ln'])
    dob.append(row['dob'])
    gender.append(row['gn'])
    fullName.append(row['fn']+' ' +row['ln'])
    
length = len(fullName)
i = 0
while i<length :
    j= i+1
    while j <length:
        if dob[i]==dob[j] and gender[i]==gender[j]:
            score = similarity_evalutation.similarity(fullName[i],fullName[j])
            print(fullName[i],fullName[j],"has score: ",score)
            if score>0.2:
                print("Poped",fullName[j])
                fullName.pop(j)
                fName.pop(j)
                lName.pop(j)
                dob.pop(j)
                gender.pop(j)
                length-=1
                
        j+=1
    i+=1
            
                

output = pd.DataFrame({'ln':lName,'dob':dob,'gn':gender,'fn':fName})
output.to_csv("Output.csv")