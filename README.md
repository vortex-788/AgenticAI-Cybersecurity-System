# AgenticAI Cybersecurity System

AI-powered threat detection and automated response system.

## 🚀 Live Demo
- **Frontend**: https://agentic-ai-cybersecurity-system-mini-project-3af50a55.vercel.app/
- **Backend**: Deploy separately on Render (see below)

## 📋 Quick Start (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Run server
python run_server.py
```

Access at `http://localhost:8000`

## ☁️ Deploy Backend on Render

1. Create account at [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect this GitHub repository
4. Render will auto-detect `render.yaml`
5. Click "Create Web Service"
6. Copy the deployed URL (e.g., `https://your-app.onrender.com`)

## 🔗 Connect Frontend to Backend

After deploying backend, update the frontend:

1. Edit `index.html` line 449:
   ```javascript
   const API_BASE = 'https://your-backend-url.onrender.com';
   ```
2. Commit and push to GitHub
3. Vercel will auto-redeploy

## 📖 Documentation

See [PROJECT_REPORT.md](https://github.com/vortex-788/AgenticAI-Cybersecurity-System) for full details.