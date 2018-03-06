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
temp = []
while i<length :
    j= i+1
    while j <length:
        if dob[i]==dob[j] and gender[i]==gender[j]:
            score = similarity_evalutation.similarity(fullName[i],fullName[j])
            print(fullName[i],fullName[j],"has score: ",score)
            if score>0.2:
                temp.append(j)
        j+=1
    i+=1
            
                
fName_ = []
lName_ = []
dob_ = []
gender_ = []
for i in range(len(fName)):
    if i not in temp:
        fName_.append(fName[i])
        lName_.append(lName[i])
        dob_.append(dob[i])
        gender_.append(gender[i])
        
output = pd.DataFrame({'ln':lName_,'dob':dob_,'gn':gender_,'fn':fName_})
output.to_csv("Output.csv")