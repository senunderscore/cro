import discord
from discord.ext import commands
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class Help(commands.Cog):
    """Help and command discovery system."""
    
    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the Help cog."""
        self.bot = bot
        self.cog_emojis = {}

    def _format_command_signature(self, command: commands.Command, prefix: str) -> str:
        """Format a command signature for display.
        
        Args:
            command: The command to format
            prefix: The guild's command prefix
            
        Returns:
            Formatted command signature
        """
        if command.signature:
            return f"{prefix}{command.qualified_name} {command.signature}"
        return f"{prefix}{command.qualified_name}"

    async def _can_run_command(self, ctx: commands.Context, command: commands.Command) -> bool:
        """Check if a user can run a command.
        
        Args:
            ctx: Command context
            command: Command to check
            
        Returns:
            True if user can run the command
        """
        try:
            return await command.can_run(ctx)
        except (commands.MissingPermissions, 
               commands.MissingRole, 
               commands.MissingAnyRole,
               commands.NotOwner):
            return False
        except Exception as e:
            logger.debug(f"Error checking command permission: {e}")
            return False

    @commands.command(aliases=['h'])
    async def help(self, ctx: commands.Context, *, command_name: Optional[str] = None) -> None:
        """Get help about anything.
        
        **Examples:**
        • `?help` — See what I can do
        • `?help eval` — Learn about the eval command
        • `?help admin` — See all admin commands
        • `?help moderation` — See all moderation commands
        
        **Pro tips:**
        • You can use `?h` or just `?` instead of `?help`
        • Use `?commands` to see everything organized
        • Missing help? Use `?help <category>` instead
        """
        if command_name:
            command = self.bot.get_command(command_name)
            
            if command:
                can_run = await self._can_run_command(ctx, command)
                member = ctx.guild.get_member(self.bot.user.id) if ctx.guild else None
                color = member.color if member else discord.Color.blurple()

                signature = self._format_command_signature(command, ctx.prefix)
                embed = discord.Embed(
                    title=f"{command.qualified_name}",
                    description=command.help or "No description available",
                    color=color
                )

                embed.set_author(name="Command Help")
                try:
                    embed.set_thumbnail(url=self.bot.user.display_avatar.url)
                except Exception:
                    pass

                embed.add_field(name="Usage", value=f"```\n{signature}\n```", inline=False)

                if command.aliases:
                    aliases = ", ".join(f"`{alias}`" for alias in command.aliases)
                    embed.add_field(name="Aliases", value=aliases, inline=True)

                perms = getattr(command, 'permissions', None)
                if perms:
                    perms_str = ", ".join(p.replace('_', ' ').title() for p in perms)
                    embed.add_field(name="Permissions", value=perms_str, inline=True)

                status = "You can use this" if can_run else "You can't use this (missing permissions)"
                embed.set_footer(text=status)
                await ctx.send(embed=embed)
                return
            
            cog = self.bot.get_cog(command_name.title())
            if cog:
                await self._show_cog_help(ctx, cog)
                return
            
            embed = discord.Embed(
                title="Not Found",
                description=f"I couldn't find a command or category called `{command_name}`.",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Tip",
                value=f"Try `{ctx.prefix}commands` to see all available commands!"
            )
            await ctx.send(embed=embed)
            return
        
        await self._show_general_help(ctx)

    async def _show_general_help(self, ctx: commands.Context) -> None:
        """Show the main help page.
        
        Args:
            ctx: Command context
        """
        member = ctx.guild.get_member(self.bot.user.id) if ctx.guild else None
        color = member.color if member else 0x2B2D31

        embed = discord.Embed(
            title="About Cro",
            description="Cro is a multipurpose bot built with 💜",
            color=color
        )

        try:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        except Exception:
            pass

        embed.add_field(
            name="Getting Help",
            value=(
                f"`{ctx.prefix}help <command>` — Learn about a specific command\n"
                f"`{ctx.prefix}help <category>` — See all commands in a category\n"
                f"`{ctx.prefix}commands` — Browse everything organized by category"
            ),
            inline=False
        )

        categories = [c for c in self.bot.cogs if c not in ['EventHandlers', 'MessageEvents']]
        if categories:
            embed.add_field(name="What I Can Do", value=" • ".join(f"**{c}**" for c in categories), inline=False)

        embed.add_field(
            name="Quick Start",
            value=(
                "1. Run `?commands` to see what's available\n"
                "2. `?help <command>` for details\n"
                "3. Configure with `?config` for server-specific options"
            ),
            inline=False
        )

        embed.add_field(
            name="Pro Tips",
            value=(
                f"Alias for help: `?h`\n"
                f"Change prefix: `{ctx.prefix}config prefix <new>`\n"
                f"Need admin tools? Try `{ctx.prefix}admin` commands"
            ),
            inline=False
        )

        embed.set_footer(text="Use ?help <command> for details on any command.")
        await ctx.send(embed=embed)

    @commands.command(name="listcogs")
    async def listcogs(self, ctx: commands.Context) -> None:
        """(Debug) List loaded cogs for the running bot."""
        cogs = ", ".join(self.bot.cogs.keys()) or "(none)"
        await ctx.send(f"Loaded cogs: {cogs}")

    async def _show_cog_help(self, ctx: commands.Context, cog: commands.Cog) -> None:
        """Show help for a specific category/cog.
        
        Args:
            ctx: Command context
            cog: The cog to show help for
        """
        visible_commands = []
        hidden_commands = 0
        
        for cmd in cog.get_commands():
            if cmd.hidden:
                hidden_commands += 1
                continue
            
            if await self._can_run_command(ctx, cmd):
                visible_commands.append(cmd)
        
        if not visible_commands and hidden_commands == 0:
            await ctx.send(f"No commands found in the {cog.qualified_name} category.")
            return
        
        embed = discord.Embed(
            title=f"{cog.qualified_name} Commands",
            description=cog.description or f"Commands from the {cog.qualified_name} category",
            color=discord.Color.blurple()
        )
        try:
            embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        except Exception:
            pass
        
        visible_commands.sort(key=lambda x: x.name)
        
        for cmd in visible_commands:
            signature = self._format_command_signature(cmd, ctx.prefix)
            cmd_description = (cmd.help or "No description").split('\n')[0]
            
            aliases_str = ""
            if cmd.aliases:
                aliases_str = f" `[{', '.join(cmd.aliases)}]`"
            
            embed.add_field(
                name=f"→ {signature}{aliases_str}",
                value=cmd_description,
                inline=False
            )
        
        if hidden_commands > 0:
            embed.set_footer(text=f"{hidden_commands} command(s) hidden (no permission)")
        else:
            embed.set_footer(text="Need help with a command? Use ?help <command>")
        
        await ctx.send(embed=embed)

    @commands.command(aliases=['cmds', 'cmd'])
    async def commands(self, ctx: commands.Context) -> None:
        """See all available commands organized by category.
        
        This is basically the command catalog - everything I can do for your server.
        
        **Want details?** Use `?help <command>` for any command you see here
        **Want to explore?** Use `?help <category>` to dive into a specific area
        """
        commands_by_cog = {}
        permission_limited = {}
        
        for cog_name, cog in self.bot.cogs.items():
            if cog_name in ['EventHandlers', 'MessageEvents']:
                continue
            
            visible_commands = []
            hidden_commands = 0
            
            for cmd in cog.get_commands():
                if cmd.hidden:
                    hidden_commands += 1
                    continue
                
                if await self._can_run_command(ctx, cmd):
                    visible_commands.append(cmd)
            
            if visible_commands:
                commands_by_cog[cog_name] = visible_commands
                if hidden_commands > 0:
                    permission_limited[cog_name] = hidden_commands
        
        if not commands_by_cog:
            await ctx.send("No commands available for you.")
            return
        
        embed = discord.Embed(
            title="All Available Commands",
            description=(
                f"**Quick help:** Use `{ctx.prefix}help <command>` for details\n"
                f"**Explore:** Use `{ctx.prefix}help <category>` to see a category\n"
                f"**Aliases:** Some commands have shortcuts (shown in help)"
            ),
            color=discord.Color.blurple()
        )
        
        cog_order = ['Admin', 'Moderation', 'Fun', 'Casual', 'Help']
        sorted_cogs = []
        
        for cog_name in cog_order:
            if cog_name in commands_by_cog:
                sorted_cogs.append(cog_name)
        
        for cog_name in sorted(commands_by_cog.keys()):
            if cog_name not in sorted_cogs:
                sorted_cogs.append(cog_name)
        
        for cog_name in sorted_cogs:
            cmds = commands_by_cog[cog_name]
            
            cmd_names = ", ".join(f"`{cmd.name}`" for cmd in sorted(cmds, key=lambda x: x.name))
            
            info = ""
            if cog_name in permission_limited:
                hidden = permission_limited[cog_name]
                info = f" *({hidden} more hidden)*"
            
            embed.add_field(
                name=f"{cog_name}{info}",
                value=cmd_names if cmd_names else "*No commands visible*",
                inline=False
            )
        
        embed.set_footer(
            text="Tip: Just mention me to see my current prefix! | ?help is your friend"
        )
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    """Load the Help cog."""
    await bot.add_cog(Help(bot))