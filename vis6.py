import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 1. 读取并准备数据
df = pd.read_csv('dataset/final_dataset_for_vis.csv').dropna()
df['date'] = pd.to_datetime(df['date'])

# 🌟 排序：让高风险（红色）的线画在最上面
df = df.sort_values(by='volatility', ascending=True)

# 预先找到全局的最小值，固定坐标轴底部，不让底部乱跳
min_fear = df['fear_ratio'].min()
min_hype = df['count_Hype'].min()
min_soc = df['total_comments'].min()
min_vol = df['volume'].min()
min_vola = df['volatility'].min()
max_vola_global = df['volatility'].max()

# 2. 初始化图形：全白背景 + 纯红饱和度颜色带 (Reds)
fig = go.Figure(data=go.Parcoords(
    line=dict(
        color=df['volatility'],
        colorscale='Reds', # 纯红色饱和度渐变
        showscale=True,
        cmin=min_vola,
        cmax=max_vola_global,
        colorbar=dict(title='Risk Volatility', tickfont=dict(color='black'), titlefont=dict(color='black'))
    ),
    dimensions=[
        dict(range=[min_fear, df['fear_ratio'].max()], label='Sentiment (Fear)', values=df['fear_ratio']),
        dict(range=[min_hype, df['count_Hype'].max()], label='Hype Volume', values=df['count_Hype']),
        dict(range=[min_soc, df['total_comments'].max()], label='Social Activity', values=df['total_comments']),
        dict(range=[min_vol, df['volume'].max()], label='Trading Volume', values=df['volume']),
        dict(range=[min_vola, max_vola_global], label='Market Risk (Vol)', values=df['volatility'])
    ],
    labelfont=dict(size=13, family="Arial Black", color="black"),
    tickfont=dict(size=11, color="#333"),
    rangefont=dict(size=10, color="#666")
))

# 3. 构建基于“色带数值（Volatility）”的解压滑块
# 我们将最大波动率到最小波动率分成 30 个挡位
thresholds = np.linspace(max_vola_global, min_vola + 0.1, 30)
steps = []

for thresh in thresholds:
    # 🌟 核心：过滤掉波动率超过当前阈值的那些极端的日子
    sub_df = df[df['volatility'] <= thresh].copy()
    
    if sub_df.empty:
        continue
        
    # 动态计算剩余数据的最高点！
    max_fear = sub_df['fear_ratio'].max()
    max_hype = sub_df['count_Hype'].max()
    max_soc = sub_df['total_comments'].max()
    max_vol = sub_df['volume'].max()
    max_vola = sub_df['volatility'].max()
    
    # 防止因为数据过少导致范围归零报错
    max_hype = max_hype if max_hype > min_hype else min_hype + 1
    max_soc = max_soc if max_soc > min_soc else min_soc + 1
    max_vol = max_vol if max_vol > min_vol else min_vol + 1
    max_vola = max_vola if max_vola > min_vola else min_vola + 0.01

    # 动态更新各轴的最大值，实现“不再拥挤”的解压效果
    dim_update = [
        dict(range=[min_fear, max_fear], label='Sentiment (Fear)', values=list(sub_df['fear_ratio'])),
        dict(range=[min_hype, max_hype], label='Hype Volume', values=list(sub_df['count_Hype'])),
        dict(range=[min_soc, max_soc], label='Social Activity', values=list(sub_df['total_comments'])),
        dict(range=[min_vol, max_vol], label='Trading Volume', values=list(sub_df['volume'])),
        dict(range=[min_vola, max_vola], label='Market Risk (Vol)', values=list(sub_df['volatility']))
    ]
    
    step = dict(
        method="restyle",
        args=[
            {"dimensions": [dim_update], "line.color": [list(sub_df['volatility'])], "line.cmax": [max_vola]}
        ],
        label=f"{thresh:.1f}" # 滑块上显示当前的阈值
    )
    steps.append(step)

# 4. 界面布局 (纯白背景)
fig.update_layout(
    plot_bgcolor='white', 
    paper_bgcolor='white',
    margin=dict(l=60, r=80, t=60, b=80),
    sliders=[dict(
        active=0, # 初始状态为最高阈值（显示全部数据）
        currentvalue={"prefix": "<b>Max Volatility Threshold: </b>", "font": {"color": "#d63031", "size": 16}},
        pad={"t": 40},
        steps=steps
    )]
)

fig.write_html("vis6_fingerprint.html")
print("✅ Vis 6 已生成！滑动条现在基于色带最大值进行过滤，可完美释放底层被压缩的日常数据。")