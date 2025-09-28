# 🚀 Deployment Guide

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- Git
- OpenAI API Key (optional)

## 🏠 Local Development

```bash
# Quick start
./start-dev.ps1

# Or manual setup
cp .env.example .env  # Add your OpenAI API key

# Backend (Terminal 1)
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
cd app && python main.py

# Frontend (Terminal 2)
cd frontend
npm install
npm start
```

## ☁️ Cloud Deployment

### Free Option: Vercel + Railway

**Frontend on Vercel:**
1. Connect GitHub to [vercel.com](https://vercel.com)
2. Deploy from `frontend` folder
3. Build command: `npm run build`
4. Output directory: `build`

**Backend on Railway:**
1. Connect GitHub to [railway.app](https://railway.app)
2. Deploy from `backend` folder
3. Add environment variable: `OPENAI_API_KEY`
4. Railway will auto-detect Python and install dependencies

### Alternative: Netlify + Render

**Frontend on Netlify:**
1. Connect GitHub to [netlify.com](https://netlify.com)
2. Build command: `cd frontend && npm run build`
3. Publish directory: `frontend/build`

**Backend on Render:**
1. Connect GitHub to [render.com](https://render.com)
2. Choose Python environment
3. Build command: `cd backend && pip install -r requirements.txt`
4. Start command: `cd backend/app && python main.py`
5. Add environment variable: `OPENAI_API_KEY`

## 🔧 Environment Configuration

Create `.env` file:
```env
OPENAI_API_KEY=your-openai-api-key-here
```

Update CORS in `backend/app/main.py` for production:
```python
allow_origins=[
    "http://localhost:3000",           # Development
    "https://your-frontend-domain.com" # Production
]
```

## ✅ Deployment Checklist

- [ ] Environment variables configured
- [ ] CORS origins updated for production
- [ ] Frontend builds successfully
- [ ] Backend runs without errors
- [ ] API endpoints accessible
- [ ] SSL/HTTPS enabled (automatic on most platforms)

## 🆘 Troubleshooting

**Build Errors:**
- Check Python/Node.js versions
- Verify all dependencies installed
- Review build logs

**API Connection Issues:**
- Confirm backend is running
- Check CORS configuration
- Verify environment variables

**Performance:**
- Enable gzip compression
- Use production builds
- Consider CDN for static assets