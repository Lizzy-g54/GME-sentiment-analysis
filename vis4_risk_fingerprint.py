import pandas as pd
import plotly.graph_objects as go

# 1. 极简数据准备
df = pd.read_csv('dataset/final_dataset_for_vis.csv').dropna()
# 🌟 排序：让高风险（红色）的线画在最上面，视觉冲击力最强
df = df.sort_values(by='volatility', ascending=True)

# 2. 轴的逻辑重排：情绪 -> 热度 -> 交易 -> 风险
dimensions = [
    dict(range=[0, 1], label='<b>Sentiment (Fear)</b>', values=df['fear_ratio']),
    dict(range=[df['count_Hype'].min(), df['count_Hype'].max()], label='<b>Hype Volume</b>', values=df['count_Hype']),
    dict(range=[df['total_comments'].min(), df['total_comments'].max()], label='<b>Social Activity</b>', values=df['total_comments']),
    dict(range=[df['volume'].min(), df['volume'].max()], label='<b>Trading Volume</b>', values=df['volume']),
    dict(range=[df['volatility'].min(), df['volatility'].max()], label='<b>Market Risk (Vol)</b>', values=df['volatility'])
]

# 3. 绘图
fig = go.Figure(data=go.Parcoords(
    line = dict(
        color = df['volatility'],
        colorscale = 'RdYlBu_r', # 红黄蓝
        showscale = True,
        cmin = df['volatility'].quantile(0.05), # 过滤极端值，颜色更分明
        cmax = df['volatility'].quantile(0.95),
        colorbar = dict(title='Volatility')
    ),
    dimensions = dimensions,
    labelfont = dict(size=14, family="Arial Black"),
    rangefont = dict(size=10)
))

fig.update_layout(
    title="<b>The Anatomy of Volatility</b>: Multi-dimensional Risk Analysis",
    # 🌟 魔法在这里：换成极客黑背景，细线瞬间变成发光的霓虹灯
    plot_bgcolor='#1a1a1a', 
    paper_bgcolor='#1a1a1a',
    font=dict(color='white'), # 文字变成白色
    margin=dict(l=80, r=80, t=100, b=80)
)

fig.write_html("vis4_risk_fingerprint.html")