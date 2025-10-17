import discord
from discord.ext import commands
import asyncio

class Moderation_Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban", aliases=["Unban"], description="Unbans a member from the server")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member_id: int):
        try:
            user = await self.bot.fetch_user(member_id)
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} has been unbanned.")
        except discord.NotFound:
            await ctx.send("Could not find that user.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to unban this member.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please specify a user ID to unban.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Could not find that user.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to unban members.")

async def setup(bot):
    await bot.add_cog(Moderation_Unban(bot))
