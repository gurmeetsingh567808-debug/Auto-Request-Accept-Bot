from pyrogram import Client
from pyrogram.types import ChatJoinRequest
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# ====== TELEGRAM CONFIG ======
API_ID = int(os.getenv("API_ID", "39782795"))
API_HASH = os.getenv("API_HASH", "0ef198353fe6021fb9a3c3600069556b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_HERE")

# ====== FAKE WEB SERVER ======
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_web():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# ====== TELEGRAM BOT ======
app = Client(
    "auto_accept_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_chat_join_request()
async def auto_accept(client, request: ChatJoinRequest):
    await request.approve()

# ====== START BOTH ======
print("🤖 Bot + Web Service Running...")

threading.Thread(target=run_web).start()
app.run()