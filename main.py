import asyncio
import logging
import logging.config
import os
from datetime import datetime
from pytz import timezone
from aiohttp import web

# Pehle loop setup karein taaki pyromod import hote waqt error na de
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from pyromod import Client
from pyrogram import __version__
from pyrogram.raw.all import layer
from info import Config

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes([web.get("/", lambda r: web.Response(text="Hello, Bot is Running!"))])
    return web_app

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="ReportBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins={'root': 'plugins'},
            in_memory=True
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        
        # Web server setup
        app = web.AppRunner(await web_server())
        await app.setup()
        await web.TCPSite(app, "0.0.0.0", Config.PORT).start()
        
        logging.info(f"✅ {me.first_name} (Pyrogram v{__version__}, Layer {layer}) started! ✅")
        await self.send_message(Config.OWNER, f"**__{me.first_name} Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped ⛔")

if __name__ == "__main__":
    bot = Bot()
    
    # Python 3.14 compatible runner
    try:
        loop.run_until_complete(bot.start())
        logging.info("Bot is running... Press Ctrl+C to stop.")
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(bot.stop())
    except Exception as e:
        logging.error(f"Fatal Error: {e}")
