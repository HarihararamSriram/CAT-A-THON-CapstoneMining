import pandas as pd
import numpy as np
df = pd.read_excel(r'CAT_Training_Dataset_V3 File.xlsx')
candidate = "ABCDE00002"
event = "Component2_discreteSensorH_Up"

# Data cleaning
df_interested = df[df["event"]==event].copy() #It contains the event Component2_discreteSensorH_Up
# Clear errors and then we need to sort it according to the chronological order (date column)
df_interested.drop(columns=["ID",], inplace=True)
#print(df_interested)
df_interested.drop_duplicates(inplace=True)
df_interested = df_interested[df_interested.date.apply(lambda x: str(x).isnumeric())].copy()
#print(df_interested)
df_interested = df_interested[df_interested.occur_count.apply(lambda x: int(x)>0)].copy()
#print(df_interested)
df_interested = df_interested[df_interested.candidate.apply(lambda x: x==candidate)].copy()
df_interested.reset_index(inplace=True, drop=True)
'''
print(df_interested)
print(df_interested.describe())
'''

maxvalues = list()
sevlist, sevandindlist = list(), list()
Y = df_interested['units'].tolist()
X = df_interested['date'].tolist()
z = df_interested['occur_count'].tolist()
for i in range(len(z)):
    Y[i]=Y[i]*z[i]
max_unit = max(Y)
for i in range(len(Y)):
    if(Y[i]==max_unit):
        maxvalues.append(int(i))
for j in maxvalues:
    sevandindlist.append([j, int(df_interested["svrty_level"].iloc[j])])
    sevlist.append(int(df_interested["svrty_level"].iloc[j]))
max_sev = max(sevlist)
all_sevlist = df_interested["svrty_level"].tolist()
cur_sev = all_sevlist[len(all_sevlist)-1] # The current severity level
X, Y = np.array(X), np.array(Y)



indofsev = sevandindlist[sevlist.index(max_sev)][0] 
if(max_sev==1):
    Y_threshold = Y[indofsev]*1.15 #15%
elif(max_sev==2):
    Y_threshold = Y[indofsev]*1.30 #30%
else:
    Y_threshold = Y[indofsev]*1.45 #severity level is 3 -> 45%

#Severity level grouping
severitylist = list()
c = list()
for i in range(1,4):
    a = df_interested['units'][df_interested['svrty_level']==i].tolist()
    b = df_interested['occur_count'][df_interested['svrty_level']==i].tolist()
    if(len(a)!=0):
        for i in range(len(a)):
            c.append(a[i]*b[i])
        severitylist.append(c)
    else:
        severitylist.append(a)


s3 = 0
check = 0

if(len(severitylist[0])!=0 and len(severitylist[1])!=0 and len(severitylist[2])!=0):
    s1 = ( min(severitylist[0]) + max(severitylist[1]) )/2
    s2 = ( min(severitylist[1]) + max(severitylist[2]) )/2
elif(len(severitylist[0])==0 and len(severitylist[1])!=0 and len(severitylist[2])!=0):
    s1 = max(severitylist[1])
    s2 = ( min(severitylist[1]) + max(severitylist[2]) )/2
elif(len(severitylist[0])!=0 and len(severitylist[1])==0 and len(severitylist[2])!=0):
    s1 = min(severitylist[0])
    s2 = max(severitylist[2])
elif(len(severitylist[0])==0 and len(severitylist[1])==0 and len(severitylist[2])!=0):
    s2 = max(severitylist[2])
    s1 = 2*s2
elif(len(severitylist[0])!=0 and len(severitylist[1])!=0 and len(severitylist[2])==0):
    s1 = ( min(severitylist[0]) + max(severitylist[1]) )/2
    s2 = min(severitylist[1])
elif(len(severitylist[0])==0 and len(severitylist[1])!=0 and len(severitylist[2])==0):
    s2 = min(severitylist[1])
    s1 = max(severitylist[1])
elif(len(severitylist[0])!=0 and len(severitylist[1])==0 and len(severitylist[2])==0):
    s1 = min(severitylist[0])
    s2 = s1/2

