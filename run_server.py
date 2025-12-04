import sys
import os
from pathlib import Path

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from app.main import app
import uvicorn

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  AgenticAI Backend API Server")
    print("="*60)
    print("\n✓ Starting FastAPI server...")
    print("✓ API available at: http://localhost:8000")
    print("✓ API docs at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n" + "="*60 + "\n")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
