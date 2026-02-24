import pandas as pd
import plotly.graph_objects as go

# 1. Read and prepare data
try:
    df = pd.read_csv('dataset/final_dataset_for_vis.csv')
    # Extract the core dimensions along with the 'date' column, dropping any empty rows
    cols = ['date', 'fear_ratio', 'count_Hype', 'total_comments', 'volume', 'volatility']
    df = df[cols].dropna()
except FileNotFoundError:
    print("❌ File not found! Please ensure the CSV file is in the specified directory.")
    exit()

# 2. Prepare hover text to display the date interactively
hover_text = df['date'].apply(lambda x: f"<b>Date: {x}</b>")

# 3. Calculate the 90th percentile for volatility to cap the color scale
color_max_limit = df['volatility'].quantile(0.90)

# 4. Create the Scatter Plot Matrix (SPLOM)
# 这里定义了 fig，所以后面的导出代码才能认出它！
fig = go.Figure(data=go.Splom(
    dimensions=[
        dict(label='<b>Fear Sentiment</b>', values=df['fear_ratio']),
        dict(label='<b>Hype Posts</b>', values=df['count_Hype']),
        dict(label='<b>Social Attention</b>', values=df['total_comments']),
        dict(label='<b>Trading Volume</b>', values=df['volume']),
        dict(label='<b>Market Risk</b><br>(Volatility)', values=df['volatility'])
    ],
    text=hover_text,
    hovertemplate="%{text}<br>X: %{x}<br>Y: %{y}<extra></extra>",
    marker=dict(
        color=df['volatility'],    
        colorscale='Reds',     
        showscale=True,
        cmax=color_max_limit, 
        cmin=df['volatility'].min(),
        colorbar=dict(title="Market Risk<br>(Volatility)", thickness=15),
        size=7,                    
        opacity=0.7,               
        line=dict(width=0.5, color='white') 
    ),
    diagonal=dict(visible=False)
))

# 5. Layout and beautification
fig.update_layout(
    title=dict(
        text="<b>Risk Correlation Matrix</b>: How Social Factors Drive Market Volatility",
        font=dict(size=22),
        y=0.95, x=0.5, xanchor='center', yanchor='top'
    ),
    width=900,   
    height=900,
    plot_bgcolor='white',
    paper_bgcolor='white',
    hovermode='closest',
    margin=dict(l=80, r=80, t=100, b=80)
)

# 6. Add subtle gridlines to all internal subplots for an academic feel
for i in range(1, 6):
    fig.update_layout(**{f'xaxis{i}': dict(showgrid=True, gridcolor='#f0f0f0', zeroline=False, tickfont=dict(size=10))})
    fig.update_layout(**{f'yaxis{i}': dict(showgrid=True, gridcolor='#f0f0f0', zeroline=False, tickfont=dict(size=10))})

# 7. Export to HTML (这一步必须放在最最最底下)
output_file = "vis4_splom_final.html"

# --- 注入给 HTML 大屏通信的 JS 脚本 ---
post_js = """
console.log("✅ Vis4 iframe 内部交互脚本已成功挂载！");
var graph = document.getElementsByClassName('plotly-graph-div')[0];
graph.on('plotly_hover', function(data){
    var pt = data.points[0];
    if (pt.text) {
        var match = pt.text.match(/Date: (\\d{4}-\\d{2}-\\d{2})/);
        if (match) {
            console.log("🖱️ Vis4 探测到鼠标悬停，正则抓取到日期:", match[1]);
            window.parent.postMessage({ type: 'plotly_hover', date: match[1] }, '*');
        }
    }
});
"""

# 真正保存 HTML 的指令，带上刚才写的 post_js
fig.write_html(output_file, post_script=post_js)
print(f"✅ Interactive SPLOM chart generated successfully with Hover Sync: {output_file}")