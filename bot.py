from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import asyncio

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
        "➕ Mujhe apne **Private Group / Channel** me add karo\n"
        "🔐 Admin banao (Approve Join Requests)\n\n"
        "✅ Main **pending + new** sabhi join requests accept karta hoon.",
        reply_markup=InlineKeyboardMarkup(
            [[
                InlineKeyboardButton(
                    "➕ Add me to Group / Channel",
                    url=f"https://t.me/{client.me.username}?startgroup=true"
                )
            ]]
        )
    )

# ---------- Auto accept NEW join request ----------
@app.on_chat_join_request()
async def auto_accept(client, request: ChatJoinRequest):
    await request.approve()
    await send_welcome_dm(client, request.from_user.id, request.from_user.first_name)

# ---------- Welcome DM ----------
async def send_welcome_dm(client, user_id, name):
    try:
        await client.send_message(
            user_id,
            f"🎉 **Welcome {name}!**\n\n"
            "✅ Aapki join request accept ho chuki hai.\n"
            "📢 Please rules follow karein.\n\n"
            "Enjoy 😊"
        )
    except:
        pass

# ---------- ACCEPT PENDING REQUESTS ON STARTUP ----------
async def accept_pending_requests():
    print("🔄 Checking pending join requests...")
    async for dialog in app.get_dialogs():
        chat = dialog.chat
        try:
            async for req in app.get_chat_join_requests(chat.id):
                await req.approve()
                await send_welcome_dm(app, req.from_user.id, req.from_user.first_name)
                print(f"✅ Accepted pending: {req.from_user.id} in {chat.id}")
        except:
            pass

# ---------- ON BOT START ----------
@app.on_start()
async def on_start(client):
    asyncio.create_task(accept_pending_requests())

# ================== START BOTH ==================
print("🤖 Auto Accept Bot (Pending + New) Running...")

threading.Thread(target=run_web).start()
app.run()