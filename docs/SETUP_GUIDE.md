# 🛠️ Setup Guide

Quick setup instructions for the Healthcare AI Chatbot.

## 📋 Prerequisites

### Required Software
- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **Node.js 16 or higher** ([Download](https://nodejs.org/))
- **Git** ([Download](https://git-scm.com/downloads))
- **Code Editor** (VS Code recommended)

### Required Accounts
- **OpenAI Account** for API access ([Sign up](https://platform.openai.com/))

## 🚀 Installation Steps

### Step 1: Project Setup
```bash
# Clone the repository
git clone <repository-url>
cd "HealthCare ChatBot"

# Verify project structure
dir  # Windows
ls   # Linux/Mac
```

Expected structure:
```
HealthCare ChatBot/
├── .env.example
├── README.md
├── backend/
├── frontend/
└── docs/
```

### Step 2: Environment Configuration
```bash
# Copy environment template
copy .env.example .env   # Windows
cp .env.example .env     # Linux/Mac
```

Edit the `.env` file:
```env
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

**Getting your OpenAI API Key:**
1. Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Click "Create new secret key"
3. Copy the generated key (starts with `sk-`)
4. Paste it in your `.env` file

### Step 3: Backend Setup (Python)

#### Windows
```powershell
cd backend
./start.ps1
```

#### Manual Setup (All Platforms)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
cd app
python main.py
```

**Expected Output:**
```
🏥 Healthcare Chatbot Backend Starting...
OpenAI API Available: True
Conversations will be stored at: ../conversations.json
INFO:     Started server process [xxxxx]
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 4: Frontend Setup (React)
Open a **new terminal/command prompt**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

### Step 5: Verification
1. **Backend**: Visit [http://localhost:8000](http://localhost:8000)
   - Should show: `{"message": "Healthcare Chatbot API is running"}`

2. **Frontend**: Visit [http://localhost:3000](http://localhost:3000)
   - Should show the chat interface with welcome message

3. **Integration Test**: 
   - Type "I have a headache" in the chat
   - Should receive healthcare advice

## 🔧 Configuration Options

### Backend Configuration
File: `backend/app/main.py`

```python
# Server settings
HOST = "0.0.0.0"  # Bind to all interfaces
PORT = 8000       # Server port

# CORS settings (for frontend)
allow_origins = ["http://localhost:3000"]

# OpenAI settings
MODEL = "gpt-4"           # AI model to use
MAX_TOKENS = 300          # Response length limit
TEMPERATURE = 0.7         # Response creativity (0-2)
```

### Frontend Configuration
File: `frontend/src/App.tsx`

```typescript
// API endpoint
const API_BASE_URL = 'http://localhost:8000';

// UI settings
const AUTO_SCROLL = true;          // Auto-scroll to new messages
const TYPING_DELAY = 500;          // Typing indicator delay (ms)
const MAX_MESSAGE_LENGTH = 500;    // Input character limit
```

## 🧪 Testing the Setup

### Basic Tests
1. **Backend Health Check**
   ```bash
   curl http://localhost:8000/health
   ```

2. **API Test**
   ```bash
   curl -X POST http://localhost:8000/diagnose \
     -H "Content-Type: application/json" \
     -d '{"symptoms": "headache"}'
   ```

3. **Frontend Build Test**
   ```bash
   cd frontend
   npm run build
   ```

### Integration Tests
1. **Chat Functionality**: Send various symptoms
2. **Error Handling**: Stop backend, test frontend error handling
3. **Mobile Responsive**: Test on different screen sizes
4. **Severity Detection**: Test mild vs serious symptoms

## 🐛 Common Issues & Solutions

### Python Issues

**Error: `python: command not found`**
```bash
# Windows - Install from python.org
# Check installation:
python --version

# Linux/Ubuntu
sudo apt update && sudo apt install python3 python3-pip

# Mac
brew install python3
```

**Error: `pip install fails`**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with user flag
pip install --user -r requirements.txt
```

**Error: Virtual environment activation fails**
```bash
# Windows - Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Alternative activation method
python venv\Scripts\activate.py  # Windows
python venv/bin/activate         # Linux/Mac
```

### Node.js Issues

**Error: `npm: command not found`**
- Install Node.js from [nodejs.org](https://nodejs.org/)
- Verify: `node --version` and `npm --version`

**Error: `npm install fails`**
```bash
# Clear cache
npm cache clean --force

# Use different registry
npm install --registry https://registry.npmjs.org/

# Delete and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: Port 3000 already in use**
```bash
# Kill process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Linux/Mac:
lsof -ti:3000 | xargs kill -9

# Or use different port
PORT=3001 npm start
```

### API Issues

**Error: OpenAI API key invalid**
- Check key format (starts with `sk-`)
- Verify key is active on OpenAI dashboard
- Check account credits/billing

**Error: CORS blocked**
- Ensure backend allows frontend origin
- Check firewall settings
- Verify backend is running on correct port

### CSS/Frontend Issues

**Error: CSS not loading**
- Check `App.css` for syntax errors
- Look for missing semicolons or braces
- Restart development server

**Error: TypeScript compilation fails**
- Check for type errors
- Verify all imports are correct
- Run `npm install` to ensure dependencies

## 🏗️ Development Environment

### Recommended VS Code Extensions
- Python
- TypeScript and JavaScript Language Features
- React snippets
- REST Client (for API testing)
- GitLens

### Environment Variables
Create `.env` file in project root:
```env
# Required
OPENAI_API_KEY=sk-your-key-here

# Optional
BACKEND_HOST=localhost
BACKEND_PORT=8000
FRONTEND_PORT=3000
NODE_ENV=development
```

### Port Configuration
- Backend: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Ensure these ports are not blocked by firewall

## 📱 Mobile Testing

### Browser Testing
- Chrome DevTools mobile simulation
- Firefox Responsive Design Mode
- Safari Web Inspector

### Real Device Testing
1. Connect devices to same network
2. Use network IP instead of localhost
3. Example: `http://192.168.1.100:3000`

## 🚀 Production Deployment

### Backend (FastAPI)
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

### Frontend (React)
```bash
cd frontend

# Build for production
npm run build

# Serve build folder
npm install -g serve
serve -s build -p 3000
```

## 🔒 Security Checklist

- [ ] API key stored in environment variables only
- [ ] `.env` file added to `.gitignore`
- [ ] CORS properly configured for your domain
- [ ] HTTPS enabled in production
- [ ] Input validation implemented
- [ ] Rate limiting configured
- [ ] Error messages don't expose sensitive data

## 📞 Support

If you encounter issues:
1. Check this setup guide
2. Review error messages carefully  
3. Search existing issues
4. Create new issue with:
   - Operating system
   - Python/Node versions
   - Full error message
   - Steps to reproduce

---

**Next Steps**: After successful setup, see `API_REFERENCE.md` for detailed API documentation.