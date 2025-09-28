# 🏥 Healthcare AI Chatbot

> **Professional AI-powered healthcare assistant with intelligent medical guidance and symptom analysis**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/React-18+-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com/)

## ✨ Features

- **🤖 AI-Powered Medical Assistance** - OpenAI GPT-4 integration with healthcare-focused responses
- **🎨 Professional UI** - Modern glassmorphism design with healthcare styling
- **⚡ Smart Fallback System** - Works even without OpenAI API key
- **📱 Responsive Design** - Optimized for desktop and mobile devices
- **🛡️ Safety First** - Medical disclaimers and severity indicators
- **💾 Conversation History** - JSON-based chat storage

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/healthcare-ai-chatbot.git
   cd healthcare-ai-chatbot
   ```

2. **Setup environment**
   ```bash
   cp .env.example .env
   # Add your OpenAI API key to .env file
   ```

3. **Start the backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cd app
   python main.py
   ```

4. **Start the frontend** (new terminal)
   ```bash
   cd frontend
   npm install
   npm start
   ```

5. **Access the application**
   
   Open [http://localhost:3000](http://localhost:3000) in your browser

## 🏗️ Project Structure

```
healthcare-ai-chatbot/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   └── main.py         # Main application
│   ├── requirements.txt    # Python dependencies
│   └── start.ps1          # Windows startup script
├── frontend/               # React TypeScript frontend
│   ├── src/
│   │   ├── App.tsx        # Main component
│   │   └── App.css        # Styling
│   └── package.json       # Node dependencies
├── docs/                  # Documentation
├── .env.example          # Environment template
├── .gitignore           # Git ignore rules
└── README.md           # This file
```

## 🔧 Configuration

Create `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-your-openai-api-key-here
```

Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## 🧪 Usage

### Test Cases
- **Mild symptoms**: "I have a headache"
- **Serious symptoms**: "chest pain and difficulty breathing"
- **General health**: "I feel tired lately"

### API Endpoints
- `GET /` - Health check
- `POST /diagnose` - Symptom analysis
- `GET /history` - Conversation history

## 🚀 Deployment

### Local Production
```bash
# Build frontend
cd frontend && npm run build

# Start backend with production server
cd backend && pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Cloud Deployment
- **Vercel** (Frontend) + **Railway** (Backend) - Free tier available
- **Netlify** (Frontend) + **Heroku** (Backend)
- **Docker** deployment ready

## 🛡️ Security

- ✅ Environment-based configuration
- ✅ API key protection
- ✅ CORS security
- ✅ Medical disclaimers
- ✅ Input validation

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Medical Disclaimer

This application provides general health information only and is not a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare providers for medical concerns.

## 🆘 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/healthcare-ai-chatbot/issues)
- 📖 **Documentation**: [Full Docs](./docs/)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/healthcare-ai-chatbot/discussions)

---

**Made with ❤️ for better healthcare accessibility**