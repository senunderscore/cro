import re
from typing import List, Dict, Any, Optional
import discord
import logging

logger = logging.getLogger(__name__)

class TextFormatter:
    """Utilities for text formatting and manipulation."""
    
    @staticmethod
    def truncate(text: str, max_length: int = 2000) -> str:
        """Truncate text to max_length, accounting for markdown.
        
        Args:
            text: The text to truncate
            max_length: Maximum length (default 2000 for Discord limits)
            
        Returns:
            Truncated text with proper markdown closure
        """
        if len(text) <= max_length:
            return text
            
        truncated = text[:max_length-3] + "..."
        
        unclosed_bold = truncated.count('**') % 2
        unclosed_italic = truncated.count('*') % 2
        unclosed_code = truncated.count('`') % 2
        
        if unclosed_bold:
            truncated += "**"
        if unclosed_italic:
            truncated += "*"
        if unclosed_code:
            truncated += "`"
            
        return truncated

    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text of mentions and markdown for safe evaluation.
        
        Args:
            text: The text to clean
            
        Returns:
            Escaped text safe for evaluation
        """
        text = discord.utils.escape_mentions(text)
        text = discord.utils.escape_markdown(text)
        return text

    @staticmethod
    def parse_flags(text: str) -> Dict[str, Any]:
        """Parse command flags from text.
        
        Example:
            'hello --user @someone --contains test' ->
            {'user': '@someone', 'contains': 'test'}
            
        Args:
            text: Text to parse for flags
            
        Returns:
            Dictionary of parsed flags
        """
        flags: Dict[str, Any] = {}
        current_flag: Optional[str] = None
        parts = text.split()
        
        for part in parts:
            if part.startswith('--'):
                current_flag = part[2:]
                flags[current_flag] = True
            elif current_flag:
                if flags[current_flag] is True:
                    flags[current_flag] = part
                else:
                    flags[current_flag] = f"{flags[current_flag]} {part}"
                    
        return flags

class EmbedBuilder:
    """Builder pattern for creating Discord embeds fluently."""
    
    def __init__(self, title: Optional[str] = None, 
                 description: Optional[str] = None, 
                 color: Optional[discord.Color] = None) -> None:
        """Initialize embed builder.
        
        Args:
            title: Optional embed title
            description: Optional embed description
            color: Optional embed color
        """
        self.embed = discord.Embed(
            title=title,
            description=description,
            color=color
        )

    def add_field(self, name: str, value: str, inline: bool = True) -> 'EmbedBuilder':
        """Add a field to the embed.
        
        Args:
            name: Field name
            value: Field value (will be truncated to 1024 chars)
            inline: Whether field should be inline
            
        Returns:
            Self for method chaining
        """
        if value:
            self.embed.add_field(
                name=name,
                value=TextFormatter.truncate(str(value), 1024),
                inline=inline
            )
        return self

    def set_author(self, name: str, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        """Set the author of the embed.
        
        Args:
            name: Author name
            icon_url: Optional author icon URL
            
        Returns:
            Self for method chaining
        """
        self.embed.set_author(name=name, icon_url=icon_url)
        return self

    def set_footer(self, text: str, icon_url: Optional[str] = None) -> 'EmbedBuilder':
        """Set the footer of the embed.
        
        Args:
            text: Footer text
            icon_url: Optional footer icon URL
            
        Returns:
            Self for method chaining
        """
        self.embed.set_footer(text=text, icon_url=icon_url)
        return self

    def set_thumbnail(self, url: str) -> 'EmbedBuilder':
        """Set the thumbnail of the embed.
        
        Args:
            url: Thumbnail URL
            
        Returns:
            Self for method chaining
        """
        self.embed.set_thumbnail(url=url)
        return self

    def build(self) -> discord.Embed:
        """Return the built embed.
        
        Returns:
            The constructed discord.Embed object
        """
        return self.embed