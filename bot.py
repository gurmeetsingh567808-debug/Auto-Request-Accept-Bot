from pyrogram import Client
from pyrogram.types import ChatJoinRequest
import os

# ========= CONFIG =========
API_ID = int(os.getenv("API_ID", "12345678"))
API_HASH = os.getenv("API_HASH", "0ef198353fe6021fb9a3c3600069556b")
BOT_TOKEN = os.getenv("BOT_TOKEN", "BOT_TOKEN_HERE")

WELCOME_TEXT = """
👋 Hello {name}

✅ Your join request has been approved.

📢 You can now access the channel/group.
💖 Enjoy!
"""

app = Client(
    "auto_accept_unlimited",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_chat_join_request()
async def auto_accept(client: Client, request: ChatJoinRequest):
    try:
        # Accept request (works for ANY channel/group)
        await request.approve()

        # Send welcome DM
        try:
            await client.send_message(
                request.from_user.id,
                WELCOME_TEXT.format(
                    name=request.from_user.first_name or "User"
                )
            )
        except:
            pass  # user ne DM band kiya ho

        print(
            f"Accepted | User: {request.from_user.id} | Chat: {request.chat.id}"
        )

    except Exception as e:
        print("Error:", e)

print("🤖 Auto Accept Unlimited Bot Running...")
app.run()