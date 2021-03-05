# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:

@revise log:
    2021.02.26 创建程序
                统计全部基金的情况
"""
# In[]
import numpy as np
import pandas as pd

# In[]
# 读取全市场的基金业绩比较基准数据，将基准组成部分进行拆分
data = pd.read_excel('全部基金业绩比较基准-数据.xlsx')
data['基准组成部分list'] = data['业绩比较基准'].apply(lambda x: str(x).split('+'))
# 计算所有基准中最多的组成部分是多少，并将所有的组成部分的list补齐为相同长度
num = 0
for i in range(len(data['基准组成部分list'])):
    if len(data['基准组成部分list'].iloc[i]) > num:
        num = len(data['基准组成部分list'].iloc[i])

data['基准组成部分list'] = data['基准组成部分list'].apply(lambda x: x + [np.nan] * (num - len(x)))

# In[]
# 统计全部基金的情况，将每一只基金的业绩比较基准进行拆分
data.dropna(inplace=True)
for j in range(num):
    data['基准组成部分%s' % (j + 1)] = data['基准组成部分list'].apply(lambda x: x[j])
    data['基准%s' % (j + 1)] = data['基准组成部分%s' % (j+1)].apply(lambda x: str(x).split('*'))
    data['基准%s' % (j + 1)] = data['基准%s' % (j + 1)].apply(lambda x: x + [np.nan] * (2 - len(x)))

    data['基准是_%s' % (j + 1)] = data['基准%s' % (j + 1)].apply(lambda x: x[0])
    data['基准比例_%s' % (j + 1)] = data['基准%s' % (j + 1)].apply(lambda x: x[1])
# In[]
# 统计全部基金的情况，计算每一种业绩比较基准对应的基金数目
countList = data['业绩比较基准'].values.tolist()
countDict = dict(zip(*np.unique(countList, return_counts=True)))
countDf = pd.DataFrame([countDict]).T
countDf.reset_index(inplace=True)
countDf.columns = ['业绩比较基准', '基准对应的基金数目']
countDf = countDf.sort_values(by='基准对应的基金数目', ascending=False)
countDf.drop(0, inplace=True)
countDf['基准组成部分list'] = countDf['业绩比较基准'].apply(lambda x: str(x).split('+'))


# 计算所有基准中最多的组成部分是多少，并将所有的组成部分的list补齐为相同长度
num = 0
for i in range(len(countDf['基准组成部分list'])):
    if len(countDf['基准组成部分list'].iloc[i]) > num:
        num = len(countDf['基准组成部分list'].iloc[i])
# 统计全部基金的情况，将每一只基金的业绩比较基准进行拆分
countDf['基准组成部分list'] = countDf['基准组成部分list'].apply(lambda x: x + [np.nan] * (num - len(x)))
# In[]
for j in range(num):
    countDf['基准组成部分%s' % (j + 1)] = countDf['基准组成部分list'].apply(lambda x: x[j])
    countDf['基准%s' % (j + 1)] = countDf['基准组成部分%s' % (j+1)].apply(lambda x: str(x).split('*'))
    countDf['基准%s' % (j + 1)] = countDf['基准%s' % (j + 1)].apply(lambda x: x + [np.nan] * (2 - len(x)))

    countDf['基准是_%s' % (j + 1)] = countDf['基准%s' % (j + 1)].apply(lambda x: x[0])
    countDf['基准比例_%s' % (j + 1)] = countDf['基准%s' % (j + 1)].apply(lambda x: x[1])

    countDf.drop('基准%s' % (j + 1),axis=1,inplace=True)
countDf.to_csv('./result/全部基金业绩比较基准_基准组成.csv', encoding="utf_8_sig")


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
data_cal.to_csv('./result/全部基金业绩比较基准_基准组成.csv', encoding="utf_8_sig")

# In[]
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
one_com = pd.read_excel('./result/全部基金业绩比较基准_基准组成_明细.xlsx',sheet_name='单基准基金')
two_com = pd.read_excel('./result/全部基金业绩比较基准_基准组成_明细.xlsx',sheet_name='双基准基金')
one_com_df = countFun(one_com['业绩比较基准'])
two_com_df = countFun(one_com['业绩比较基准'])
