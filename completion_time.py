import pandas as pd
import os
import sys


if len(sys.argv) != 3:
    print("Useage python " + sys.argv[0]  + " <dir name>" + " <number of jobs>")
    sys.exit(0)


dir = sys.argv[1]
num = int(sys.argv[2])
ls = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]


job_list = ["job"+str(i) for i in range(1,num+1)]
ls.remove('default')
forder_name =  ['default']+ls

dic = {}
def get_time_complete(file):
    print(file)
    da = pd.read_csv(file)
    col = da.columns
    return float(da[col[0]].values[-1]) - float(da[col[0]].values[0])

for ford in forder_name:
    dic[ford] = {}
    for job_file in job_list:
        dic[ford][job_file] = get_time_complete("./"+dir+'/'+ford+"/"+job_file+".csv")

ses = dic.keys()
ses = forder_name
data = pd.DataFrame()
data["job"] = job_list
for se in ses:
    d = []
    for job in job_list:
        d.append(dic[se][job])
    data[se] = d

data.set_index('job', inplace=True)




improve_list = ['nan']
reduce_list = ['nan']
best_list = ['nan']
worst_list = ['nan']
improve_average_list = ['nan']
improve_median_list = ['nan']
reduce_average_list = ['nan']
reduce_median_list = ['nan']

for i in range(1,len(forder_name)):
    diff = data['default'] - data[forder_name[i]]
    improve_jobs = diff[diff>0] #.tolist()
    improve_average = round(improve_jobs.mean(),4)
    improve_average_list.append(improve_average)
    improve_median = round(improve_jobs.median(),4)
    improve_median_list.append(improve_median)
    improve = len(diff[diff>0])
    improve_list.append(improve)
    reduce_jobs = diff[diff<0] #.tolist()
    reduce_average = round(reduce_jobs.mean(),4)
    reduce_average_list.append(reduce_average)
    reduce_median = round(reduce_jobs.median(),4)
    reduce_median_list.append(reduce_median)
    reduce = len(diff[diff<0])
    reduce_list.append(reduce)
    pre = diff / data['default']
    best = str(round(max(pre)*100,1))+'%'
    best_list.append(best)
    worst = str(round(min(pre)*100,1))+'%'
    worst_list.append(worst)

    
data.loc['average'] = data.mean()
data.loc['improve'] = improve_list
data.loc['reduce'] = reduce_list


data.loc['improve_average'] = improve_average_list
data.loc['reduce_average'] = reduce_average_list

data.loc['improve_median'] = improve_median_list
data.loc['reduce_median'] = reduce_median_list

data.loc['best'] = best_list
data.loc['worst'] = worst_list

data.to_csv("./{}/time_com.csv".format(dir))


