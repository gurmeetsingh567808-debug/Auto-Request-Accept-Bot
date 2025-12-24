from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
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

# ---------- /start command ----------
@app.on_message(filters.private & filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(
        "🤖 **I am Request Accept Bot**\n\n"
        "➕ Mujhe apne **Private Group ya Channel** me add karo\n"
        "🔐 Aur mujhe **Admin** banao (Approve Join Requests)\n\n"
        "✅ Main sabhi join requests **automatically accept** kar dunga.",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Add me to Group / Channel",
                        url=f"https://t.me/{client.me.username}?startgroup=true"
                    )
                ]
            ]
        )
    )

# ---------- Auto accept join request ----------
@app.on_chat_join_request()
async def auto_accept(client, request: ChatJoinRequest):
    await request.approve()

    # Welcome DM
    try:
        await client.send_message(
            request.from_user.id,
            f"🎉 **Welcome {request.from_user.first_name}!**\n\n"
            "✅ Aapki join request accept ho chuki hai.\n"
            "📢 Please rules follow karein.\n\n"
            "Enjoy 😊"
        )
    except:
        pass

# ================== START BOTH ==================
print("🤖 Auto Accept Bot with Start Button Running...")

threading.Thread(target=run_web).start()
app.run()