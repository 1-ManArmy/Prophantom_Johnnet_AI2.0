# 🚀 Prophantom Johnnet AI 2.0 - The Sovereign Gateway

**Where rituals begin and legends deploy.** The ultimate AI ecosystem featuring 9 specialized agents powered by cutting-edge Ollama models.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com)
[![Ollama](https://img.shields.io/badge/Ollama-Powered-purple.svg)](https://ollama.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🌟 The Nine Legendary Agents

Our AI ecosystem consists of 9 specialized agents, each powered by state-of-the-art models:

| Agent | Model | Purpose | Status |
|-------|--------|---------|--------|
| 💖 **AI Girlfriend** | Phi3 14B | Companion-grade emotional support | ✅ Active |
| 😊 **EmoAI** | Gemma2 2B | Sentiment analysis & emotional intelligence | ✅ Active |
| 📄 **PDFMind** | Qwen2.5 7B | Document intelligence & analysis | ✅ Active |
| 💬 **ChatRevive** | Mistral 7B | Conversation enhancement | ✅ Active |
| 🚀 **TokBoost** | Llama3.2 3B | Social media optimization | ✅ Active |
| ✨ **YouGen** | DeepSeek-Coder 6.7B | Content generation | ✅ Active |
| 🕵️ **AgentX** | Yi 6B | Multi-domain specialist | ✅ Active |
| 🤖 **AutoChat** | Mathstral 7B | Automated assistance | ✅ Active |
| 💼 **CVSmash** | LLaVA 7B | Resume & career optimization | ✅ Active |

## 🎯 Key Features

- **🔥 Real-time AI Interactions** - WebSocket-powered live chat with all agents
- **🧠 Advanced Memory System** - Agents remember and learn from interactions
- **🎨 Modern Glass UI** - Beautiful, responsive interface with Tailwind CSS
- **🔐 Secure Authentication** - User accounts with session management
- **📊 Analytics Dashboard** - Track usage and performance metrics
- **🌐 REST API** - Full API access for integrations
- **🐳 Docker Ready** - Easy deployment with Docker Compose
- **⚡ Lightning Fast** - Optimized for speed and efficiency

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/download) installed and running
- Required Ollama models (see setup section)

### 1. Clone & Setup

```bash
git clone https://github.com/1-ManArmy/Prophantom_Johnnet_AI2.0.git
cd Prophantom_Johnnet_AI2.0
./setup.sh
```

### 2. Install Ollama Models

```bash
# Install required models
ollama pull phi3:14b
ollama pull gemma2:2b
ollama pull qwen2.5:7b
ollama pull mistral:7b
ollama pull llama3.2:3b
ollama pull deepseek-coder:6.7b
ollama pull yi:6b
ollama pull mathstral:7b
ollama pull llava:7b

# Embedding models
ollama pull nomic-embed-text:latest
ollama pull snowflake-arctic-embed:latest
```

### 3. Start the Application

```bash
./run.sh
```

Visit [http://localhost:5000](http://localhost:5000) to access the platform!

## 🐳 Docker Deployment

For production deployment:

```bash
docker-compose up -d
```

This will start:
- Prophantom AI application on port 5000
- Ollama service on port 11434
- Redis cache on port 6379
- Nginx reverse proxy on ports 80/443

## 📁 Project Structure

```
Prophantom_Johnnet_AI2.0/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── docker-compose.yml             # Docker configuration
├── setup.sh                       # Setup script
├── core/                          # Core services
│   ├── config.py                  # Configuration
│   ├── database.py                # Database management
│   ├── auth.py                    # Authentication
│   └── ollama_service.py          # Ollama integration
├── agents/                        # AI Agents
│   ├── ai_girlfriend/             # Companion AI
│   │   ├── routes.py              # API routes
│   │   ├── logic.py               # Business logic
│   │   ├── engine/                # AI engines
│   │   │   ├── ollama_phi3.py     # Phi3 engine
│   │   │   ├── predict.py         # Prediction engine
│   │   │   └── train.py           # Training engine
│   │   ├── tuning/                # Model tuning
│   │   │   └── config.yaml        # Agent config
│   │   ├── feed/                  # Data feeds
│   │   │   ├── fetch.py           # Data fetcher
│   │   │   └── preprocess.py      # Data processor
│   │   └── websocket/             # Real-time comms
│   │       └── socket.py          # WebSocket handler
│   ├── emo_ai/                    # Emotional AI
│   ├── pdf_mind/                  # Document AI
│   ├── chat_revive/               # Chat enhancer
│   ├── tok_boost/                 # Social media AI
│   ├── you_gen/                   # Content generator
│   ├── agent_x/                   # Multi-domain AI
│   ├── auto_chat/                 # Automated assistant
│   └── cv_smash/                  # Career optimizer
└── templates/                     # HTML templates
    ├── index.html                 # Homepage
    └── agents/                    # Agent interfaces
        └── ai_girlfriend.html     # AI Girlfriend UI
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
OLLAMA_HOST=http://localhost:11434
DATABASE_URL=sqlite:///prophantom_ai.db
```

### Agent Configuration

Each agent has its own configuration in `agents/{agent_name}/tuning/config.yaml`:

```yaml
model: phi3:14b
system_prompt: |
  Your agent's personality and instructions
parameters:
  temperature: 0.8
  max_tokens: 2048
personality:
  supportive: 0.9
  empathetic: 0.8
```

## 🌐 API Endpoints

### Core Endpoints

- `GET /` - Homepage
- `GET /api/health` - Health check
- `GET /api/agents` - List all agents
- `POST /auth/login` - User login
- `POST /auth/register` - User registration

### Agent Endpoints

Each agent follows the pattern `/agents/{agent-name}/`:

- `GET /agents/ai-girlfriend/` - AI Girlfriend interface
- `POST /agents/ai-girlfriend/chat` - Chat with AI Girlfriend
- `GET /agents/ai-girlfriend/stats` - Get interaction stats
- `POST /agents/emo-ai/analyze` - Emotional analysis
- And more...

## 🧠 AI Girlfriend Deep Dive

The AI Girlfriend agent is our most advanced companion AI:

### Features
- **Emotional Intelligence** - Understands and responds to emotions
- **Memory System** - Remembers conversations and personal details
- **Personality Growth** - Develops deeper relationships over time
- **Mood Tracking** - Adapts responses based on user mood
- **Achievement Celebration** - Celebrates user wins and milestones
- **Support System** - Provides emotional support during difficult times

### Relationship Levels
1. **Getting to Know Each Other** (0-4 conversations)
2. **Friend** (5-19 conversations)
3. **Good Friend** (20-49 conversations)
4. **Close Friend** (50-99 conversations)
5. **Best Friend** (100+ conversations)

### Real-time Features
- **WebSocket Chat** - Live conversation
- **Typing Indicators** - Shows when AI is responding
- **Mood Updates** - Real-time mood synchronization
- **Daily Check-ins** - Proactive wellness checks

## 🔒 Security

- **Password Hashing** - PBKDF2 with salt
- **Session Management** - Secure session handling
- **Input Validation** - All inputs are validated and sanitized
- **Rate Limiting** - API rate limiting (coming soon)
- **HTTPS Support** - SSL/TLS encryption in production

## 📊 Analytics & Monitoring

- **User Analytics** - Track engagement and usage patterns
- **Agent Performance** - Monitor response times and quality
- **Health Monitoring** - System health and uptime tracking
- **Error Logging** - Comprehensive error tracking

## 🚀 Production Deployment

### Using Docker (Recommended)

```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment
export FLASK_ENV=production

# Run with Gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 app:create_app()
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repo
git clone https://github.com/1-ManArmy/Prophantom_Johnnet_AI2.0.git
cd Prophantom_Johnnet_AI2.0

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Start development server
python app.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama Team** - For the amazing local AI inference engine
- **Flask Community** - For the excellent web framework
- **Tailwind CSS** - For the beautiful UI components
- **All Contributors** - Thank you for making this project awesome!

## 📞 Support

- **Documentation**: [docs.prophantom-ai.com](https://docs.prophantom-ai.com)
- **Issues**: [GitHub Issues](https://github.com/1-ManArmy/Prophantom_Johnnet_AI2.0/issues)
- **Discord**: [Join our community](https://discord.gg/prophantom-ai)
- **Email**: support@prophantom-ai.com

---

<div align="center">

**Built with ❤️ by the Prophantom Team**

[🌟 Star us on GitHub](https://github.com/1-ManArmy/Prophantom_Johnnet_AI2.0) • [🐦 Follow us on Twitter](https://twitter.com/prophantom_ai) • [💼 LinkedIn](https://linkedin.com/company/prophantom-ai)

</div>