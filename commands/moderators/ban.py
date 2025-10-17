import discord
from discord.ext import commands
import asyncio
import random
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["Ban"], description="Bans a member from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if member == ctx.author:
            await ctx.send("You cannot ban yourself.")
            return

        if member == ctx.guild.owner:
            await ctx.send("You cannot ban the server owner.")
            return

        if member.top_role >= ctx.author.top_role:
            await ctx.send("You cannot ban someone with a higher or equal role than yours.")
            return

        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.mention} has been banned. Reason: {reason}")
            #get channel by id
            ban_log_channel = self.bot.get_channel(111111111111111111) # Replace with your ban log channel ID or use os.getenv("BAN_LOG_CHANNEL_ID") to fetch from environment variables

            
            if ban_log_channel:
                embed = discord.Embed(title="Ban Log", description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Reason:** {reason}\n**Time:** {datetime.datetime.now()}", color=discord.Color.red())
                await ban_log_channel.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("I do not have permission to ban this member.")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member to ban.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that member.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to ban members.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
