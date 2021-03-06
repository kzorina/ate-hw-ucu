#!/usr/bin/env python2
#encoding: UTF-8
import csv
import ate

def read_terms(T_file,skip_lines=1):
    T=[]
    with open(T_file,'r') as csvfile:
        T_reader = csv.reader(csvfile, delimiter=" ", quotechar='"')
        cnt=0
        for row in T_reader:
            cnt+=1
            if cnt>skip_lines:
                term=(row[0], float(row[1]))
                if(term[1]>0):
                    T.append( term )
    return T



T1=read_terms('hands-on/time-onto-paper/terms-c-value.csv')
T2=read_terms('hands-on/time-onto-paper/terms-manual.csv')

print ("T1 - T2",ate.thd(T1, T2))
print ("T2 - T1",ate.thd(T2, T1))

T3=read_terms('hands-on/time-onto-paper/terms-termine.csv',skip_lines=0)
print ("T2 - T3",ate.thd(T2, T3))
