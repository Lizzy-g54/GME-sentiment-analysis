import pandas as pd

# 1. 读取大文件 (只加载需要的列以节省内存)
print("正在读取大文件...")
df = pd.read_csv("gme_sentiment_labeled.csv", usecols=['body', 'sentiment_label', 'score', 'timestamp'])

# 2. 处理日期：把 timestamp 转换成 YYYY-MM-DD 格式
df['date'] = pd.to_datetime(df['timestamp']).dt.strftime('%Y-%m-%d')

# 3. 排序并取精华：按日期和情绪分组，每天每种情绪只取点赞最高的前 2 条
print("正在提取精华评论...")
top_comments = df.sort_values('score', ascending=False).groupby(['date', 'sentiment_label']).head(2)

# 4. 保存为轻量级文件 (通常只有几百KB)
top_comments.to_csv("top_comments.csv", index=False)
print("处理完成！生成了 top_comments.csv")