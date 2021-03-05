# -*- coding: utf-8 -*-
"""
@author: Mengxuan Chen
@description:
    主动基金业绩比较基准选择研究
@revise log:
    2021.02.24 创建程序
    2021.02.25 统计二级分类
    2021.02.26  统计全部基金的情况
    2021.03.01 统计分行业的情况
    2021.03.04 统计一级分类
    2021.03.05 整理代码
"""
# In[]
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re,os
import warnings
import time
import warnings
warnings.filterwarnings('ignore')
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）


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
data = pd.read_excel('./data/全部基金业绩比较基准-数据.xlsx')
data = decompose(data)
data_cal = data.copy()
data_cal.drop([
               '基准组成部分list',
               '基准组成部分1',
               '基准组成部分2',
               '基准组成部分3',
               '基准组成部分4',
               '基准组成部分5',
               '基准1','基准2','基准3','基准4','基准5'],axis=1,inplace=True)
data_cal.to_csv('./data/全部基金业绩比较基准_基准组成.csv')


# In[]


# In[]


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
    isExists = os.path.exists("./result/一级分类/%s"%index)
    if not isExists:
        os.makedirs("./result/一级分类/%s"%index)
    plt.savefig('./result/一级分类/%s'%index +'/基金大类_%s'%index +'_基准组成数目_%d' %num+'.png')
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
    isExists = os.path.exists("./result/一级分类图示/%s"%index)
    if not isExists:
        os.makedirs("./result/一级分类图示/%s"%index)
    plt.savefig('./result/一级分类图示/%s'%index +'/基金大类_%s'%index +'_基准组成数目_%d' %num+"基金标准_%s"%benchmark+'.png')


# In[]
begin = time.time()
data = pd.read_csv('./data/全部基金业绩比较基准_基准组成.csv',index_col=0)
first_class = data.iloc[:,2].drop_duplicates().dropna()
second_class = data.iloc[:,3].drop_duplicates().dropna()
benchmark_class = data.iloc[:,4].drop_duplicates().dropna()
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
            countDf.to_csv('./result/%s' % index +'num_'+str(num)+ '.csv', encoding="utf_8_sig")
            countDf.to_excel(excel_writer=wrt1, sheet_name='%s' % index +'num_'+str(num))
        print("drawing...")
        plot_num(countDf.loc[:,'业绩比较基准'][:20], countDf.loc[:,'基准对应的基金数目'][:20],index,num)
wrt1.save()
wrt1.close()
end = time.time()
print("Time use:%d"%(end-begin))


# In[]
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
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
    countList = data_i['业绩比较基准'].values.tolist()
    countDict = dict(zip(*np.unique(countList,return_counts=True)))
    countDf = pd.DataFrame([countDict]).T
    countDf.reset_index(inplace=True)
    countDf.columns = ['业绩比较基准','基准对应的基金数目']
    countDf = countDf.sort_values(by='基准对应的基金数目',ascending=False)
wrt2.save()
wrt2.close()


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

# In[]
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
# 对行业分类的基金的基准选择进行研究
df = data.copy()
df_industry = df.dropna(subset =[ '所属主题基金类别(Wind行业)'])
industry = df_industry['所属主题基金类别(Wind行业)'].drop_duplicates().dropna()

# In[]
df_indus = pd.DataFrame(df_industry.groupby(['所属主题基金类别(Wind行业)']).count()['证券代码'])
df_indus.reset_index(inplace=True)
df_indus.columns = ['所属主题基金类别(Wind行业)','行业对应的基金数目']
df_indus = df_indus.sort_values(by='行业对应的基金数目',ascending=False)


# In[]
wrtindu = pd.ExcelWriter('./result/行业分类_统计_股指基准）.xlsx')
for industry_i in industry.tolist():
    df_ii = pd.read_excel('./result/行业分类.xlsx',sheet_name='行业_%s'%industry_i[:-6])

    benchmark = pd.DataFrame(df_ii.groupby(['基准是_1']).count()['证券代码'])
    df_ii['基准比例_1'] = df_ii['基准比例_1'].fillna(0)
    df_ii['基准比例_1'] = df_ii['基准比例_1'].astype('float')
    benchmark_ratio = pd.DataFrame(df_ii.groupby(['基准是_1']).mean()['基准比例_1'])

    ben = pd.merge(benchmark, benchmark_ratio, on=['基准是_1'])
    ben.reset_index(inplace=True)
    ben.columns = ['基准是_1', '基准对应的基金数目', '所选股指比例平均数']
    ben = ben.sort_values(by='基准对应的基金数目', ascending=False)
    ben.drop(0, inplace=True)

    ben.to_excel(excel_writer=wrtindu, sheet_name='行业_%s' % industry_i[:-6])

wrtindu.save()
wrtindu.close()

# In[]
wrtindu2 = pd.ExcelWriter('./result/行业分类_统计_债指基准.xlsx')
for industry_i in industry.tolist():
    df_ii = pd.read_excel('./result/行业分类.xlsx',sheet_name='行业_%s'%industry_i[:-6])
    benchmark = pd.DataFrame(df_ii.groupby(['基准是_2']).count()['证券代码'])
    df_ii['基准比例_2'] = df_ii['基准比例_2'].fillna(0)
    df_ii['基准比例_2'] = df_ii['基准比例_2'].astype('float')
    df_ii['基准比例_2'].fillna(1,inplace=True)
    benchmark_ratio = pd.DataFrame(df_ii.groupby(['基准是_2']).mean()['基准比例_2'])

    ben = pd.merge(benchmark, benchmark_ratio, on=['基准是_2'])
    ben.reset_index(inplace=True)
    ben.columns = ['基准是_1', '基准对应的基金数目', '所选债指比例平均数']
    ben = ben.sort_values(by='基准对应的基金数目', ascending=False)
    ben.drop(0, inplace=True)

    ben.to_excel(excel_writer=wrtindu2, sheet_name='行业_%s' % industry_i[:-6])

wrtindu2.save()
wrtindu2.close()

