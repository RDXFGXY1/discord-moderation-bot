import discord
from discord.ext import commands
import asyncio
import datetime

class Moderation_Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="timeout", aliases=["Timeout"], description="Timeouts a member from the server")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, time: str, *, reason="No reason provided"):
        try:
            time_obj = self.parse_time(time)
            if time_obj is None:
                await ctx.send("Invalid time format. Use format like 1h, 1m, 1s.")
                return

            await member.timeout(time_obj, reason=reason)
            await ctx.send(f"{member.mention} has been timed out for {time}. Reason: {reason}")

            timeout_log_channel = self.bot.get_channel(111111111111111111) # Replace with your timeout log channel ID or use os.getenv("TIMEOUT_LOG_CHANNEL_ID") to fetch from environment variables
            if timeout_log_channel:
                embed = discord.Embed(title="Timeout Log", description=f"**User:** {member.mention}\n**Moderator:** {ctx.author.mention}\n**Time:** {time}\n**Reason:** {reason}\n**Time:** {datetime.datetime.now()}", color=discord.Color.orange())
                await timeout_log_channel.send(embed=embed)

        except discord.Forbidden:
            await ctx.send("I do not have permission to timeout this member.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    def parse_time(self, time_str):
        time_dict = {"s": 1, "m": 60, "h": 3600, "d": 86400}
        if time_str[-1] not in time_dict:
            return None
        try:
            num = int(time_str[:-1])
            unit = time_str[-1]
            return datetime.timedelta(seconds=num * time_dict[unit])
        except ValueError:
            return None
    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a member, time, and reason to timeout.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that member or invalid time format.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to timeout members.")

async def setup(bot):
    await bot.add_cog(Moderation_Timeout(bot))
