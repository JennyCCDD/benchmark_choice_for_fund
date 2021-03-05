# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:
    plsreg2
@revise log:
    2021.02.24 创建程序

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
data = pd.read_excel('全部基金业绩比较基准-数据.xlsx')
# data.index = data.index.apply(lambda x: re.sub('\s+', '', str(x)).strip())
# data = data.drop(['投资类型[基金分类]投资类型(一级分类)'],axis = 1)
# In[]
# data['ID'] = data.apply(lambda x: x.loc[:,'证券代码']+x.loc[:,'证券简称'],axis=1)
# In[]
first_class = data.loc[:,'投资类型(一级分类)'].drop_duplicates().dropna()
second_class = data.loc[:,'投资类型(二级分类)'].drop_duplicates().dropna()
benchmark_class = data.loc[:,'业绩比较基准'].drop_duplicates().dropna()
# In[]
# pivot = pd.pivot_table(data,
#                        index='证券代码',    # 透视的行，分组依据
#                        values='业绩比较基准')
# In[]
wrt1 = pd.ExcelWriter('./result/一级分类.xlsx')
for item, index in enumerate(first_class):
    path = "./result/一级分类/%s" % index
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')

    data_i = data[data['投资类型(一级分类)']==index]
    # data_i.sort_values('业绩比较基准')
    # des = pd.DataFrame(data_i['业绩比较基准'].drop_duplicates().dropna())
    # value_count()
    countList = data_i['业绩比较基准'].values.tolist()
    countDict = dict(zip(*np.unique(countList,return_counts=True)))
    countDf = pd.DataFrame([countDict]).T
    countDf.reset_index(inplace=True)
    countDf.columns = ['业绩比较基准','基准对应的基金数目']
    countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False)
    countDf.drop(0, inplace=True)

    countDf.to_csv('./result/%s' % index + '.csv', encoding="utf_8_sig")
    countDf.to_excel(excel_writer=wrt1, sheet_name='%s' % index)



    if countDf['基准对应的基金数目'].any()>20:
        pass
        countDf.to_csv('./result/%s' % index + '.csv', encoding="utf_8_sig")
    else:
        fundDict = {}
        ####################################
        ##############丰富一下此处的文本分类####
        ####################################
        for myClass in ['定期存款','黄金','商品','%','债券','中证500','沪深300','中债','可转债']:
            bool = countDf['业绩比较基准'].str.contains(myClass)
            filter_data = countDf[bool]
            num = filter_data['基准对应的基金数目'].sum()
            fundDict[myClass] = num
            fundDf = pd.DataFrame([fundDict]).T
            fundDf.reset_index(inplace=True)
            fundDf.columns = ['业绩比较基准类型', '基准对应的基金数目']
            fundDf = fundDf.sort_values(by='基准对应的基金数目',ascending=False)
            fundDf.drop(0,inplace=True)
            fundDf.to_csv('./result/一级分类/%s'%index +'/基金大类_%s'%index +'_细分类_%s' %myClass+'.csv',encoding="utf_8_sig")


            # plt.xkcd()# 类似手写体的style
            # 绘制横向的柱状体， 第一个参数是y轴的可迭代对象, 第二个参数是x轴的可迭代对象, 颜色是绿色
            plt.barh(fundDf['业绩比较基准类型'], fundDf['基准对应的基金数目'], color='#0BF92E')
            # plt.xticks(range(len(fundDf['业绩比较基准类型'])),fundDf['业绩比较基准类型']) ## 可以设置坐标字
            plt.xlabel('主动基金业绩比较基准选择研究',fontproperties='SimHei')
            plt.ylabel('业绩比较基准类型',fontproperties='SimHei')
            plt.title('基金大类_%s'%index +'_细分类_%s' %myClass,fontproperties='SimHei')
            plt.tight_layout()

            plt.show()
            plt.savefig('./result/一级分类/%s'%index +'/基金大类_%s'%index +'_细分类_%s' %myClass+'.png')
wrt1.save()
wrt1.close()


# In[]
wrt2 = pd.ExcelWriter('./result/二级分类.xlsx')
for item, index in enumerate(second_class):
    path = "./result/二级分类/%s" % index
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' 创建成功')
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
    data_i = data[data['投资类型(二级分类)']==index]
    # data_i.sort_values('业绩比较基准')
    # des = pd.DataFrame(data_i['业绩比较基准'].drop_duplicates().dropna())
    # value_count()
    countList = data_i['业绩比较基准'].values.tolist()
    countDict = dict(zip(*np.unique(countList,return_counts=True)))
    countDf = pd.DataFrame([countDict]).T
    countDf.reset_index(inplace=True)
    countDf.columns = ['业绩比较基准','基准对应的基金数目']
    countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False)
    # countDf.drop(0, inplace=True)
    # countDf.to_csv('./result/%s' % index + '.csv', encoding="utf_8_sig")
    # countDf.to_excel(excel_writer=wrt2,sheet_name='%s' % index)
wrt2.save()
wrt2.close()

# In[]
for item, index in enumerate(second_class):
    data_class_i = pd.read_excel('./result/二级分类.xlsx',sheet_name='%s' % index)
    data_class_i_top = data_class_i.iloc[:20,:]
    plt.barh(data_class_i_top['业绩比较基准'], data_class_i_top['基准对应的基金数目'], color='#0BF92E')
    # plt.xticks(range(len(fundDf['业绩比较基准类型'])),fundDf['业绩比较基准类型']) ## 可以设置坐标字
    plt.xlabel('主动基金业绩比较基准选择研究', fontproperties='SimHei')
    plt.ylabel('业绩比较基准类型', fontproperties='SimHei')
    plt.title('基金大类_%s' % index + '_细分类_%s' % index, fontproperties='SimHei')
    plt.tight_layout()
    # axes.set_autoscale_on(True)
    # axes.autoscale_view(True, True, True)
    plt.show()
    # plt.savefig('./result/二级分类/%s' % index +'.png')

# In[]
data_class_stock = pd.read_excel('./result/二级分类.xlsx',sheet_name='偏股混合型基金')
fundDict = {}

for myClass in ['中证500','上证国债','沪深300','可转债']:
    bool = data_class_stock['业绩比较基准'].str.contains(myClass)
    filter_data = data_class_stock[bool]
    num = filter_data['基准对应的基金数目'].sum()
    fundDict[myClass] = num
    fundDf = pd.DataFrame([fundDict]).T
    fundDf.reset_index(inplace=True)
    fundDf.columns = ['业绩比较基准类型', '基准对应的基金数目']
    fundDf = fundDf.sort_values(by='基准对应的基金数目',ascending=False)
    fundDf.drop(0,inplace=True)
    fundDf.to_csv('./result/二级分类/偏股混合型基金.csv',encoding="utf_8_sig")


    # plt.xkcd()# 类似手写体的style
    # 绘制横向的柱状体， 第一个参数是y轴的可迭代对象, 第二个参数是x轴的可迭代对象, 颜色是绿色
    plt.barh(fundDf['业绩比较基准类型'], fundDf['基准对应的基金数目'], color='#0BF92E')
    # plt.xticks(range(len(fundDf['业绩比较基准类型'])),fundDf['业绩比较基准类型']) ## 可以设置坐标字
    plt.xlabel('主动基金业绩比较基准选择研究',fontproperties='SimHei')
    plt.ylabel('业绩比较基准类型',fontproperties='SimHei')
    plt.title('基金大类_%s'%index +'_细分类_%s' %myClass,fontproperties='SimHei')
    plt.tight_layout()

    plt.show()