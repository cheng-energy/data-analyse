import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.gridspec as gridspec
import numpy as np
movies_data = pd.read_csv("D:\\BaiduNetdiskDownload\\数据分析\\movies.csv",sep= ',')
#缺失值处理，直接填充上一个好像不太好，还是直接删除
#第一个图表的数据处理
movies_data = movies_data.dropna()
movies_data = movies_data.drop_duplicates(subset='电影名')
movies_data.sort_values(['年份','上映时间'],ascending=False)


# 全局设置中文字体（用你系统里有的字体）
plt.rcParams['font.family'] = 'KaiTi'
plt.rcParams['axes.unicode_minus'] = False

# 开始绘制图表
plt.figure(figsize=[12,10])
plt.subplot(2,2,1)
shu = movies_data.groupby('年份')['年份'].size()
plt.ylabel('电影数量',fontsize=15)
plt.plot(shu.index,shu)
plt.xlabel('年份',fontsize=10)
plt.xticks(shu.index[::10], rotation=45)
plt.title('不同年份电影数量的折线图',fontsize=20)
plt.grid(True,linestyle=':', alpha=0.5)

# 绘制第二份图表
#第二个图表的数据处理
language = movies_data.groupby('语言')['语言'].size()
plt.subplot(2,2,3)
plt.title('不同语言电影的数量统计图',fontsize=20)
plt.bar(language.index[::1],language)
plt.xticks(rotation=45)
plt.xlabel('语言',fontsize=20)
plt.grid(True,linestyle=':',alpha=0.5)


# 绘制第三个图表：统计不同类型电影的数量
# 1. 去除空格，按逗号拆分成列表
types_series = movies_data['类型'].str.replace(' ', '').str.split(',')

# 2. 展开成多行
types_exploded = movies_data.assign(类型=types_series).explode('类型')

# 3. 统计每个类型的数量
type_counts = types_exploded['类型'].value_counts()
plt.subplot(2,2,2)
plt.title('不同类型电影的数量',fontsize=15)
plt.bar(type_counts.index,type_counts.values)
plt.xlabel('电影类型',fontsize=15)
plt.ylabel('电影数量',fontsize=15)
plt.tight_layout()
plt.grid(True,linestyle=':',alpha=0.5)


# 第四个图表绘制，统计对比各个电影的评分比例（饼状图）
bin = movies_data.groupby('评分')['评分'].count()
# 绘制饼图
plt.subplot(2,2,4)
plt.pie(bin.values, autopct='%1.1f%%',shadow=False,startangle=90,colors=['red', 'blue', 'green', 'orange', 'purple'])
plt.title('电影不同评分比例',fontsize=15)
plt.savefig('D:/python/energy-python/images',dpi=1000)
plt.show()

