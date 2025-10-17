import discord
from discord.ext import commands
import asyncio
import datetime

class Moderation_Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="kick", aliases=["Kick"], description="Kicks a member from the server")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member == ctx.author:
            await ctx.send("You cannot kick yourself.")
            return

        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot kick someone with a higher or equal role than yours.")
            return

        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked. Reason: {reason}")

            kick_log_channel = self.bot.get_channel(111111111111111111) # Replace with your log channel ID or use os.getenv("KICK_LOG_CHANNEL_ID") to fetch from environment variables
            if kick_log_channel:
                embed = discord.Embed(title="Kick Log", description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason}\n**Time:** {datetime.datetime.now()}", color=discord.Color.red())
                await kick_log_channel.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("I do not have permission to kick this member.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to kick.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that member.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to kick members.")

async def setup(bot):
    await bot.add_cog(Moderation_Kick(bot))
