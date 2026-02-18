# 🎙️ Trump Bot

[![Try it live](https://img.shields.io/badge/🚀_Try_it_live-Streamlit-FF4B4B?style=for-the-badge)](https://trump-bot-nxche3qzqfq4eujhzi62eu.streamlit.app/)

Chat with an AI-powered Donald Trump. Ask him anything — trade wars, border walls, or what he thinks about your lunch.

Built with **RAG (Retrieval-Augmented Generation)** to ground responses in real Trump speeches and statements, so the bot doesn't just sound like Trump — it knows what Trump actually said.

## Demo

> **You:** What do you think about AI?
>
> **Trump Bot:** *Let me tell you, AI is tremendous. We have the best AI, nobody does AI like us...*

## Tech Stack

| Layer | Tech |
|-------|------|
| LLM | OpenAI GPT-4 |
| RAG Framework | LangChain |
| Frontend & Backend | Streamlit |
| Data | Trump speeches & transcripts |

## Project Structure

```
trump-bot/
├── backend/          # LangChain RAG pipeline
├── frontend/         # Streamlit chat UI
├── data/             # Trump speeches & documents for RAG
├── check.py          # Data validation script
├── minimal_qa.py     # Minimal Q&A demo script
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.9+
- OpenAI API key

### Installation

```bash
# Clone the repo
git clone https://github.com/amazingLychee/trump-bot.git
cd trump-bot

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY=your_api_key_here
```

### Run

```bash
# Quick test with minimal Q&A
python minimal_qa.py

# Or start the full app
streamlit run frontend/app.py
```

Streamlit will open automatically in your browser.

## How It Works

1. **Data Ingestion** — Trump's speeches and transcripts are chunked and embedded into a vector store
2. **Retrieval** — When you ask a question, LangChain retrieves the most relevant chunks
3. **Generation** — GPT-4 generates a response in Trump's style, grounded in the retrieved context

## Disclaimer

This is a fun side project for learning RAG. The bot's responses are AI-generated and do not represent real statements from Donald Trump.
