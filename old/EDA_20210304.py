# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:
    plsreg2
@revise log:
    2021.02.25 创建程序

"""
# In[]
import pandas as pd


# In[]
wrt2stat = pd.ExcelWriter('./result/二级分类_统计.xlsx')
for sheet_i in ['偏股混合型基金','灵活配置型基金','增强指数型基金','普通股票型基金','偏债混合型基金']:
    data_class_i = pd.read_excel('./result/二级分类.xlsx', sheet_name='%s'%sheet_i)
    stock_benchmark = pd.DataFrame(data_class_i.groupby(['所选股指']).sum()['基准对应的基金数目'])
    stock_benchmark_ratio = pd.DataFrame(data_class_i.groupby(['所选股指']).mean()['所选股指比例'])
    stock_ben = pd.merge(stock_benchmark, stock_benchmark_ratio, on=['所选股指'])
    stock_ben.reset_index(inplace=True)
    stock_ben.columns = ['所选股指', '基准对应的基金数目', '所选股指比例平均数']
    stock_ben = stock_ben.sort_values(by='基准对应的基金数目', ascending=False)
    stock_ben.drop(0, inplace=True)

    bond_benchmark = pd.DataFrame(data_class_i.groupby(['所选债指']).sum()['基准对应的基金数目'])
    # bond_benchmark_ratio = pd.DataFrame(data_class_stock.groupby(['所选债指']).mean()['所选债指比例'])

    bond_benchmark.reset_index(inplace=True)
    bond_benchmark.columns = ['所选债指', '基准对应的基金数目']
    bond_benchmark_ratio = pd.DataFrame(data_class_i.groupby(['所选债指']).mean()).iloc[:, -1]  # ['所选债指比例']
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