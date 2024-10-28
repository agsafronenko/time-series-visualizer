import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import platform
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

if platform.system == "Windows":
    os.system('cls')
else:
    os.system('clear')

df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    fig, axis = plt.subplots(figsize=(24, 8))
    axis.plot(df.index, df['value'], color='red', linewidth=1.2)
    axis.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=18)
    axis.set_xlabel('Date', fontsize=14)
    axis.set_ylabel('Page Views', fontsize=14)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month_name()
    df_bar['value'] = pd.to_numeric(df_bar['value'])
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().reset_index()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar['month'] = pd.Categorical(df_bar['month'], categories=months)
    df_bar = df_bar.sort_values(['year', 'month'])
    axis = df_bar.pivot(index='year', columns='month', values='value').plot(kind='bar', figsize=(24, 8), width=0.9)
    axis.set_title('Average Daily Page Views per Month', fontsize=18)
    axis.set_xlabel('Years', fontsize=14)
    axis.set_ylabel('Average Page Views', fontsize=14)
    axis.legend(title='Months', fontsize=16)
    fig = plt.gcf()
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(24, 8))

    sns.boxplot(data=df_box, x='year', y='value', ax=axis1, 
                palette='Set3', linewidth=1.2, fliersize=3, 
                boxprops=dict(edgecolor='black'),
                whiskerprops=dict(color='black'),
                medianprops=dict(color='black'))
    axis1.set_title('Year-wise Box Plot (Trend)', fontsize=18)
    axis1.set_xlabel('Year', fontsize=14)
    axis1.set_ylabel('Page Views', fontsize=14)

    sns.boxplot(data=df_box, x='month', y='value', ax=axis2, 
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                hue='month', palette='Set3', linewidth=1.2, fliersize=3, 
                boxprops=dict(edgecolor='black'),
                whiskerprops=dict(color='black'),
                medianprops=dict(color='black'))
    axis2.set_title('Month-wise Box Plot (Seasonality)', fontsize=18)
    axis2.set_xlabel('Month', fontsize=14)
    axis2.set_ylabel('Page Views', fontsize=14)
    fig.savefig('box_plot.png')
    return fig