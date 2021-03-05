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
data1 = pd.read_excel('初步结论20210301.xlsx',sheet_name='股指基准_二级分类_偏股混合型基金')
data2 = pd.read_excel('初步结论20210301.xlsx',sheet_name='股指基准_二级分类_灵活配置型基金')
data3 = pd.read_excel('初步结论20210301.xlsx',sheet_name='股指基准_二级分类_普通股票型基金')
data4 = pd.read_excel('初步结论20210301.xlsx',sheet_name='股指基准_二级分类_偏债混合型基金')
# In[]
data = pd.concat([data1,data2,data3,data4],axis=0)
# In[]
stock_benchmark = pd.DataFrame(data.groupby(['所选股指']).sum()['基准对应的基金数目'])
stock_benchmark_ratio = pd.DataFrame(data.groupby(['所选股指']).mean()['所选股指比例平均数'])

stock_ben = pd.merge(stock_benchmark,stock_benchmark_ratio,on=['所选股指'])
stock_ben.reset_index(inplace=True)
stock_ben.columns = ['所选股指', '基准对应的基金数目','所选股指比例平均数']
stock_ben = stock_ben.sort_values(by='基准对应的基金数目',ascending=False)
stock_ben.drop(0,inplace=True)


# In[]
data11 = pd.read_excel('初步结论20210301.xlsx',sheet_name='债指基准_二级分类_偏股混合型基金')
data21 = pd.read_excel('初步结论20210301.xlsx',sheet_name='债指基准_二级分类_灵活配置型基金')
data31 = pd.read_excel('初步结论20210301.xlsx',sheet_name='债指基准_二级分类_普通股票型基金')
data41 = pd.read_excel('初步结论20210301.xlsx',sheet_name='债指基准_二级分类_偏债混合型基金')
# In[]
data_1 = pd.concat([data11,data21,data31,data41],axis=0)
# In[]
stock_benchmark = pd.DataFrame(data_1.groupby(['所选债指']).sum()['基准对应的基金数目'])
stock_benchmark_ratio = pd.DataFrame(data_1.groupby(['所选债指']).mean()['所选债指比例平均数'])

bond_ben = pd.merge(stock_benchmark,stock_benchmark_ratio,on=['所选债指'])
bond_ben.reset_index(inplace=True)
bond_ben.columns = ['所选债指', '基准对应的基金数目','所选债指比例平均数']
bond_ben = bond_ben.sort_values(by='基准对应的基金数目',ascending=False)
bond_ben.drop(0,inplace=True)

# In[]
stock_ben.to_csv('./result/所选股指比例平均数.csv', encoding="utf_8_sig")
bond_ben.to_csv('./result/所选债指比例平均数.csv', encoding="utf_8_sig")

# In[]
# 对行业分类的基金的基准选择进行研究
df = pd.read_excel('初步结论20210301.xlsx',sheet_name='全部基金业绩比较基准-数据')
df_industry = df.dropna(subset =[ '所属主题基金类别(Wind行业)'])
industry = df_industry['所属主题基金类别(Wind行业)'].drop_duplicates().dropna()

# In[]
df_indus = pd.DataFrame(df_industry.groupby(['所属主题基金类别(Wind行业)']).count()['证券代码'])
df_indus.reset_index(inplace=True)
df_indus.columns = ['所属主题基金类别(Wind行业)','行业对应的基金数目']
df_indus = df_indus.sort_values(by='行业对应的基金数目',ascending=False)

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
df_industry = decompose(df_industry)
# In[]
wrtindu = pd.ExcelWriter('./result/行业分类_统计_股指基准）.xlsx')
for industry_i in industry.tolist():
    df_ii = pd.read_excel('./result/行业分类.xlsx',sheet_name='行业_%s'%industry_i[:-6])
    # df_ii = df_industry[df_industry['所属主题基金类别(Wind行业)']==industry_i]

    benchmark = pd.DataFrame(df_ii.groupby(['基准是_1']).count()['证券代码'])
    df_ii['基准比例_1'] = df_ii['基准比例_1'].fillna(0)
    # df_ii['基准比例_1'] = df_ii['基准比例_1'].apply(lambda x : x.replace(" ", ""))
    df_ii['基准比例_1'] = df_ii['基准比例_1'].astype('float')
    benchmark_ratio = pd.DataFrame(df_ii.groupby(['基准是_1']).mean()['基准比例_1'])

    ben = pd.merge(benchmark, benchmark_ratio, on=['基准是_1'])
    ben.reset_index(inplace=True)
    ben.columns = ['基准是_1', '基准对应的基金数目', '所选股指比例平均数']
    ben = ben.sort_values(by='基准对应的基金数目', ascending=False)
    ben.drop(0, inplace=True)

    # countList = df_ii['基准是_1'].values.tolist()
    # countDict = dict(zip(*np.unique(countList,return_counts=True)))
    # countDf = pd.DataFrame([countDict]).T
    # countDf.reset_index(inplace=True)
    # countDf.columns = ['基准是_1','基准对应的基金数目']
    # countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False)
    ben.to_excel(excel_writer=wrtindu, sheet_name='行业_%s' % industry_i[:-6])

wrtindu.save()
wrtindu.close()

# In[]
wrtindu2 = pd.ExcelWriter('./result/行业分类_统计_债指基准.xlsx')
for industry_i in industry.tolist():
    df_ii = pd.read_excel('./result/行业分类.xlsx',sheet_name='行业_%s'%industry_i[:-6])
    # df_ii = df_industry[df_industry['所属主题基金类别(Wind行业)']==industry_i]

    benchmark = pd.DataFrame(df_ii.groupby(['基准是_2']).count()['证券代码'])
    df_ii['基准比例_2'] = df_ii['基准比例_2'].fillna(0)
    # df_ii['基准比例_1'] = df_ii['基准比例_1'].apply(lambda x : x.replace(" ", ""))
    df_ii['基准比例_2'] = df_ii['基准比例_2'].astype('float')
    df_ii['基准比例_2'].fillna(1,inplace=True)
    benchmark_ratio = pd.DataFrame(df_ii.groupby(['基准是_2']).mean()['基准比例_2'])

    ben = pd.merge(benchmark, benchmark_ratio, on=['基准是_2'])
    ben.reset_index(inplace=True)
    ben.columns = ['基准是_1', '基准对应的基金数目', '所选债指比例平均数']
    ben = ben.sort_values(by='基准对应的基金数目', ascending=False)
    ben.drop(0, inplace=True)

    # countList = df_ii['基准是_1'].values.tolist()
    # countDict = dict(zip(*np.unique(countList,return_counts=True)))
    # countDf = pd.DataFrame([countDict]).T
    # countDf.reset_index(inplace=True)
    # countDf.columns = ['基准是_1','基准对应的基金数目']
    # countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False)
    ben.to_excel(excel_writer=wrtindu2, sheet_name='行业_%s' % industry_i[:-6])

wrtindu2.save()
wrtindu2.close()
