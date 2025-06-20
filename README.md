# TweetCraft 🪄

AI-powered tweet thread generator using multi-agent architecture. Generate engaging Twitter threads with research, strategy, writing, editing, and analytics agents working together.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🚀 Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/ps-research/TweetCraft.git
cd TweetCraft
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Get API Keys**
   - [OpenAI API Key](https://platform.openai.com/api-keys) (for GPT-4o)
   - [Tavily API Key](https://tavily.com) (for web search)

## ✨ Features

- **6 AI Agents**: Research → Strategy → Writing → Editing → Quality Control → Analytics
- **Real-time Research**: Automatic web search and data synthesis
- **Quality Control**: Built-in revision system with scoring
- **Style Options**: Professional, Casual, Humorous, or Thought-provoking
- **Analytics**: Engagement predictions and optimization tips

## 🏗️ Architecture

```
Research Agent → Strategy Agent → Writer Agent → Editor Agent → Supervisor Agent → Analytics Agent
```

Each agent specializes in one aspect of thread creation, ensuring high-quality output.

## 📱 Usage

1. Enter your OpenAI and Tavily API keys
2. Choose thread length (2-7 tweets) and style
3. Enter your topic
4. Click "Generate Thread"
5. Watch the agents work in real-time
6. Copy your optimized thread

## 🛠️ Tech Stack

- **LangGraph**: Multi-agent orchestration
- **OpenAI GPT-4o**: Content generation
- **Tavily**: Web search and research
- **Streamlit**: User interface

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

**Built for content creators who want to leverage AI for better social media engagement.**
