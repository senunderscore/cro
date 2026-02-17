# Cro-bot

Cro is a multipurpose Discord bot built with discord.py. It uses prefix commands and is split into modular cogs.

## Features

### Moderation
- Case-based records with notes and warnings
- Kick, ban, silent ban, unban, softban, tempban, massban
- Timeouts (mute/unmute) with duration parsing
- Lock and unlock channels
- Role add/remove and nickname changes
- Purge tools (bots, contains, embeds, emoji, files, links, mentions, humans) and cleanup

### Admin and Configuration
- Per-server configuration and custom prefixes
- Toggle default prefixes (defaults: `-`, `?`, `!`, `.`)
- Tag system for quick responses
- Logging channel setup (join/leave, messages, mod audit)
- Starboard channel and star threshold
- Bot master-only eval command

### Logging and Events
- Member join/leave logging
- Message edit/delete logging
- Profile and role changes logging
- Starboard for high-reaction messages
- Message tracking used by `snipe`

### Fun and Social
- Dice rolls, coin flips, 8ball
- Hug, pat, boop, slap, throw
- Cookies system (thank you detection, give, eat, check)
- Text transforms: `reverse`, `mock`, `uwu`
- `choose`, `snipe`, `patch`, `urban`, `what`

### Utility and Info
- About, invite, issues
- Ping, server info, user profiles
- Avatar and banner lookups
- Reminders and AFK system
- Emoji info
- Steam profile lookup (requires API key)
- GitHub profile lookup

### Integrations (Parked)
- Twitch, YouTube, and Minecraft cogs exist but are not loaded by default.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Create a `.env` file in the project root:

```bash
DISCORD_TOKEN=your-bot-token
BOT_MASTERS=123456789012345678,987654321098765432
STEAM_API_KEY=
TWITCH_CLIENT_ID=
TWITCH_CLIENT_SECRET=
YOUTUBE_API_KEY=
```

`DISCORD_TOKEN` (or `TOKEN`) is required. The other keys are optional and only needed for their related features.

## Project Structure

```
cogs/                  # Command modules (admin, moderation, fun, etc.)
events/                # Event handlers (logging, errors, features)
events/integrations/   # Parked integrations (not loaded by default)
utils/                 # Helpers, permissions, settings, cache
data/                  # JSON persistence
main.py                # Bot entry point
requirements.txt       # Python dependencies
```

## Commands (Highlights)

### Admin
| Command | Description |
|---------|-------------|
| `?config` | View/set server configuration |
| `?toggleprefix` | Toggle default prefixes |
| `?tag` | Create and fetch tags |
| `?joinleave` | Configure join/leave logging |
| `?messagelogs` | Configure message logging |
| `?modaudit` | Configure mod audit logging |
| `?starboard` | Configure starboard |

### Moderation
| Command | Description |
|---------|-------------|
| `?records` | View moderation records (aliases: `history`, `infractions`) |
| `?warn` | Warn a member |
| `?mute` | Timeout a member |
| `?ban` | Ban a member |
| `?tempban` | Temporarily ban a member |
| `?purge` | Bulk delete messages |
| `?lock` | Lock a channel |

### Fun and Utility
| Command | Description |
|---------|-------------|
| `?roll` | Roll dice (e.g., `?roll 2d6`) |
| `?coinflip` | Flip a coin |
| `?hug` | Hug someone |
| `?cookies` | Check cookie count |
| `?reminder` | Set a reminder |
| `?snipe` | Show last deleted message |

## Data Storage

Cro creates JSON files under `data/` as needed:
- `data/settings.json` for per-server settings
- `data/mod_logs.json` for moderation records
- `data/cookies.json` for cookies data
- `data/strings.json` for status and ping responses
