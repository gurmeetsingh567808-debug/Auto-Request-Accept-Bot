from pyrogram import Client
from pyrogram.types import ChatJoinRequest
import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise RuntimeError("❌ Environment variables not set properly")

API_ID = int(API_ID)

app = Client(
    "auto_accept_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_chat_join_request()
async def auto_accept(client, request: ChatJoinRequest):
    await request.approve()

print("🤖 Auto Accept Bot Running...")
app.run()