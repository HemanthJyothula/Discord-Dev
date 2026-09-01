import asyncio
import logging
import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from pathlib import Path

# ---- Initialization ----
ROOT_DIR = Path(__file__).resolve().parent
COGS_DIR = ROOT_DIR / "cogs"
load_dotenv(ROOT_DIR / ".env")
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN: raise RuntimeError("DISCORD_TOKEN is not configured.")
logging.basicConfig(level=logging.INFO,format=("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
logger = logging.getLogger("bot")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True


# ---- Bot ----
class Bot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned,intents=intents)
        self.root_dir = ROOT_DIR
        self.cogs_dir = COGS_DIR

    async def setup_hook(self) -> None:
        await self.load_cogs()
        
    async def load_cogs(self) -> None:
        if not self.cogs_dir.exists(): raise FileNotFoundError(f"Cog directory not found: {self.cogs_dir}")
        for file in sorted(self.cogs_dir.rglob("*.py")):
            if file.name.startswith("_"): continue
            relative = file.relative_to(ROOT_DIR)
            module = ".".join(relative.with_suffix("").parts)
            try:
                await self.load_extension(module)
                logger.info("Loaded cog: %s",module,)
            except Exception:
                logger.exception("Failed to load cog: %s",module)
                raise

    async def on_ready(self) -> None:
        for guild in self.guilds:
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            logger.info("Synced %d slash command(s) in the server %s.",len(synced),guild.name)
        logger.info("Logged in as %s (%s)",self.user,self.user.id if self.user else "unknown")
        logger.info("Connected to %d guild(s).",len(self.guilds))


# ---- Main ----
async def main() -> None:
    bot = Bot()
    try:
        logger.info("Starting bot...")
        async with bot: await bot.start(TOKEN)
    finally:
        if not bot.is_closed(): await bot.close()

if __name__ == "__main__":
    asyncio.run(main())