import pandas as pd
import datetime
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import sys
import seaborn as sns


job1_color = "#9b59b6"
job2_color = "#e74c3c"
job3_color = "#34495e"
job4_color = "#2ecc71"
job5_color = '#00008B'
job6_color = '#008B8B'
job7_color = '#B8860B'
job8_color = '#FF8C00'
job9_color = '#BC8F8F'
job10_color = '#808000'
job11_color = '#6B8E23'
job12_color = "#9b59b6"
job13_color = '#FFA500'
job14_color = '#FF4500'
job15_color = '#DA70D6'
job16_color = '#EEE8AA'
job17_color = '#AFEEEE'
job18_color = '#DB7093'
job19_color = '#9ACD32'
job20_color = '#FFDAB9'


input_file = ['node1.csv','node2.csv','node3.csv','node4.csv']

n=1
for node in input_file:
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
    sub_order = {}
    ordered = []
    for i in df1.columns[:-1]:
        sub_order[i] = df1[i].tolist().index(list(filter(lambda x: x!=0,df1[i]))[0])
    for w in sorted(sub_order, key=sub_order.get):
        ordered.append(w)
    ordered.append("Time")
    df2 = df1[ordered]
    df2 = df2.reset_index(drop=True)
    if 'job1' in df2.columns:
        init_time = df2['Time'][0]

 

n=1
for node in input_file:
    file_name = 'node{}_cpu.eps'.format(n)
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
    
    
    joblist = np.array(df2.columns).tolist()[:-1]
    for i in range(len(joblist)):
        if joblist[i].endswith('mig') or joblist[i].endswith('re'):
            joblist[i] = joblist[i].split('-')[0]

    color_list = []
    for job in joblist:
        color = eval('{}_color'.format(job))
        color_list.append(color)
    # print(color_list)


    plt.figure(figsize=(10, 5))

    x = df2["Time"].values
    y = df2.drop(columns=['Time']).T.values
    # l = list(range(df2.shape[1]))
    # l.pop(0)
    #labels = df1.columns[:-1].tolist()
    labels = joblist
    f_size = 16
    fig, ax = plt.subplots()
    x_major_locator=MultipleLocator(300)
    plt.stackplot(x,y,labels=labels,colors = color_list)
    plt.xlabel("Time",fontsize=f_size)
    plt.ylabel("CPU Usage",fontsize=f_size)
    plt.ylim(0, 1) 
    plt.xlim(xmin=0)
    ax.xaxis.set_major_locator(x_major_locator)
    ax.set_axisbelow(True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.grid()
    plt.legend(loc='upper right',fontsize = 8)
    #plt.legend(bbox_to_anchor=(0.5, -0.1),loc='upper center',ncol=4)
    plt.margins(0,0)
    plt.xticks(fontsize=f_size-4)
    plt.yticks(fontsize=f_size-4)
    plt.savefig(file_name, format='eps', dpi=1000, bbox_inches='tight')
    
    n+=1









