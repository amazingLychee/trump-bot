# check_format.py
import json

with open('data/trump_tweets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*60)
print("📊 JSON文件格式检查")
print("="*60)

print(f"\n总推文数: {len(data):,}")

if data:
    first = data[0]
    
    print(f"\n📋 所有字段:")
    for key in first.keys():
        print(f"  - {key}")
    
    print(f"\n👀 第一条推文完整内容:")
    print(json.dumps(first, indent=2, ensure_ascii=False)[:1000])
    print("\n...")
    
    print(f"\n📝 前3条推文内容预览:")
    for i, tweet in enumerate(data[:3], 1):
        # 尝试找文本
        text = (tweet.get('text') or 
                tweet.get('content') or 
                tweet.get('tweet') or 
                tweet.get('full_text') or 
                'NO TEXT FOUND')
        print(f"\n推文 #{i}:")
        print(f"  {text[:100]}...")