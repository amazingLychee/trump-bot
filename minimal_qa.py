# quick_start.py
import json
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

print("📄 加载JSON...")

# 读取JSON
with open('data/trump_tweets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"✅ 加载了 {len(data):,} 条推文")

# 智能提取文本（尝试常见字段名）
print("\n🔍 提取推文内容...")
tweets = []

for item in data:
    # 尝试找到文本字段
    text = None
    for field in ['text', 'content', 'tweet', 'full_text', 'body']:
        if field in item and item[field]:
            text = str(item[field]).strip()
            break
    
    # 如果找到有效文本
    if text and len(text) > 10:
        tweets.append(Document(page_content=text))

print(f"✅ 提取了 {len(tweets):,} 条有效推文")

# 使用前5000条（避免太慢）
tweets = tweets[:5000]
print(f"📊 使用前 {len(tweets):,} 条")

# 创建Trump Bot
print("\n🤖 创建Trump Bot...")

vectorstore = Chroma.from_documents(
    documents=tweets,
    embedding=OpenAIEmbeddings()
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

prompt = ChatPromptTemplate.from_template("""
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

Respond as Trump would:""")

llm = ChatOpenAI(model="gpt-4", temperature=0.8)

def format_tweets(docs):
    return "\n\n".join([doc.page_content for doc in docs])

chain = (
    {"context": retriever | format_tweets, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("✅ Trump Bot 准备就绪！\n")
print("="*60)

# 测试
def chat(question):
    print(f"\n👤 You: {question}")
    print("🤔 Trump is thinking...\n")
    response = chain.invoke(question)
    print(f"🗣️  Trump: {response}\n")
    print("-"*60)
    return response

# 运行几个测试
chat("What do you think about artificial intelligence?")
chat("How should we handle the economy?")
chat("What's your opinion on social media?")

print("\n🎉 Trump Bot 测试完成！")