from functools import wraps
from discord.ext import commands
from typing import Callable, Any
import logging
from config import BOT_MASTERS

logger = logging.getLogger(__name__)

class PermissionHandler:
    """Handles permission checking for commands via decorators."""
    
    @staticmethod
    def has_permissions(**permissions: bool) -> Callable:
        """Check if a user has all required permissions.
        
        Usage:
            @PermissionHandler.has_permissions(manage_messages=True)
            async def some_command(self, ctx):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(self: Any, ctx: commands.Context, *args: Any, **kwargs: Any) -> Any:
                # Bot masters and guild owners bypass checks
                if str(ctx.author.id) in BOT_MASTERS or ctx.author == ctx.guild.owner:
                    logger.debug(f"Permission bypass for {ctx.author} in {ctx.command.name}")
                    return await func(self, ctx, *args, **kwargs)

                # Check each required permission
                missing_perms = []
                for perm, required in permissions.items():
                    if required and not getattr(ctx.author.guild_permissions, perm, False):
                        formatted_perm = ' '.join(word.capitalize() for word in perm.split('_'))
                        missing_perms.append(formatted_perm)

                if missing_perms:
                    if len(missing_perms) == 1:
                        await ctx.send("You don't have permission to use this command.")
                    else:
                        perms_list = '`, `'.join(missing_perms)
                        await ctx.send(f"You need the following permissions to use this command:\n`{perms_list}`")
                    logger.warning(f"Permission denied for {ctx.author} - missing: {missing_perms}")
                    return None

                return await func(self, ctx, *args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def is_bot_master() -> Callable:
        """Check if user is a bot master.
        
        Usage:
            @PermissionHandler.is_bot_master()
            async def admin_command(self, ctx):
                ...
        """
        def decorator(func: Callable) -> Callable:
            @wraps(func)
            async def wrapper(self: Any, ctx: commands.Context, *args: Any, **kwargs: Any) -> Any:
                if str(ctx.author.id) not in BOT_MASTERS:
                    await ctx.send("This command is only available to bot developers.")
                    logger.warning(f"Unauthorized access attempt by {ctx.author} to {ctx.command.name}")
                    return None
                return await func(self, ctx, *args, **kwargs)
            return wrapper
        return decorator 