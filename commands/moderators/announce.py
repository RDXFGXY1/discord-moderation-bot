import discord
from discord.ext import commands
from discord.ui import Modal, TextInput

class Announce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="announce", aliases=["Announce"], description="Sends an announcement to the server")
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx):
        await ctx.send("📢 Please provide the title of your announcement:")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        try:
            title_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            title = title_msg.content

            await ctx.send("✍️ Please provide the content of your announcement:")
            content_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            content = content_msg.content

            await ctx.send("🔗 Optional: Provide a footer or link (or type 'skip' to skip):")
            footer_msg = await self.bot.wait_for("message", timeout=60.0, check=check)
            footer = footer_msg.content if footer_msg.content.lower() != "skip" else f"Announced by {ctx.author.name}"

            embed = discord.Embed(
                title=title,
                description=content,
                color=discord.Color.blue()
            )
            embed.set_footer(text=footer)
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)

        except asyncio.TimeoutError:
            await ctx.send("⏰ You took too long to respond. Announcement cancelled.")

    @announce.error
    async def announce_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 You do not have permission to use this command.")

async def setup(bot):
    await bot.add_cog(Announce(bot))
