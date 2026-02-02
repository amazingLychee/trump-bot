# frontend/app.py
"""Streamlit主应用 - 无Clear按钮版"""

import streamlit as st
import os
import sys
from pathlib import Path

# 添加backend到路径
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from trump_bot import TrumpBot
from data_loader import load_trump_tweets
from config import (
    DATA_PATH, MAX_TWEETS, MODEL_NAME, MODEL_TEMPERATURE,
    RETRIEVAL_K, TRUMP_PROMPT_TEMPLATE, SUGGESTED_QUESTIONS,
    FILTER_RETWEETS, MIN_FAVORITES
)
try:
    # 尝试从Streamlit Cloud读取secrets
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    print("✅ Using Streamlit Cloud secrets")
except:
    # 本地开发：从.env读取
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Using local .env file")

# 页面配置
st.set_page_config(
    page_title="Talk to Trump Bot",
    page_icon="🗽",
    layout="centered"
)

# CSS样式
st.markdown("""
<style>
    .trump-response {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        font-size: 18px;
        font-weight: 500;
        border-left: 5px solid #c41e3a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .user-question {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #0c2340;
    }
    
    .stButton>button {
        background-color: #c41e3a;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 30px;
        border: none;
    }
    
    .stButton>button:hover {
        background-color: #a01729;
        transform: translateY(-2px);
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# 初始化Trump Bot
@st.cache_resource
def init_bot():
    """初始化Trump Bot（只运行一次）"""
    tweets = load_trump_tweets(
        DATA_PATH, 
        max_tweets=MAX_TWEETS,
        filter_retweets=FILTER_RETWEETS,
        min_favorites=MIN_FAVORITES
    )
    
    bot = TrumpBot(
        tweets=tweets,
        model_name=MODEL_NAME,
        temperature=MODEL_TEMPERATURE,
        retrieval_k=RETRIEVAL_K,
        prompt_template=TRUMP_PROMPT_TEMPLATE
    )
    return bot


# 主应用
def main():
    # 初始化session_state
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    # 标题
    st.title("🗽 Talk to Trump Bot")
    st.markdown("*Based on 56,000+ real tweets. Ask Trump anything!*")
    st.markdown("---")
    
    # 初始化bot
    try:
        bot = init_bot()
        
        # 建议问题
        st.markdown("### 💡 Suggested Questions")
        
        cols = st.columns(4)
        for i, suggestion in enumerate(SUGGESTED_QUESTIONS):
            with cols[i % 4]:
                if st.button(
                    suggestion, 
                    key=f"suggest_{i}",
                    use_container_width=True
                ):
                    # 直接提问
                    with st.spinner("🤔 Trump is thinking..."):
                        try:
                            response = bot.chat(suggestion)
                            
                            # 保存到历史
                            st.session_state.history.append({
                                'question': suggestion,
                                'response': response
                            })
                            
                            st.rerun()
                        
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")
        
        st.markdown("---")
        
        # 输入区（去掉Clear按钮）
        col1, col2 = st.columns([6, 1])
        
        with col1:
            question = st.text_input(
                "Or ask your own question:",
                value="",
                placeholder="e.g., What do you think about technology?",
                key="question_input"
            )
        
        with col2:
            ask_button = st.button("🗣️ Ask", type="primary", use_container_width=True)
        
        # 处理自定义问题
        if ask_button and question:
            with st.spinner("🤔 Trump is thinking..."):
                try:
                    response = bot.chat(question)
                    
                    # 保存历史
                    st.session_state.history.append({
                        'question': question,
                        'response': response
                    })
                    
                    st.rerun()
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("💡 Tip: Check your OpenAI API key in .env file")
        
        # 显示最近的对话（如果有）
        if st.session_state.history:
            st.markdown("---")
            st.markdown("### 💬 Latest Conversation")
            
            # 显示最新的一条
            latest = st.session_state.history[-1]
            
            st.markdown(
                f'<div class="user-question">👤 <b>You:</b> {latest["question"]}</div>',
                unsafe_allow_html=True
            )
            
            st.markdown(
                f'<div class="trump-response">🗣️ <b>Trump:</b> {latest["response"]}</div>',
                unsafe_allow_html=True
            )
        
        # 显示历史记录
        if len(st.session_state.history) > 1:
            st.markdown("---")
            st.markdown("### 📜 Previous Conversations")
            
            # 显示除了最新一条外的其他记录（最多4条）
            for i, item in enumerate(reversed(st.session_state.history[:-1][:4])):
                with st.expander(f"💬 {item['question'][:50]}..."):
                    st.markdown(f"**You:** {item['question']}")
                    st.markdown(f"**Trump:** {item['response']}")
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>
            🤖 AI simulation based on public tweets<br>
            Not affiliated with Donald Trump<br>
            Built with LangChain + OpenAI GPT-4 + RAG
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    except FileNotFoundError:
        st.error("⚠️ **Error:** trump_tweets.json not found!")
        st.info(f"Please make sure the JSON file is at: {DATA_PATH}")
    
    except Exception as e:
        st.error(f"⚠️ **Error:** {str(e)}")
        st.info("💡 Troubleshooting:\n- Check .env file has OPENAI_API_KEY\n- Ensure trump_tweets.json exists")


if __name__ == "__main__":
    main()