#!/usr/bin/env python
# coding: utf-8

# # 一级市场的统计

# In[42]:


# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:

@revise log:
    2021.02.24 创建程序
    TimeCost：285s
"""
# In[]
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import re,os
import warnings
import time
warnings.filterwarnings("ignore")
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
# In[]
begin = time.time()
data = pd.read_csv('./result2/全部基金业绩比较基准_基准组成.csv',index_col=0)
first_class = data.iloc[:,2].drop_duplicates().dropna()
second_class = data.iloc[:,3].drop_duplicates().dropna()
benchmark_class = data.iloc[:,4].drop_duplicates().dropna()
wrt1 = pd.ExcelWriter('./result2/一级分类.xlsx')
for item, index in enumerate(first_class):
    path = "./result2/一级分类/%s" % index
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
    data_i = data[data['投资类型(一级分类)']==index]
    data_i = data_i.reset_index(drop=True)
    data_i['基准数目'] = 0
    for i in range(data_i.shape[0]):
        data_i.loc[i,'基准数目'] = len(data_i.loc[i,'业绩比较基准'].split('+'))
    loop_of_num = set(data_i['基准数目'].values)
    for num in loop_of_num:
        tempDf = data_i[(data_i['基准数目']==num)].reset_index(drop = True)
        countDf = pd.DataFrame(columns=('业绩比较基准','基准对应的基金数目','基金对应平均比例'))
        benchmark = set(tempDf['基准是_1'].values.tolist()+tempDf['基准是_2'].values.tolist()+tempDf['基准是_3'].values.tolist()+tempDf['基准是_4'].values.tolist()+tempDf['基准是_5'].values.tolist())  
        for benm in benchmark:
            if not isinstance(benm,float):
#                 print(benm)
                list_ratio = []
                list_ratio_num = []
                list_ratio+=tempDf[tempDf['基准是_1']==benm]['基准比例_1'].values.tolist()
                list_ratio+=tempDf[tempDf['基准是_2']==benm]['基准比例_2'].values.tolist()
                list_ratio+=tempDf[tempDf['基准是_3']==benm]['基准比例_3'].values.tolist()
                list_ratio+=tempDf[tempDf['基准是_4']==benm]['基准比例_4'].values.tolist()
                list_ratio+=tempDf[tempDf['基准是_5']==benm]['基准比例_5'].values.tolist()
                average = 0
                if len(list_ratio)>10:
                    for ratio in list_ratio:
                        if not isinstance(ratio,float):
                            if (len(ratio)>5) or (ratio=='I') or (ratio=='S'):
                                continue
                            if ratio[-1]=='%':
                                list_ratio_num.append(float(ratio[:-1])/100)
                            else:
                                list_ratio_num.append(float(ratio)/100)
                    if len(list_ratio_num)!=0:
                        average = np.sum(list_ratio_num)/len(list_ratio_num)
                    else:
                        average = 0
                if num==1 or benm[-1]=='%':
                    average = 1
                if len(list_ratio_num)>5:
                    ratio_df = dict(zip(*np.unique(list_ratio_num, return_counts=True)))
                    ratio_df = pd.DataFrame([ratio_df]).T
                    ratio_df.reset_index(inplace=True)
#                     print(ratio_df)
#                     print(list_ratio_num)
                    ratio_df.columns = ['比率', '频次']
                    plot_distribution(ratio_df.loc[:,'比率'],ratio_df.loc[:,'频次'],index,num,benm)               
#                 if benm=='创业板指数收益率' and index=='股票型基金' and num==2:
#                     print(list_ratio)
#                     print(list_ratio_num)
#                     print(average)
                cnt = 0
                for index_temp in range(tempDf.shape[0]):   
                    if (benm == tempDf.loc[index_temp,'基准是_1']) or (benm == tempDf.loc[index_temp,'基准是_2']) or (benm == tempDf.loc[index_temp,'基准是_3']) or (benm == tempDf.loc[index_temp,'基准是_4'] or (benm == tempDf.loc[index_temp,'基准是_5'])):
                        cnt+=1
                if benm[-1]=='%':
                    benm = '固定利率'+benm
                new=pd.DataFrame({'业绩比较基准':benm,'基准对应的基金数目':cnt,'基金对应平均比例':average},index=[1])
                countDf = countDf.append(new,ignore_index=True)
        countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False).reset_index(drop = True)
        if countDf.shape[0]>=5:
            countDf.to_csv('./result2/%s' % index +'num_'+str(num)+ '.csv', encoding="utf_8_sig")
            countDf.to_excel(excel_writer=wrt1, sheet_name='%s' % index +'num_'+str(num))
        print("drawing...")
        plot_num(countDf.loc[:,'业绩比较基准'][:20], countDf.loc[:,'基准对应的基金数目'][:20],index,num)
wrt1.save()
wrt1.close()
end = time.time()
print("Time use:%d"%(end-begin))




def plot_num(dataA,dataB,index,num):
    fig, axes = plt.subplots(figsize=(len(dataA)*2, len(dataA)),    # 图表区的大小
        facecolor='cornsilk',)    # 图表区的背景色
    plt.rcParams['font.size'] = 20
    plt.barh(dataA, dataB, color='grey')
    for a, b in zip(dataB,dataA):
        plt.text(a+0.5, b, '%.0f' %a, ha='center', va='center', fontsize=20,color = "r")

    plt.xlabel('主动基金业绩比较基准选择研究',fontproperties='SimHei')
    plt.ylabel('业绩比较基准类型',fontproperties='SimHei')
    plt.title('基金大类_%s'%index +'_基准组成数目_%d' %num,fontproperties='SimHei')
    plt.tight_layout()
    isExists = os.path.exists("./result2/一级分类/%s"%index)
    if not isExists:
        os.makedirs("./result2/一级分类/%s"%index)
    plt.savefig('./result2/一级分类/%s'%index +'/基金大类_%s'%index +'_基准组成数目_%d' %num+'.png')
#     plt.show()



def plot_distribution(dataA,dataB,index,num,benchmark):
    fig, axes = plt.subplots(figsize=(20, 10),    # 图表区的大小
        facecolor='cornsilk',)    # 图表区的背景色
    plt.rcParams['font.size'] = 20
    plt.plot(dataA,dataB)
    plt.xlabel('基金标准所占比例',fontproperties='SimHei')
    plt.ylabel('频次',fontproperties='SimHei')
    plt.title("基金标准_%s"%benchmark+'基金大类_%s'%index +'_基准组成数目_%d' %num,fontproperties='SimHei')
    plt.tight_layout()
    isExists = os.path.exists("./result2/一级分类图示/%s"%index)
    if not isExists:
        os.makedirs("./result2/一级分类图示/%s"%index)
    plt.savefig('./result2/一级分类图示/%s'%index +'/基金大类_%s'%index +'_基准组成数目_%d' %num+"基金标准_%s"%benchmark+'.png')

