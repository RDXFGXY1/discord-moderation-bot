import discord
from discord.ext import commands, tasks
from discord.ui import View, Select, Button
import asyncio
import json
import os
from dotenv import load_dotenv

# Load env file form root dir
load_dotenv()

# Main code
class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_num = 0  # Initialize ticket counter as an instance variable
        self.staff_file = "config/staff/staff.json"
        self.staff_statuses = {}  # Cache for tracking previous statuses
        self.status_channel_id = int(os.getenv("STATUS_CHANNEL_ID", "0"))  # Replace with your channel ID
        self.update_staff_status.start()  # Start the status checker loop

    @tasks.loop(seconds=1)
    async def update_staff_status(self):
        """Check staff statuses and update the embed if needed."""
        if not os.path.exists(self.staff_file):
            print(f"{self.staff_file} not found!")
            return

        # Load staff data from the JSON file
        with open(self.staff_file, "r") as f:
            staff_data = json.load(f)

        GUILD_ID = os.getenv("GUILD_ID", "0") 
        guild = self.bot.get_guild(int(GUILD_ID)) 
        if not guild:
            print("Bot is not in the specified guild!")
            return

        updated_statuses = {}
        for staff_id in staff_data:
            member = guild.get_member(int(staff_id))
            if not member:
                # If the member is not found in the guild, assume offline
                updated_statuses[staff_id] = {"name": staff_data[staff_id]["name"], "status": "offline"}
                continue
            
            # Check the status
            status = member.status
            if status == discord.Status.online:
                status_text = "In Service"  # You can replace this with whatever you want
                emoji = "<a:status_online_animated2:1313841696227987549>"
            elif status == discord.Status.idle:
                status_text = "Idle"
                emoji = "<a:idle:1313626712755404870>"  # Replace IDLE_EMOJI_ID with the actual emoji ID
            elif status == discord.Status.dnd:
                status_text = "Out Of Service"
                emoji = "<a:dnd:1313840782024900608>"  # Replace DND_EMOJI_ID with the actual emoji ID
            elif status == discord.Status.offline:
                status_text = "Offline"
                emoji = "<a:offline1:1313841737646604308>"

            updated_statuses[staff_id] = {"name": staff_data[staff_id]["name"], "status": status_text, "emoji": emoji}

        # Compare with cached statuses and update if there's a change
        if updated_statuses != self.staff_statuses:
            self.staff_statuses = updated_statuses  # Update the cache
            await self.update_embed(staff_data)  # Update the embed


    async def update_embed(self, staff_data):  # Ensure this method is correctly defined
        """Update the ticket system embed."""
        embed = discord.Embed(
            title="Ticket System",
            description="يرجى منك اختيار حسب طلبك او المشكل الخاص بك و الضغط على الزر المناسب في الاسفل\n\n"
                        "Please choose according to your request or problem and press the appropriate button below",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1311659428818325524/1314149955929378856/order_info.png?ex=6752b905&is=67516785&hm=8c4daac4f2a08519eafcc3fa0ba5de07e54ede48df7b68e14c556057637a964a&")

        embed.add_field(name="__Staff List__", value=self.format_staff_list(staff_data), inline=False)
        channel = self.bot.get_channel(self.status_channel_id)
        if channel:
            async for msg in channel.history(limit=10):
                if msg.author == self.bot.user and msg.embeds:
                    await msg.edit(embed=embed)
                    return
            await channel.send(embed=embed)
    def format_staff_list(self, staff_data):
        return "\n".join(
            f"{'✅' if info['status'] else '❌'} {info['name']}" for info in staff_data.values()
        )

    def create_ticket_embed(self, staff_data):
        """Create the main ticket system embed."""
        embed = discord.Embed(
            title="Ticket System",
            description="يرجى منك اختيار حسب طلبك او المشكل الخاص بك و الضغط على الزر المناسب في الاسفل\n\n"
                        "Please choose according to your request or problem and press the appropriate button below",
            color=discord.Color.blue()
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1311659428818325524/1314149955929378856/order_info.png?ex=6752b905&is=67516785&hm=8c4daac4f2a08519eafcc3fa0ba5de07e54ede48df7b68e14c556057637a964a&")
        embed.add_field(name="__Staff List__", value=self.format_staff_list(staff_data), inline=False)
        return embed

    def format_staff_list(self, staff_data):
        """Format the staff list for the embed."""
        formatted_list = ""
        for staff_id, info in self.staff_statuses.items():
            name = info["name"]
            status = f"{info['emoji']} [{info['status']}]"
            formatted_list += f"{status} <@!{staff_id}> ({name})\n"
        return formatted_list


    @commands.command(name="ticket", aliases=["Ticket"], description="Opens a ticket menu")
    async def ticket(self, ctx):
        """Send the ticket embed and menu."""
        if not os.path.exists(self.staff_file):
            await ctx.send("Staff configuration file not found!")
            return

        with open(self.staff_file, "r") as f:
            staff_data = json.load(f)

        embed = self.create_ticket_embed(staff_data)
        view = TicketDropdownView(self)
        self.status_message = await ctx.send(embed=embed, view=view)

class TicketDropdownView(View):
    def __init__(self, cog):
        super().__init__(timeout=None)  # The dropdown remains active indefinitely
        self.cog = cog
        self.add_item(TicketDropdownMenu(cog))

class TicketDropdownMenu(Select):
    def __init__(self, cog):
        options = [
            discord.SelectOption(
                label="About us",
                description="Get more information about us and our services.",
                emoji="<:about_sus:1314564269576290314>"
            ),
            discord.SelectOption(
                label="Terms of use",
                description="View our terms of service.",
                emoji="<:terms_of_use:1314564277876817951>"
            ),
            discord.SelectOption(
                label="Our Service",
                description="Learn about the services we offer.",
                emoji="<:services:1314565028359307266>",
            ),
            discord.SelectOption(
                label="Report a bug",
                description="Report a bug or an issue you are facing.",
                emoji="<:report:1314564269916033074>"
            )
        ]

        super().__init__(
            placeholder="Choose your ticket type...",
            min_values=1,
            max_values=1,
            options=options,
        )
        self.cog = cog

    async def callback(self, interaction: discord.Interaction):
        ticket_type = self.values[0]
        guild = interaction.guild
        author = interaction.user

        # Handle ticket creation for "Report a bug"
        if ticket_type == "Report a bug":
            self.cog.ticket_num += 1
            ticket_channel = await guild.create_text_channel(
                name=f"ticket-{self.cog.ticket_num}",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                    guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                },
                reason=f"Ticket created by {author.name}",
            )
            embed = discord.Embed(
                title="Bug Report Ticket",
                description="Please describe the issue you are facing. A staff member will assist you shortly.",
                color=discord.Color.blue()
            )
            embed.set_author(name=author.display_name, icon_url=author.avatar.url)
            embed.set_footer(text="Use the button below to close this ticket.")
            view = TicketCloseButtonView()
            await ticket_channel.send(embed=embed, view=view)
            await interaction.response.send_message(
                f"Your bug report ticket has been created: {ticket_channel.mention}",
                ephemeral=True,
            )
        else:
            # Handle ephemeral messages for other options
            if ticket_type == "About us":
                embed = discord.Embed(
                    title="About Us",
                    description="We are a team dedicated to providing excellent support and services.",
                    color=discord.Color.green()
                )
            elif ticket_type == "Terms of use":
                embed = discord.Embed(
                    title="Terms of Use",
                    description="By using our services, you agree to abide by our terms and conditions.",
                    color=discord.Color.orange()
                )
            elif ticket_type == "Our Service":
                embed = discord.Embed(
                    title="Our Services",
                    description="We offer various services including customer support, bug reporting, and more.",
                    color=discord.Color.purple()
                )
            await interaction.response.send_message(embed=embed, ephemeral=True)


class TicketCloseButtonView(View):
    def __init__(self):
        super().__init__()
        self.add_item(TicketCloseButton())

class TicketCloseButton(Button):
    def __init__(self):
        super().__init__(label="Close Ticket", style=discord.ButtonStyle.danger)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        channel = interaction.channel
        await channel.send("This ticket will be closed in 5 seconds...")
        await asyncio.sleep(5)
        await channel.delete(reason="Ticket closed by user")

async def setup(bot):
    await bot.add_cog(TicketSystem(bot))
