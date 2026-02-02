# backend/data_loader.py
"""数据加载模块"""

import json
from langchain_core.documents import Document
from typing import List

def load_trump_tweets(
    filepath: str, 
    max_tweets: int = None,
    filter_retweets: bool = True,
    min_favorites: int = 0
) -> List[Document]:
    """
    加载Trump推文数据
    
    Args:
        filepath: JSON文件路径
        max_tweets: 最多加载多少条推文
        filter_retweets: 是否过滤转发
        min_favorites: 最小点赞数（筛选热门推文）
        
    Returns:
        Document列表
    """
    print(f"📄 Loading tweets from {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ Found {len(data):,} tweets in file")
    
    # 过滤处理
    filtered_data = []
    
    for item in data:
        # 过滤转发
        if filter_retweets:
            # 检查 isRetweet 字段
            if item.get('isRetweet') == 't':
                continue
            # 检查文本是否以 RT 开头
            text = item.get('text', '')
            if text.startswith('RT @'):
                continue
        
        # 过滤低点赞
        if min_favorites > 0:
            favorites = item.get('favorites', 0)
            if isinstance(favorites, str):
                try:
                    favorites = int(favorites)
                except:
                    favorites = 0
            if favorites < min_favorites:
                continue
        
        filtered_data.append(item)
    
    print(f"📊 After filtering: {len(filtered_data):,} tweets")
    
    # 限制数量
    if max_tweets:
        filtered_data = filtered_data[:max_tweets]
        print(f"✂️  Using first {len(filtered_data):,} tweets")
    
    # 提取文本并创建Documents
    tweets = []
    for item in filtered_data:
        text = item.get('text', '').strip()
        
        if text and len(text) > 10:
            tweets.append(Document(
                page_content=text,
                metadata={
                    'date': item.get('date', ''),
                    'favorites': item.get('favorites', 0),
                    'retweets': item.get('retweets', 0),
                    'device': item.get('device', ''),
                    'id': item.get('id', '')
                }
            ))
    
    print(f"✅ Loaded {len(tweets):,} valid tweets")
    
    return tweets