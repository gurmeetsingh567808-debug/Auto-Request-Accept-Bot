from pyrogram import Client, filters
from pyrogram.types import (
    ChatJoinRequest,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os

# ================== CONFIG ==================
API_ID = int(os.getenv("API_ID", "39782795"))
API_HASH = os.getenv("API_HASH", "0ef198353fe6021fb9a3c3600069556b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_HERE")

# ================== FAKE WEB SERVER ==================
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

# ================== BOT ==================
app = Client(
    "auto_accept_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------- /start ----------
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🤖 **I am Request Accept Bot**\n\n"
        "➕ Mujhe **Private Group / Channel** me add karo\n"
        "🔐 Admin banao (Approve Join Requests)\n\n"
        "✅ Main **new join requests automatically accept** karta hoon.",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "➕ Add me to Group / Channel",
                    url=f"https://t.me/{client.me.username}?startgroup=true"
                )
            ]]
        )
    )

# ---------- Auto accept NEW requests ----------
@app.on_chat_join_request()
async def auto_accept(client, request: ChatJoinRequest):
    await request.approve()

    # Welcome DM
    try:
        await client.send_message(
            request.from_user.id,
            f"🎉 **Welcome {request.from_user.first_name}!**\n\n"
            "✅ Aapki join request accept ho gayi hai.\n"
            "Enjoy 😊"
        )
    except:
        pass

# ================== START ==================
print("🤖 Auto Accept Bot Running (STABLE MODE)...")

threading.Thread(target=run_web).start()
app.run()