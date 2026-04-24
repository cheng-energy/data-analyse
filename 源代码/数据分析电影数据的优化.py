import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path


def load_and_clean_data(file_path):
    """加载并清洗电影数据"""
    movies_data = pd.read_csv(file_path, sep=',')

    # 缺失值处理
    movies_data = movies_data.dropna()

    # 去除重复电影（基于电影名）
    movies_data = movies_data.drop_duplicates(subset='电影名')

    # 按年份和上映时间排序（需要重新赋值）
    movies_data = movies_data.sort_values(['年份', '上映时间'], ascending=False)

    return movies_data


def plot_movies_by_year(movies_data, ax):
    """绘制不同年份电影数量的折线图"""
    year_counts = movies_data.groupby('年份').size()

    ax.plot(year_counts.index, year_counts.values, marker='o', linewidth=2, markersize=4)
    ax.set_xlabel('年份', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.set_title('不同年份电影数量的折线图', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle=':', alpha=0.5)

    # 每10年显示一个刻度
    if len(year_counts) > 10:
        ax.set_xticks(year_counts.index[::10])


def plot_movies_by_language(movies_data, ax):
    """绘制不同语言电影的数量统计图"""
    language_counts = movies_data.groupby('语言').size().sort_values(ascending=False)

    # 只显示前15种语言，避免过于拥挤
    top_languages = language_counts.head(15)

    bars = ax.bar(top_languages.index, top_languages.values, color='#2196F3', alpha=0.8)
    ax.set_xlabel('语言', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.set_title('不同语言电影的数量统计图（Top 15）', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle=':', alpha=0.5, axis='y')

    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)


def plot_movies_by_type(movies_data, ax):
    """绘制不同类型电影的数量统计图"""
    # 处理类型字段：去除空格，按逗号拆分
    types_series = movies_data['类型'].str.replace(' ', '').str.split(',')

    # 展开成多行
    types_exploded = movies_data.assign(类型=types_series).explode('类型')

    # 统计每个类型的数量
    type_counts = types_exploded['类型'].value_counts().head(15)  # 取前15个类型

    bars = ax.bar(type_counts.index, type_counts.values, color='#4CAF50', alpha=0.8)
    ax.set_xlabel('电影类型', fontsize=12)
    ax.set_ylabel('电影数量', fontsize=12)
    ax.set_title('不同类型电影的数量统计（Top 15）', fontsize=16, fontweight='bold')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, linestyle=':', alpha=0.5, axis='y')

    # 在柱状图上添加数值标签
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', fontsize=8)


def plot_movies_by_rating(movies_data, ax):
    """绘制电影评分分布的饼图"""
    rating_counts = movies_data['评分'].value_counts().sort_index()

    # 定义颜色映射
    colors = plt.cm.Set3(np.linspace(0, 1, len(rating_counts)))

    wedges, texts, autotexts = ax.pie(
        rating_counts.values,
        labels=rating_counts.index.astype(str),
        autopct='%1.1f%%',
        shadow=True,
        startangle=90,
        colors=colors,
        pctdistance=0.85
    )

    ax.set_title('电影不同评分比例分布', fontsize=16, fontweight='bold')

    # 优化百分比文字大小
    for autotext in autotexts:
        autotext.set_fontsize(8)


def main():
    """主函数：执行所有数据分析和可视化"""
    # 设置数据文件路径
    data_file = "D:\\BaiduNetdiskDownload\\数据分析\\movies.csv"

    # 检查文件是否存在
    if not Path(data_file).exists():
        print(f"错误：找不到数据文件 {data_file}")
        return

    # 加载和清洗数据
    print("正在加载数据...")
    movies_data = load_and_clean_data(data_file)
    print(f"数据加载完成，共 {len(movies_data)} 条记录")

    # 全局设置中文字体
    plt.rcParams['font.family'] = 'KaiTi'
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.dpi'] = 100

    # 创建画布
    fig = plt.figure(figsize=[16, 12])

    # 绘制四个子图
    print("正在生成图表...")

    ax1 = plt.subplot(2, 2, 1)
    plot_movies_by_year(movies_data, ax1)

    ax2 = plt.subplot(2, 2, 2)
    plot_movies_by_type(movies_data, ax2)

    ax3 = plt.subplot(2, 2, 3)
    plot_movies_by_language(movies_data, ax3)

    ax4 = plt.subplot(2, 2, 4)
    plot_movies_by_rating(movies_data, ax4)

    # 自动调整布局
    plt.tight_layout()

    # 保存图表
    output_path = '电影数据分析报告.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"图表已保存至：{output_path}")

    # 显示图表
    plt.show()
    print("分析完成！")


if __name__ == '__main__':
    main()
