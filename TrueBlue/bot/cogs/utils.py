import discord
from discord.ext import commands
from datetime import datetime
from discord import app_commands
from zoneinfo import ZoneInfo

class MyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # --- PING ----
    @app_commands.command(name="ping",description="Check if the bot is alive")
    async def ping(self,interaction: discord.Interaction): await interaction.response.send_message(
        "⚡ Who summoned the ping?! Please don’t test my connection, mortal. I’m online, stable, and operating at full capacity. The router is calm, the packets are flowing, and the latency is under control. 🛜📡",
        ephemeral=True)

    @app_commands.command(name="sync", description="Sync slash commands")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        guild = self.bot.guilds[0]
        self.bot.tree.copy_global_to(guild=guild)
        synced = await self.bot.tree.sync(guild=guild)
        await interaction.response.send_message(f"Synced {len(synced)} command(s).",ephemeral=True)

    @app_commands.command(name="clearcommands", description="clear all commands for the guild")
    async def clearcommands(self, interaction: discord.Interaction):
        if not await self.bot.is_owner(interaction.user): await interaction.response.send_message("You are not authorized to use this command.",ephemeral=True); return
        guild = self.bot.guilds[0]
        self.tree.clear_commands(guild=guild)
        synced = await self.bot.tree.sync(guild=guild)
        await interaction.response.send_message("All global slash commands have been cleared.",ephemeral=True)

    @app_commands.command(name="reload", description="Reload a cog")
    async def reload(self, interaction: discord.Interaction, cog: str):
        if not await self.bot.is_owner(interaction.user): await interaction.response.send_message("You are not authorized to use this command.",ephemeral=True); return
        try:
            await self.bot.reload_extension(f"cogs.{cog}")
            await interaction.response.send_message(f"Reloaded all cogs`{cog}`.", ephemeral=True)
        except commands.ExtensionError as e:
            await interaction.response.send_message(f"Failed to load updated cogs: `{e}`", ephemeral=True)

async def setup(bot):
    await bot.add_cog(MyCommands(bot))