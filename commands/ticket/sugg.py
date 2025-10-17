import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import os

# Load env file form root dir
load_dotenv()


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggestion", aliases=["suggest"], description="Submit a suggestion to the server admins")
    async def suggestion(self, ctx, *, suggestion_message: str = None):
        if not suggestion_message:
            await ctx.send("❌ **Please provide a suggestion to submit.**\nUse `-help suggestion` for more information.")
            return

        # Confirmation message
        confirmation_message = await ctx.send(
            embed=discord.Embed(
                title="💡 Suggestion Confirmation",
                description="Are you sure you want to submit this suggestion?\n\n"
                            f"**Suggestion:**\n{suggestion_message}\n\n"
                            "Click ✅ to confirm or ❌ to cancel.",
                color=discord.Color.blurple()
            ).set_author(
                name=f"Suggestion by {ctx.author.display_name}",
                icon_url=ctx.author.avatar.url
            )
        )

        # Add reactions for confirmation
        await confirmation_message.add_reaction("✅")
        await confirmation_message.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=None, check=check)

            if str(reaction.emoji) == "✅":
                # Handle suggestion submission
                suggestion_channel = discord.utils.get(ctx.guild.text_channels, name="suggestions")
                if suggestion_channel is None:
                    await ctx.send("❌ **Suggestions channel not found! Please create a channel named `suggestions`.**")
                    return

                # Create suggestion embed
                suggestion_embed = discord.Embed(
                    title="📝 New Suggestion",
                    description=f"**Suggestion:**\n{suggestion_message}",
                    color=discord.Color.green()
                )
                suggestion_embed.set_author(
                    name=f"Submitted by {ctx.author.display_name}",
                    icon_url=str(ctx.author.avatar) if ctx.author.avatar else str(ctx.author.default_avatar)
                )
                suggestion_embed.set_footer(
                    text=f"User ID: {ctx.author.id} • {ctx.author.name}#{ctx.author.discriminator}"
                )
                suggestion_embed.add_field(name="🔗 User Mention", value=ctx.author.mention, inline=False)

                # Send suggestion to the suggestions channel
                suggestion_message = await suggestion_channel.send(embed=suggestion_embed)

                # Add voting reactions
                await suggestion_message.add_reaction("👍")
                await suggestion_message.add_reaction("👎")

                # Notify user of successful submission
                await confirmation_message.edit(
                    content="✅ **Suggestion submitted successfully! Thank you for your input.**",
                    embed=None
                )

            elif str(reaction.emoji) == "❌":
                # User canceled the suggestion submission
                await confirmation_message.edit(
                    content="❌ **Suggestion submission canceled.**",
                    embed=None
                )

        except asyncio.TimeoutError:
            # Handle timeout
            await confirmation_message.edit(
                content="⏰ **Suggestion submission timed out. Please try again.**",
                embed=None
            )

# Setup the cog
async def setup(bot):
    await bot.add_cog(Suggestions(bot))
