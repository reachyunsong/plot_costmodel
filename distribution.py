import pandas as pd
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import sys
import seaborn as sns
import types

import os
# path = '/'
# files = []
# for i in os.listdir(path):
#     if os.path.isfile(os.path.join(path,i)) and 'n' in i:
#         files.append(i)
# print(files)

def getFileName(path):
    f_list = os.listdir(path)
    # print(f_list)
    filelist = []
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        if os.path.splitext(i)[1] == '.csv' and os.path.splitext(i)[0].startswith('node'):
            filelist.append(i)
    return filelist
# print(getFileName('./'))

input_file = getFileName('./')
# input_file = ['node1.csv','node2.csv','node3.csv','node4.csv']

n=1
for node in input_file:
    df = pd.read_csv(node,sep=";",header=0)
    df = df.fillna(0)
    # print(df)

    def time_convert(df):
        #import pydz
        #tz = pytz.time("EDT")
        for i in range(len(df['Time'])):
            a = datetime.datetime.strptime(df["Time"][i],"%Y-%m-%dT%H:%M:%S.%fZ")
            a = time.mktime(a.timetuple())
            a -= 14400
            df.iloc[[i], [0]] = a

    time_convert(df)

    df_columns = list(filter(lambda s: "job" in s,df.columns))
    for i in df_columns:
        df[i] = df[i] / 16
    df_columns.append("Time")
    df1 = df[df_columns]
    # print(df1)
    
    for index, row in df1.iterrows():
        if sum(row[:-1]) == 0:
            df1 = df1.drop(index)
    sub_order = {}
    ordered = []
    for i in df1.columns[:-1]:
        sub_order[i] = df1[i].tolist().index(list(filter(lambda x: x!=0,df1[i]))[0])
    for w in sorted(sub_order, key=sub_order.get):
        ordered.append(w)
    ordered.append("Time")
    df2 = df1[ordered]
    df2 = df2.reset_index(drop=True)
    # print(df2)
    if 'job1' in df2.columns:
        init_time = df2['Time'][0]


 

n=1
alljoblist = []
allstarttime = []
allendtime = []
for node in input_file:
    file_name = 'node{}_distribution.eps'.format(n)
    df = pd.read_csv(node,sep=";",header=0)
    # print(df['Time'])
    df = df.fillna(0)

    def time_convert(df):
        #import pydz
        #tz = pytz.time("EDT")
        for i in range(len(df['Time'])):
            a = datetime.datetime.strptime(df["Time"][i],"%Y-%m-%dT%H:%M:%S.%fZ")
            a = time.mktime(a.timetuple())
            a -= 14400
            df.iloc[[i], [0]] = a

    time_convert(df)

    df_columns = list(filter(lambda s: "job" in s,df.columns))
    for i in df_columns:
        df[i] = df[i] / 16
    df_columns.append("Time")
    df1 = df[df_columns]
    
    for index, row in df1.iterrows():
        if sum(row[:-1]) == 0:
            df1 = df1.drop(index)
    df1['Time'] = df1['Time'] - init_time
    sub_order = {}
    ordered = []
    for i in df1.columns[:-1]:
        sub_order[i] = df1[i].tolist().index(list(filter(lambda x: x!=0,df1[i]))[0])
    for w in sorted(sub_order, key=sub_order.get):
        ordered.append(w)
    ordered.append("Time")
    df2 = df1[ordered]
    df2 = df2.reset_index(drop=True)
    # print(df2)
    
    joblist = np.array(df2.columns).tolist()[:-1]
    alljoblist.append(joblist)

  
    # print(joblist)
    endlist = []
    startlist = []
    
    
    for job in joblist:
        for i in range(len(df2[job])):
            if df2[job][i] == 0.0:
                pass
            else:
                end_time = df2['Time'][i] 
        endlist.append(end_time)

    df2 = df2.replace(0,np.nan)
    index = df2.apply(lambda series: series.first_valid_index())[:-1]
    df2 = df2.replace(np.nan,0)
    startlist = df2['Time'][index].values.tolist()
    # print('start',startlist)
    # print('end',endlist)
    allstarttime.append(startlist)
    allendtime.append(endlist)


node1_color = '#FFA500'
node2_color = '#87CEEB'
node3_color = '#808000'
node4_color = '#D2691E'
node5_color = '#90EE90'
node6_color = '#FF1493'
node7_color = '#8B0000'
node8_color = '#800080'

color_init = [node1_color,node2_color,node3_color,node4_color]
colorlist = []

index = 0
for node in alljoblist:
    file_name = 'node{}_distribution.eps'.format(index+1)
    color=[]
    for job in node:
        
        if job.endswith('mig') or job.endswith("re"):
            job = job.split('-')[0]
        n=0
        for no in alljoblist:
            if job in no:
                color.append(color_init[n])
            n+=1
    colorlist.append(color)
    


    
    plt.figure(figsize=(10, 5))
    
    labels = node
    

    xstart = allstarttime[index]
    xstop = allendtime[index]
    y = labels
    # print(xstart)
    # print(xstop)

    f_size = 16

    plt.xlabel("Time(seconds)",fontsize=f_size)
    plt.ylabel("Job Id",fontsize=f_size)
    
    plt.xlim(0, max(xstop)+10)

    # print(colorlist[index])
    plt.hlines(y, xstart, xstop, colors=colorlist[index], lw=8, label =labels)

    from matplotlib.lines import Line2D
    custom_lines = [Line2D([0], [0], color='#FFA500', lw=4),
                Line2D([0], [0], color='#87CEEB', lw=4),
                Line2D([0], [0], color='#808000', lw=4),
                Line2D([0], [0], color='#D2691E', lw=4)]

    # fig, ax = plt.subplots()
    # lines = ax.plot(data)
    plt.legend(custom_lines, ['W -1', 'W -2', 'W -3','W -4'],loc=4,fontsize = 12)

    # plt.legend(loc='upper right',labels = "W"+"-"+str(i),fontsize = 8)
    
    plt.savefig(file_name, format='eps', dpi=1000, bbox_inches='tight')
    
    index +=1












