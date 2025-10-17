import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Load environment variables
load_dotenv()

class MemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = int(os.getenv("ALL_LOG", "0"))  # Welcome channel ID from .env  

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Send a welcome message to the welcome channel as embed
        welcome_channel = discord.utils.get(member.guild.channels, id=self.welcome_channel_id)
        if welcome_channel:
            welcome_embed = discord.Embed(
                title="New Member!",
                description=f"{member.mention} has joined {member.guild.name}",
                color=discord.Color.green()
            )
            welcome_embed.add_field(name="Account Created", value=f"{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}", inline=False)
            welcome_embed.add_field(name="Account Age", value=f"`{self.account_age(member.created_at)}`", inline=True)
            welcome_embed.add_field(name="Joined Server", value=f"{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}", inline=True)
            welcome_embed.add_field(name="Roles", value=f"{', '.join([role.name for role in member.roles[1:]])}", inline=False)  # Skip @everyone role
            welcome_embed.add_field(name="Bot Account", value="Yes" if member.bot else "No", inline=True)
            welcome_embed.add_field(name="Status", value=f"{member.status}", inline=True)
            
            # Additional account checks (e.g., if the account was created recently)
            if self.is_suspicious_account(member):
                welcome_embed.add_field(name="⚠️ Suspicious Account", value="This account was created recently, please verify its authenticity.", inline=False)
                welcome_embed.color = discord.Color.red()  # Change the color to red for suspicious accounts

            welcome_embed.set_footer(text="Welcome Message")
            welcome_embed.set_author(name=member.name, icon_url=member.avatar.url)
            welcome_embed.set_thumbnail(url=member.avatar.url)
            await welcome_channel.send(embed=welcome_embed)

    def account_age(self, created_at):
        # Ensure both datetimes are offset-aware for subtraction
        now = datetime.now(timezone.utc)  # Using UTC timezone for consistency
        difference = now - created_at
        years = difference.days // 365
        months = (difference.days % 365) // 30
        days = (difference.days % 365) % 30
        hours, remainder = divmod(difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Format the account age as a string
        return f"{years} years, {months} months, {days} days"

    def is_suspicious_account(self, member):
        now = datetime.now(timezone.utc)  # Ensure this is offset-aware
        account_creation_time = member.created_at
        age_in_days = (now - account_creation_time).days

        # Flag account if it's less than 3 days old or created within the last 24 hours
        if age_in_days <= 1:
            return True  # Flag new accounts as suspicious
        return False

# Cog setup
async def setup(bot):
    await bot.add_cog(MemberJoin(bot))
