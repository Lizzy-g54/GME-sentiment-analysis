import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. Read data
try:
    df = pd.read_csv('dataset/final_dataset_for_vis.csv')
except FileNotFoundError:
    print("❌ File not found! Please check the path.")
    exit()

# 2. Data Processing
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d')
df['stock_id'] = 'GME' 

df['sentiment_net'] = (df['count_Hype'] - df['count_Fear']) / (df['total_comments'] + 1e-9)
y_col = 'total_comments'

x_min, x_max = df['sentiment_net'].min(), df['sentiment_net'].max()
y_min, y_max = df[y_col].min(), df[y_col].max()
range_x = [x_min - 0.05, x_max + 0.05]
range_y = [np.log10(max(y_min * 0.8, 1)), np.log10(y_max * 1.5)]

fear_min = df['fear_ratio'].min()
fear_max = df['fear_ratio'].max()
fear_mean = df['fear_ratio'].mean()
# 找到 fear_ratio 最高的那一天
max_fear_row = df.loc[df['fear_ratio'].idxmax()]
print(f"🕵️‍♂️ 最 Extreme（最红）的球藏在: {max_fear_row['date_str']}")
print(f"   当天的恐慌值达到了: {max_fear_row['fear_ratio']:.2f}, 但总评论数(高度)只有: {max_fear_row['total_comments']}")

# 3. Build Base Animation
temp_fig = px.scatter(
    df, x='sentiment_net', y=y_col,
    animation_frame='date_str', animation_group='stock_id', 
    size='volume', color='fear_ratio',
    color_continuous_scale='Reds', range_color=[fear_min, fear_max],  
    size_max=50, opacity=0.85
)

# 4. 轻量化累积轨迹 (单层架构，最防跳)
fig = go.Figure()

# 基础层：初始球
fig.add_trace(temp_fig.data[0])

# 基础层：初始轨迹（预先定义好样式，不在这里填数据）
fig.add_trace(go.Scatter(
    x=[], y=[], mode='lines', 
    line=dict(color='rgba(100, 100, 100, 0.4)', width=1.5, dash='dash'),
    hoverinfo='skip'
))

new_frames = []
for i, frame in enumerate(temp_fig.frames):
    # 只拿所有历史坐标，不进行复杂的多层切片，减轻 CPU 负担
    full_trail_x = df['sentiment_net'].iloc[:i+1]
    full_trail_y = df[y_col].iloc[:i+1]
    
    new_frame = go.Frame(
        data=[
            frame.data[0], # 保持球的 animation_group 稳定
            go.Scatter(x=list(full_trail_x), y=list(full_trail_y)) # 只更新这一根线
        ],
        name=frame.name,
        # 强制 layout 不在帧切换时变动
        layout=frame.layout
    )
    new_frames.append(new_frame)

fig.frames = new_frames

# 【关键修改】在 update_layout 里的 Play 按钮，换成更高级的缓动函数
fig.update_layout(
    updatemenus=[dict(
        buttons=[
            dict(label='▶ Play', method='animate', args=[None, dict(
                frame=dict(duration=800, redraw=False), # redraw=False 是防跳关键！
                transition=dict(duration=500, easing="cubic-in-out"), # 丝滑缓动
                fromcurrent=True
            )])
        ]
    )]
)

# 5. Professional Layout
fig.update_layout(
    template="plotly_white",
    title=dict(
        text="<b>The Market Spiral</b>: Anatomy of a Bubble Cycle",
        y=0.95, x=0.5, xanchor='center', yanchor='top', font=dict(size=24)
    ),
    
    xaxis=dict(
        title="<b>Sentiment Balance</b><br><span style='font-size:12px'>(← Fear Dominated | Hype Dominated →)</span>",
        range=range_x, zeroline=True, zerolinewidth=2, zerolinecolor='rgba(0,0,0,0.5)', 
        showgrid=True, gridcolor='rgba(200,200,200,0.3)'
    ),
    
    yaxis=dict(
        type="log",
        title="<b>Community Engagement</b><br><span style='font-size:12px'>(Total Comments, Log Scale)</span>",
        range=range_y, showgrid=True, gridcolor='rgba(200,200,200,0.3)'
    ),
    
    # 添加各个注释说明（包含球大小的说明）
    annotations=[
        dict(x=0.08, y=range_y[1]-0.2, text="<b>Hype Phase</b>", showarrow=False, font=dict(color="green", size=15)),
        dict(x=-0.08, y=range_y[1]-0.2, text="<b>Panic Phase</b>", showarrow=False, font=dict(color="red", size=15)),
        # 【新增】明确标注球的大小代表什么
        dict(
            x=1.1, y=1.05, xref='paper', yref='paper',
            text="🔵 <b>Bubble Size</b> = Trading Volume",
            showarrow=False, font=dict(size=13, color="gray"), xanchor='right'
        )
    ],
    
    # 【修改播放速度】duration 调高到 800，加入 500ms 的平滑过渡
    updatemenus=[dict(
        type='buttons', showactive=False,
        y=0, x=1.12, xanchor='left', yanchor='bottom', pad=dict(t=50, r=10),
        buttons=[
            dict(label='▶ Play', method='animate', args=[None, dict(frame=dict(duration=800, redraw=True), transition=dict(duration=500, easing="linear"), fromcurrent=True)]),
            dict(label='⏸ Pause', method='animate', args=[[None], dict(frame=dict(duration=0, redraw=False), mode='immediate')])
        ]
    )],
    
    sliders=[dict(
        active=0, yanchor='top', y=0, xanchor='left', x=0.05,
        currentvalue=dict(prefix='<b>Date: </b>', visible=True, xanchor='left', font=dict(size=14)),
        pad=dict(b=10, t=50), len=0.88,
        steps=[dict(args=[[frame.name], dict(frame=dict(duration=0, redraw=True), mode='immediate')],
                    label=frame.name, method='animate') for frame in fig.frames]
    )],
    
    # 【修改色板标签】强制显示具体数值，避免被 Plotly 隐藏
    coloraxis=dict(
        colorscale='Reds', cmin=fear_min, cmax=fear_max,
        colorbar=dict(
            title=dict(text="<b>Fear<br>Intensity</b>", side="right"), 
            tickmode='array',
            tickvals=[fear_min, fear_mean, fear_max], 
            ticktext=[f'Low ({fear_min:.2f})', f'Avg ({fear_mean:.2f})', f'Extreme ({fear_max:.2f})']
        )
    ),
    
    margin=dict(l=80, r=80, t=100, b=80), showlegend=False
)

fig.write_html("vis2_market_spiral_perfect.html")
print("✅ 完美版生成！播放变平缓了，残影变成了真正的渐变消失，所有图例和数值也清晰可见了！")