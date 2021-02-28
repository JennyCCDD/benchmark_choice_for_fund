# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:
    plsreg2
@revise log:
    2021.02.26 创建程序
                统计全部基金的情况
"""
# In[]
import numpy as np
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')
# In[]
# 拆分基准的组成部分
def decompose(df):
    df['基准组成部分list'] = df['业绩比较基准'].apply(lambda x: str(x).split('+'))
    # 计算所有基准中最多的组成部分是多少
    num = 0
    for i in range(len(df['基准组成部分list'])):
        if len(df['基准组成部分list'].iloc[i]) > num:
            num = len(df['基准组成部分list'].iloc[i])
    # 并将所有的组成部分的list补齐为相同长度
    df['基准组成部分list'] = df['基准组成部分list'].apply(lambda x: x + [np.nan] * (num - len(x)))

    # 统计全部基金的情况，将每一只基金的业绩比较基准进行拆分
    # df.dropna(inplace=True)
    for j in range(num):
        df['基准组成部分%s' % (j + 1)] = df['基准组成部分list'].apply(lambda x: x[j])
        df['基准%s' % (j + 1)] = df['基准组成部分%s' % (j+1)].apply(lambda x: str(x).split('*'))
        df['基准%s' % (j + 1)] = df['基准%s' % (j + 1)].apply(lambda x: x + [np.nan] * (2 - len(x)))

        df['基准是_%s' % (j + 1)] = df['基准%s' % (j + 1)].apply(lambda x: x[0])
        df['基准比例_%s' % (j + 1)] = df['基准%s' % (j + 1)].apply(lambda x: x[1])
    return df

# In[]
# 读取全市场的基金业绩比较基准数据，将基准组成部分进行拆分
data = pd.read_excel('全部基金业绩比较基准-数据.xlsx')
data = decompose(data)

# In[]

data_cal = data.copy()
data_cal.drop(['基准指数代码',
               '基准组成部分list',
               '基准组成部分1',
               '基准组成部分2',
               '基准组成部分3',
               '基准组成部分4',
               '基准组成部分5',
               '基准1','基准2','基准3','基准4','基准5'],axis=1,inplace=True)



def countFun(series):
    countList = series.values.tolist()
    countDict = dict(zip(*np.unique(countList, return_counts=True)))
    countDf = pd.DataFrame([countDict]).T
    countDf.reset_index(inplace=True)
    countDf.columns = ['业绩比较基准', '基准对应的基金数目']
    countDf = countDf.sort_values(by='基准对应的基金数目', ascending=False)
    countDf.drop(0, inplace=True)
    return countDf
# In[]
first_class = data.loc[:,'投资类型(一级分类)'].drop_duplicates().dropna()
for item, index in enumerate(first_class):
    data_i = data_cal.loc[data_cal['投资类型(一级分类)']==index]
    data_i = decompose(data_i)
    data_i.to_csv('./result/投资类型(一级分类)_%s'%index+'_decompose.csv',encoding='utf_8_sig')
    # print(data_i)
    # countdf = countFun(data_i.loc[data_i['基准组成部分2'] == np.nan]['业绩比较基准'])
