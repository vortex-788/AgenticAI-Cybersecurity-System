#!/usr/bin/env python3
"""
Simple HTTP Server for AgenticAI Cybersecurity System
Serves the frontend and provides CORS headers
"""
import http.server
import socketserver
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        return super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == "__main__":
    PORT = 8080
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"  AgenticAI Frontend Server")
        print(f"{'='*60}")
        print(f"\n✓ Frontend serving at: http://localhost:{PORT}")
        print(f"✓ Open your browser and navigate to: http://localhost:{PORT}\n")
        print(f"Press Ctrl+C to stop the server\n")
        print(f"{'='*60}\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nServer stopped.")
            sys.exit(0)
