# Discord Moderation & Management Bot

> A comprehensive Discord bot that actually works (most of the time). Built with discord.py and questionable coding decisions.

## Features That Actually Work

### Moderation Commands
Because someone has to keep the chaos under control.

- **Kick** - Yeeting members from the server (with style)
- **Warn System** - Three strikes and you're... well, still here, but warned
- **Come** - Teleport members to your voice channel (not creepy at all)
- **Where** - For when you need to stalk... I mean, locate members

### Logging & Monitoring
Big Brother is watching, but in a friendly way.

- **Member Join/Leave Tracking** - Know who's joining your cult... server
- **Message Edit/Delete Logging** - Because we all know you said something stupid
- **Role Update Logging** - Track promotions, demotions, and identity crises
- **Moderation Action Logging** - Keep receipts of everything
- **Command Usage Logging** - See who's spamming commands at 3 AM
- **Suspicious Account Detection** - Catching trolls since... well, since now

### Automation
Set it and forget it (but please don't actually forget it).

- **Auto-Role** - Welcome wagon, automated edition
- **Auto-Moderation** - AI-powered link deletion (okay, it's just regex, but sounds cooler)
- **New Account Flagging** - "Your account is 5 minutes old. Sus."

### Management Systems
The fancy stuff that makes you look professional.

- **Ticket System** - Customer support, but make it Discord
- **Staff Feedback** - Rate your overlords... I mean, moderators
- **Announcement System** - Broadcast your terrible jokes server-wide
- **Suggestion System** - Democracy in action (votes may be rigged)
- **Application System** - Hire new minions... staff members

## Requirements

You know, the boring stuff:

- Python 3.8+ (because we're not savages using Python 2)
- discord.py 2.0+ (the good version)
- python-dotenv (for hiding your secrets)
- colorama (making terminals pretty since forever)
- A Discord bot token (obviously)
- Common sense (optional, but recommended)

## Installation

### The "I Know What I'm Doing" Version

```bash
git clone https://github.com/yourusername/discord-moderation-bot.git
cd discord-moderation-bot
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your favorite text editor (vim users, we see you)
mkdir -p server/warns config/staff apply
python main.py
```

### The "Please Hold My Hand" Version

**Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/discord-moderation-bot.git
cd discord-moderation-bot
```
Translation: Download the code and go into that folder.

**Step 2: Install Dependencies**
```bash
pip install -r requirements.txt
```
Translation: Install all the stuff this bot needs to not crash immediately.

**Step 3: Configure Environment Variables**
```bash
cp .env.example .env
nano .env  # or use notepad like a normal person
```
Translation: Copy the example file and fill in your actual information. Don't use "your_token_here" as your actual token. We've seen people do this.

**Step 4: Create Required Directories**
```bash
mkdir -p server/warns config/staff apply
```
Translation: Make some folders. The bot will be sad without them.

**Step 5: Initialize Staff Configuration**

Create a file at `config/staff/staff.json`:
```json
{
  "YOUR_STAFF_ID_HERE": {
    "name": "Staff McStaffface",
    "status": true,
    "vouches": 0,
    "reps": 0
  }
}
```
Translation: Tell the bot who the cool kids are.

**Step 6: Run the Bot**
```bash
python main.py
```
Translation: Press the magic button and pray to the Python gods.

## Configuration

Your `.env` file should look something like this:

```env
# Bot Token - Keep this secret or hackers will use your bot to spam cat pictures
DISCORD_TOKEN=your_bot_token_here

# Server Configuration
GUILD_ID=your_guild_id_here

# Channel IDs - Right-click and "Copy ID" (enable Developer Mode first, genius)
ALL_LOG=your_log_channel_id
STATUS_CHANNEL_ID=your_status_channel_id

# Role IDs - Same deal as channels
USER_ROLE_ID=your_auto_role_id
STAFF_ROLE_ID=your_staff_role_id

# Auto-Moderation - Channels and roles that get a free pass
IGNORED_CHANNELS=channel_id_1, channel_id_2
IGNORED_ROLES=role_id_1, role_id_2

# File Paths - Don't change these unless you enjoy pain
WARN_FILE=server/warns/warnings.json
```

## Command Reference

Because documentation is important (allegedly).

### Moderation Commands

| Command | Description | Permissions Required | Chance of Abuse |
|---------|-------------|---------------------|-----------------|
| `-kick <member> [reason]` | Remove someone's Discord privileges | Kick Members | High |
| `-warn <member> [reason]` | Official "I'm disappointed in you" | Manage Messages | Medium |
| `-warnings <member>` | View someone's rap sheet | Manage Messages | Low |
| `-clearwarns <member>` | Forgiveness is divine | Manage Messages | Low |
| `-come <member>` | Summon someone to your presence | Move Members | Creepy |

### Utility Commands

| Command | Description | Permissions Required |
|---------|-------------|---------------------|
| `-whereare <member>` | GPS for Discord | None |
| `-announce` | Make important-sounding messages | Administrator |
| `-suggestion <message>` | Suggest things that will never happen | None |
| `-ticket` | Open a help desk ticket | None |

### Staff Commands

| Command | Description | Cooldown |
|---------|-------------|----------|
| `-vouch <staff_member>` | Give someone street cred | 24 hours |
| `-rep <staff_member>` | Internet points for staff | 24 hours |
| `-my_stats` | Check your internet points | None |

### Auto-Moderation Commands

For when you want the bot to do your job for you.

| Command | Description | Permissions Required |
|---------|-------------|---------------------|
| `-ignore_channel <channel>` | Give channel a moderation free pass | Manage Channels |
| `-unignore_channel <channel>` | Revoke said free pass | Manage Channels |
| `-ignore_role <role>` | VIP treatment for specific roles | Manage Roles |
| `-unignore_role <role>` | No more VIP | Manage Roles |
| `-set_log_channel <channel>` | Where the bot tattles | Manage Channels |

### Application Management

| Command | Description | Permissions Required |
|---------|-------------|---------------------|
| `-apply_action <user_id> <true/false>` | Accept or reject staff wannabes | Administrator |

## Project Structure

```
discord-bot/
├── cogs/
│   ├── events/              # Things that happen automatically
│   │   ├── handel_join.py   # "Welcome to the server!" spam
│   │   ├── handel_leave.py  # "Goodbye!" but with feelings
│   │   ├── handel_mod.py    # Keeping tabs on moderator power trips
│   │   ├── handel_role.py   # Role change stalking
│   │   ├── message_deleted.py  # Preserving deleted cringe forever
│   │   └── message_edited.py   # "I saw what you originally wrote"
│   ├── commands/            # Things users can actually do
│   │   ├── kick.py          # The yeeting mechanism
│   │   ├── warn.py          # Official disappointment system
│   │   ├── come.py          # Voice channel teleportation
│   │   ├── where.py         # Stalker mode
│   │   ├── announce.py      # Broadcast your bad jokes
│   │   ├── sugg.py          # Suggestion box (digital edition)
│   │   ├── ticket.py        # Help desk simulator
│   │   ├── feedback.py      # Rate your moderators
│   │   └── apply.py         # Job application processor
│   ├── logging/             # Terminal spam
│   │   ├── on_commands.py   # Colorful command logs
│   │   └── handel_commands.py  # Even more logs
│   └── automation/          # The "smart" features
│       ├── auto_moderation_system.py  # Link destroyer 9000
│       └── auto_role.py     # Automatic welcome committee
├── config/
│   └── staff/
│       └── staff.json       # The list of people with power
├── server/
│   └── warns/
│       └── warnings.json    # Hall of shame
├── .env                     # Your secrets (keep it secret, keep it safe)
├── .env.example             # Template for your secrets
├── .gitignore               # Files Git should ignore (like your ex)
├── requirements.txt         # Shopping list for pip
├── LICENSE                  # Legal stuff
├── README.md                # You are here
└── main.py                  # The heart of the operation
```

## Setup Guide

### Getting Your Bot Token

1. Visit the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" (be creative with the name)
3. Go to the "Bot" section
4. Click "Add Bot" and confirm you're not a robot (ironic)
5. Enable these Privileged Gateway Intents or nothing will work:
   - PRESENCE INTENT
   - SERVER MEMBERS INTENT
   - MESSAGE CONTENT INTENT (this one's super important)
6. Copy your bot token (the long string of gibberish)
7. Paste it in your `.env` file
8. Never, EVER share this token (seriously, don't)

### Inviting the Bot

1. Still in Developer Portal? Good.
2. Go to OAuth2 > URL Generator
3. Select scopes: `bot` and `applications.commands`
4. Select permissions (or just check Administrator if you're lazy)
5. Copy the generated URL
6. Paste in browser and invite to your server
7. Watch your bot appear offline because you haven't started it yet

### Getting IDs

Enable Developer Mode first:
- User Settings > Advanced > Developer Mode: ON

Then:
- Right-click anything (channels, roles, users)
- Click "Copy ID"
- Paste into your `.env` file
- Feel like a hacker

## Troubleshooting

### Bot Not Responding
- Is it online? Check Discord.
- Did you enable MESSAGE CONTENT INTENT? (everyone forgets this)
- Can it see the channel?
- Did you try turning it off and on again?

### "Log channel not found"
- Check the channel ID in `.env`
- Make sure the bot can actually see that channel
- Did you accidentally delete the channel? (we won't judge)

### Commands Not Working
- Check the prefix (default is `-`)
- Make sure you have permissions
- Try asking the bot nicely

### Auto-Role Not Assigning
- Is the bot's role above the auto-role?
- Does it have MANAGE_ROLES permission?
- Did you spell the role ID correctly?

### It's Still Not Working
- Check the terminal for error messages
- Google the error (we all do it)
- Ask ChatGPT (we won't tell)
- Open an issue on GitHub (actually helpful)

## Contributing

Want to make this bot better? Here's how:

1. Fork it (top right on GitHub)
2. Clone your fork
3. Create a branch (`git checkout -b feature/amazing-feature`)
4. Make your changes
5. Commit them (`git commit -m 'Add some amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request
8. Wait patiently (or impatiently, we get it)

### Code Style Guidelines

- Follow PEP 8 (Python's style guide, not a cafeteria)
- Use meaningful variable names (no more `x`, `y`, `asdf`)
- Add comments for complex code
- Test your code before submitting
- Don't break existing features (please)

## Known Issues

Things we know about but haven't fixed yet:

- Member leave logging tries to fetch message history (spoiler: it can't)
- Some IDs are hardcoded (we're working on it)
- Cooldowns reset when bot restarts (feature, not a bug)
- May contain traces of bugs

## Changelog

### Version 1.0.0 (Current)
- Initial release
- All the features listed above
- Probably some bugs we haven't found yet

## License

MIT License - Do whatever you want with this code. Seriously. We don't care. Just don't sue us if your server gets nuked.

See [LICENSE](LICENSE) file for the boring legal details.

## Support

Need help? We're here... sometimes.

- Open an issue on GitHub
- Join our Discord server (link coming soon)
- Email us and we'll respond in 3-5 business days (or never)
- Sacrifice a rubber duck to the programming gods

## Disclaimer

This bot is provided "as-is" which is lawyer-speak for "it works on my machine."

Always test in a development server first. We're not responsible if you accidentally ban everyone, delete all channels, or start a robot uprising.

## Acknowledgments

- [discord.py](https://github.com/Rapptz/discord.py) - For making Discord bots possible
- Stack Overflow - For solving all our problems
- Coffee - For keeping us awake during debugging sessions
- You - For actually reading this README

---

Made with caffeine and questionable decisions by NullStudio Inc.

**Star this repo if it helped you!** (or if you just want to make us feel good about ourselves)
