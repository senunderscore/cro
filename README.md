# Cro-bot

A feature-rich Discord bot built with discord.py, featuring moderation, entertainment, admin tools, and extensible command architecture.

## Features

### Moderation
- User moderation with case tracking
- Moderation logs and audit trails
- Infractions and history tracking
- Time-based parsing for durations

### Entertainment
- Dice rolling (`?roll 2d6`)
- Coin flip games
- Social interaction commands (hug, etc.)
- 8-ball responses
- And more!

### Admin Tools
- Server configuration management
- Custom prefix system
- Tag system for quick responses
- Logging channels (join/leave, messages, moderation)
- Starboard system

### Permissions & Security
- Role-based permission checking
- Bot master system for special commands
- Guild owner overrides
- Audit logging for permission denials

### Logging & Events
- Member join/leave logging
- Message edit/delete logging
- Moderation action logging
- Starboard for reaction tracking

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure with environment variables
export TOKEN="your-token"
export BOT_MASTERS="your-user-id"

# 3. Run the bot
python main.py
```

## Configuration

### Environment Variables (Recommended)
```bash
export TOKEN="your-discord-bot-token"
export BOT_MASTERS="123456789,987654321"  # Comma-separated user IDs
export TWITCH_CLIENT_ID="your-twitch-id"
export STEAM_API_KEY="your-steam-key"
```

### Or use .env file
Create `.env` in the project root and the bot will auto-load it.

### Or use config.py
Copy `example-config.py` to `config.py` and edit directly (not recommended for secrets).

## Project Structure

```
cogs/                  # Command modules (admin, moderation, fun, etc.)
events/                # Event handlers (logging, errors, integrations)
utils/                 # Utility modules (formatting, permissions, settings)
data/                  # Data storage (JSON-based persistence)
assets/                # Static assets (fonts, images)
main.py                # Bot entry point
requirements.txt       # Python dependencies
```

## Commands

### Admin Commands
| Command | Description | Example |
|---------|-------------|---------|
| `?config` | View/set server configuration | `?config prefix !` |
| `?eval` | Execute Python code (masters only) | `?eval print("hello")` |
| `?description` | Set channel topic | `?description Welcome to this channel` |
| `?channelname` | Change channel name | `?channelname general` |
| `?tag` | Manage server tags | `?tag create rules <content>` |
| `?joinleave` | Configure member logging | `?joinleave #logs` |
| `?messagelogs` | Configure message logging | `?messagelogs #mod-logs` |
| `?modaudit` | Configure moderation logging | `?modaudit #audit` |
| `?starboard` | Configure starboard | `?starboard #highlights` |

### Moderation Commands
| Command | Description |
|---------|-------------|
| `?records` | View user moderation history |
| `?history` | Alias for records |
| `?infractions` | Alias for records |

### Fun Commands
| Command | Description |
|---------|-------------|
| `?roll` | Roll dice (e.g., `?roll 2d6`) |
| `?coinflip` | Flip a coin |
| `?hug` | Give someone a hug |

## Architecture

### Cog System
Commands are organized into "cogs" - modular command groups:
- **admin.py**: Server administration commands
- **moderation.py**: User moderation and tracking
- **fun.py**: Entertainment and games
- **casual.py**: Casual interaction commands
- **help.py**: Help system

### Event System
Event handlers process Discord events:
- **Core events**: Error handling, logging, message processing
- **Feature events**: Starboard, user tracking
- **Integration events**: External service integrations (Twitch, YouTube, Minecraft)

### Utilities
Reusable components:
- **formatting.py**: Text/embed builders
- **permissions.py**: Permission decorators and checking
- **settings.py**: Per-server settings management
- **cache.py**: In-memory caching
- **time.py**: Time parsing utilities

## Development

### Adding a Command
```python
# In a cog file
@commands.command()
@PermissionHandler.has_permissions(administrator=True)
async def mycommand(self, ctx: commands.Context) -> None:
    """Command description."""
    await ctx.send("Response")
```

### Adding an Event Handler
```python
# In events/core/events.py (or new file)
@commands.Cog.listener()
async def on_message(self, message: discord.Message) -> None:
    """Handle message events."""
    if message.author.bot:
        return
    # Your logic here
```

### Using Logging
```python
import logging
logger = logging.getLogger(__name__)

logger.info("Important information")
logger.warning("Warning message")
logger.error("Error message")
logger.debug("Debug info")
```

## Permissions

### Bot Master Permissions
- `?eval` - Execute Python code

### Administrator Permissions
- Config commands
- Tag management
- Logging configuration
- Starboard management

### Moderator Permissions
- User record lookup
- Limited moderation actions

## Data Storage

Settings are stored in JSON files:
- `data/settings.json` - Per-server configuration
- `data/mod_logs.json` - Moderation history
- `data/strings.json` - Bot strings and status messages

All files are auto-created on first run.