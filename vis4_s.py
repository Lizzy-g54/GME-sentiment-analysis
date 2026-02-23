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
# This prevents extreme outliers from washing out the color gradient for the rest of the high-risk days
color_max_limit = df['volatility'].quantile(0.90)

# 4. Create the Scatter Plot Matrix (SPLOM)
fig = go.Figure(data=go.Splom(
    dimensions=[
        dict(label='<b>Fear Sentiment</b>', values=df['fear_ratio']),
        dict(label='<b>Hype Posts</b>', values=df['count_Hype']),
        dict(label='<b>Social Attention</b>', values=df['total_comments']),
        dict(label='<b>Trading Volume</b>', values=df['volume']),
        dict(label='<b>Market Risk</b><br>(Volatility)', values=df['volatility'])
    ],
    
    # Bind the hover text to the chart
    text=hover_text,
    hovertemplate="%{text}<br>X: %{x}<br>Y: %{y}<extra></extra>",
    
    # Adjust marker styling and color logic
    marker=dict(
        color=df['volatility'],    
        colorscale='Reds',     
        showscale=True,
        
        # Apply the color cap to ensure clear color clustering
        cmax=color_max_limit, 
        cmin=df['volatility'].min(),
        
        colorbar=dict(title="Market Risk<br>(Volatility)", thickness=15),
        size=7,                    
        opacity=0.7,               
        line=dict(width=0.5, color='white') 
    ),
    # Hide the diagonal plots as self-correlation is meaningless
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

# 7. Export to HTML
output_file = "vis4_splom_final.html"
fig.write_html(output_file)
print(f"✅ Interactive SPLOM chart generated successfully: {output_file}")