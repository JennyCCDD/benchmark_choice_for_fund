# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:
    plsreg2
@revise log:
    2021.02.25 创建程序

"""
# In[]
import numpy as np
import pandas as pd
from sklearn.cross_decomposition import PLSRegression
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import re,os
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）

# In[]
data_class_stock = pd.read_excel('./result/二级分类.xlsx',sheet_name='偏股混合型基金')
# data_class_stock = data_class_stock.iloc[:,:-1]
stock_benchmark = pd.DataFrame(data_class_stock.groupby(['所选股指']).sum()['基准对应的基金数目'])
stock_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选股指']).mean()['所选股指比例'])
stock_ben = pd.merge(stock_benchmark,stock_benchmark_ratio,on=['所选股指'])
stock_ben.reset_index(inplace=True)
stock_ben.columns = ['所选股指', '基准对应的基金数目','所选股指比例平均数']
stock_ben = stock_ben.sort_values(by='基准对应的基金数目',ascending=False)
stock_ben.drop(0,inplace=True)

# In[]
bond_benchmark = pd.DataFrame(data_class_stock.groupby(['所选债指']).sum()['基准对应的基金数目'])
# bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()['所选债指比例'])

bond_benchmark.reset_index(inplace=True)
bond_benchmark.columns = ['所选债指', '基准对应的基金数目']
bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()).iloc[:,-1]#['所选债指比例']
bond_benchmark_ratio = pd.DataFrame(bond_benchmark_ratio)
bond_benchmark_ratio.reset_index(inplace=True)
bond_benchmark_ratio.columns = ['所选债指', '所选债指比例平均数']

bond_ben = pd.merge(bond_benchmark,bond_benchmark_ratio,
                    on='所选债指')
# bond_ben.reset_index(inplace=True)
bond_ben.columns = ['所选债指', '基准对应的基金数目','所选债指比例平均数']
bond_ben = bond_ben.sort_values(by='基准对应的基金数目',ascending=False)
bond_ben.drop(0,inplace=True)

# In[]
wrt2stat = pd.ExcelWriter('./result/二级分类_统计.xlsx')
for sheet_i in ['偏股混合型基金','灵活配置型基金','增强指数型基金','普通股票型基金','偏债混合型基金']:
    data_class_i = pd.read_excel('./result/二级分类.xlsx', sheet_name='%s'%sheet_i)
    stock_benchmark = pd.DataFrame(data_class_stock.groupby(['所选股指']).sum()['基准对应的基金数目'])
    stock_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选股指']).mean()['所选股指比例'])
    stock_ben = pd.merge(stock_benchmark, stock_benchmark_ratio, on=['所选股指'])
    stock_ben.reset_index(inplace=True)
    stock_ben.columns = ['所选股指', '基准对应的基金数目', '所选股指比例平均数']
    stock_ben = stock_ben.sort_values(by='基准对应的基金数目', ascending=False)
    stock_ben.drop(0, inplace=True)

    # bond_benchmark = pd.DataFrame(data_class_stock.groupby(['所选债指']).sum()['基准对应的基金数目'])
    # bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()['所选债指比例'])
    # bond_ben = pd.merge(bond_benchmark, bond_benchmark_ratio,on=['所选债指'])
    # bond_ben.reset_index(inplace=True)
    # bond_ben.columns = ['所选债指', '基准对应的基金数目', '所选债指比例平均数']
    # bond_ben = bond_ben.sort_values(by='基准对应的基金数目', ascending=False)
    # bond_ben.drop(0, inplace=True)

    bond_benchmark = pd.DataFrame(data_class_stock.groupby(['所选债指']).sum()['基准对应的基金数目'])
    # bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()['所选债指比例'])

    bond_benchmark.reset_index(inplace=True)
    bond_benchmark.columns = ['所选债指', '基准对应的基金数目']
    bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()).iloc[:, -1]  # ['所选债指比例']
    bond_benchmark_ratio = pd.DataFrame(bond_benchmark_ratio)
    bond_benchmark_ratio.reset_index(inplace=True)
    bond_benchmark_ratio.columns = ['所选债指', '所选债指比例平均数']

    bond_ben = pd.merge(bond_benchmark, bond_benchmark_ratio,
                        on='所选债指')
    # bond_ben.reset_index(inplace=True)
    bond_ben.columns = ['所选债指', '基准对应的基金数目', '所选债指比例平均数']
    bond_ben = bond_ben.sort_values(by='基准对应的基金数目', ascending=False)
    bond_ben.drop(0, inplace=True)

    stock_ben.to_excel(excel_writer=wrt2stat, sheet_name='股票_%s' % sheet_i)
    bond_ben.to_excel(excel_writer=wrt2stat, sheet_name='债券_%s' % sheet_i)

wrt2stat.save()
wrt2stat.close()
# In[]
data_class_stock = pd.read_excel('./result/二级分类.xlsx',sheet_name='股票多空')
float_benchmark = pd.DataFrame(data_class_stock.groupby(['浮动基准']).sum()['基准对应的基金数目'])
fix_benchmark = pd.DataFrame(data_class_stock.groupby(['固定基准']).mean()['基准对应的基金数目'])
float_benchmark.to_csv('浮动基准_股票多空.csv', encoding="utf_8_sig")
fix_benchmark.to_csv('固定基准_股票多空.csv' ,encoding="utf_8_sig")

# In[]
data_class_stock = pd.read_excel('./result/二级分类.xlsx',sheet_name='偏股混合型基金')
stock_benchmark = pd.DataFrame(data_class_stock.groupby(['所选股指']).sum()['基准对应的基金数目'])
stock_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选股指']).mean()['所选股指比例'])
# pivot = pd.pivot_table(data_class_stock,
#                        index=['所选股指'],    # 透视的行，分组依据
#                        values=['基准对应的基金数目'],
#                        columns=['所选股指比例'],
#                        aggfunc=[np.mean])
stock_ben = pd.merge(stock_benchmark,stock_benchmark_ratio,on=['所选股指'])
stock_ben.reset_index(inplace=True)
stock_ben.columns = ['所选股指', '基准对应的基金数目','所选股指比例平均数']
stock_ben = stock_ben.sort_values(by='基准对应的基金数目',ascending=False)
stock_ben.drop(0,inplace=True)

# In[]
data = pd.read_excel('全部基金业绩比较基准-数据.xlsx')
# bool = countDf['业绩比较基准'].str.contains(myClass)
data['指数组合'] = data['业绩比较基准'].apply(lambda x: x.str.contains("+"))

