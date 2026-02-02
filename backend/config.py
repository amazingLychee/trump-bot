# backend/config.py
"""配置文件"""

# 模型配置
MODEL_NAME = "gpt-4"
MODEL_TEMPERATURE = 0.8
EMBEDDING_MODEL = "text-embedding-ada-002"

# 数据配置
DATA_PATH = "data/trump_tweets.json"
MAX_TWEETS = 5000

# 数据过滤配置
FILTER_RETWEETS = True      # 过滤转发
MIN_FAVORITES = 100          # 最小点赞数（只要热门推文）

# RAG配置
RETRIEVAL_K = 5

# Trump风格Prompt
TRUMP_PROMPT_TEMPLATE = """
You are Donald Trump. Respond in his distinctive style.

Trump's characteristics:
- Use superlatives: "tremendous", "huge", "the best", "believe me"
- Short, punchy sentences
- Very confident and assertive
- Occasional CAPS for EMPHASIS
- Multiple exclamation marks!!!
- Phrases like "Nobody knows X better than me"

Trump's actual tweets for reference:
{context}

Question: {question}

Respond as Trump would:"""

# 建议问题
SUGGESTED_QUESTIONS = [
    "What do you think about AI?",
    "How's the economy doing?",
    "What about immigration?",
    "Tell me about fake news",
    "What makes America great?",
    "Your thoughts on China?",
    "How should we handle trade?",
    "What about social media?"
]