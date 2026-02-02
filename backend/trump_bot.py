# backend/trump_bot.py
"""Trump Bot核心逻辑"""

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from typing import List

class TrumpBot:
    """Trump对话机器人"""
    
    def __init__(
        self, 
        tweets: List[Document],
        model_name: str = "gpt-4",
        temperature: float = 0.8,
        retrieval_k: int = 5,
        prompt_template: str = None
    ):
        """
        初始化Trump Bot
        
        Args:
            tweets: 推文Document列表
            model_name: 使用的模型
            temperature: 温度参数
            retrieval_k: 检索数量
            prompt_template: Prompt模板
        """
        print("🤖 Initializing Trump Bot...")
        
        self.tweets = tweets
        self.model_name = model_name
        self.temperature = temperature
        self.retrieval_k = retrieval_k
        
        # 创建向量数据库
        print("🔨 Creating vector database...")
        self.vectorstore = Chroma.from_documents(
            documents=tweets,
            embedding=OpenAIEmbeddings()
        )
        
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": retrieval_k}
        )
        
        # 创建LLM
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature
        )
        
        # 创建Prompt
        if prompt_template is None:
            prompt_template = """
You are Donald Trump. Respond in his distinctive style.

Trump's characteristics:
- Use superlatives: "tremendous", "huge", "the best"
- Short, punchy sentences
- Very confident and assertive
- Occasional CAPS for EMPHASIS
- Multiple exclamation marks!!!

Trump's tweets:
{context}

Question: {question}

Trump's response:"""
        
        self.prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # 创建Chain
        self.chain = self._create_chain()
        
        print("✅ Trump Bot ready!")
    
    def _create_chain(self):
        """创建RAG链"""
        
        def format_tweets(docs):
            return "\n\n".join([doc.page_content for doc in docs])
        
        chain = (
            {
                "context": self.retriever | format_tweets, 
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        return chain
    
    def chat(self, question: str) -> str:
        """
        与Trump Bot对话
        
        Args:
            question: 用户问题
            
        Returns:
            Trump的回答
        """
        if not question or len(question.strip()) == 0:
            raise ValueError("Question cannot be empty")
        
        response = self.chain.invoke(question)
        return response
    
    def get_stats(self) -> dict:
        """获取统计信息"""
        return {
            "total_tweets": len(self.tweets),
            "model": self.model_name,
            "temperature": self.temperature,
            "retrieval_k": self.retrieval_k
        }