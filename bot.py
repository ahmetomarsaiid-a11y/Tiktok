import logging
import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types

# pulling the token from your environment variables so it is ready for railway
BOT_TOKEN = os.getenv("BOT_TOKEN", "PUT_YOUR_TOKEN_HERE")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def fetch_hd_video(url: str) -> str | None:
    api_url = "https://www.tikwm.com/api/"
    async with aiohttp.ClientSession() as session:
        # the hd parameter forces the highest possible quality output
        async with session.post(api_url, data={"url": url, "hd": 1}) as resp:
            if resp.status == 200:
                data = await resp.json()
                if data.get("code") == 0:
                    # hdplay is the pure raw no-watermark stream
                    return data["data"].get("hdplay") or data["data"].get("play")
    return None

@dp.message()
async def download_handler(message: types.Message):
    text = message.text or ""
    
    # only triggers if you actually drop a tiktok link in the chat
    if "tiktok.com" in text:
        wait_msg = await message.reply("⏳ pulling the raw hd file...")
        
        try:
            video_url = await fetch_hd_video(text)
            
            if video_url:
                await message.reply_video(video=video_url, caption="highest quality secured 🔥")
                await wait_msg.delete()
            else:
                await wait_msg.edit_text("❌ link is cooked or video is private")
        except Exception:
            await wait_msg.edit_text("💔 api is tweaking right now")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# update for railway to trigger fresh build
