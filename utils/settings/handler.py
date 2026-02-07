import json
import os
import logging
from typing import Dict, Any, Optional
from .defaults import DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

class ServerSettings:
    """Handles per-server settings management with JSON persistence."""
    
    def __init__(self) -> None:
        """Initialize settings handler and ensure data directory exists."""
        self.settings_file = 'data/settings.json'
        self.settings: Dict[str, Any] = self._load_settings()
        os.makedirs('data', exist_ok=True)

    def _load_settings(self) -> Dict[str, Any]:
        """Load settings from file with error handling."""
        try:
            with open(self.settings_file, 'r') as f:
                data = json.load(f)
                logger.info(f"Loaded settings for {len(data)} guilds")
                return data
        except FileNotFoundError:
            logger.info("Settings file not found, starting with empty settings")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse settings.json: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error loading settings: {e}")
            return {}

    def _save_settings(self) -> None:
        """Save settings to file with error handling."""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
        except IOError as e:
            logger.error(f"Failed to save settings: {e}")
        except Exception as e:
            logger.error(f"Unexpected error saving settings: {e}")

    def get_server_setting(self, guild_id: int, setting: str) -> Optional[Any]:
        """Get a specific setting for a server"""
        guild_settings = self.settings.get(str(guild_id), {})
        return guild_settings.get(setting, DEFAULT_SETTINGS.get(setting))

    def get_all_server_settings(self, guild_id: int) -> Dict[str, Any]:
        """Get all settings for a server"""
        guild_settings = self.settings.get(str(guild_id), {})
        return {**DEFAULT_SETTINGS, **guild_settings}

    def set_server_setting(self, guild_id: int, setting: str, value: Any) -> None:
        """Set a specific setting for a server"""
        if str(guild_id) not in self.settings:
            self.settings[str(guild_id)] = {}
            
        self.settings[str(guild_id)][setting] = value
        self._save_settings()

    def remove_server_setting(self, guild_id: int, setting: str) -> None:
        """Remove a specific setting for a server"""
        if str(guild_id) in self.settings:
            self.settings[str(guild_id)].pop(setting, None)
            self._save_settings()

    def clear_server_settings(self, guild_id: int) -> None:
        """Clear all settings for a server"""
        self.settings.pop(str(guild_id), None)
        self._save_settings() 