"""
Configuration module for Meeting Sidekick.
Handles loading configuration from environment variables and files.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Default configuration
DEFAULT_CONFIG = {
    "openai_api_key": "",
    "whisper_model": "base",
    "enable_notifications": True,
    "summary_update_interval": 25,  # seconds
    "action_items_update_interval": 50,  # seconds
    "insight_cooldown": 30,  # seconds
    "export_directory": "meeting_exports"
}

class Config:
    def __init__(self):
        """Initialize configuration with default values."""
        self.config = DEFAULT_CONFIG.copy()
        self.config_file = self._get_config_file_path()
        
        # Load environment variables
        load_dotenv()
        
        # Load configuration from file if it exists
        self._load_config_from_file()
        
        # Override with environment variables
        self._load_config_from_env()
        
    def _get_config_file_path(self):
        """Get the configuration file path."""
        # Get the user's home directory
        home_dir = Path.home()
        
        # Create .meeting_sidekick directory if it doesn't exist
        config_dir = home_dir / ".meeting_sidekick"
        config_dir.mkdir(exist_ok=True)
        
        # Configuration file path
        return config_dir / "config.json"
        
    def _load_config_from_file(self):
        """Load configuration from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    file_config = json.load(f)
                    # Update config with file values
                    self.config.update(file_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config file: {e}")
                
    def _load_config_from_env(self):
        """Load configuration from environment variables."""
        # OpenAI API key
        if 'OPENAI_API_KEY' in os.environ:
            self.config['openai_api_key'] = os.environ['OPENAI_API_KEY']
            
        # Whisper model
        if 'WHISPER_MODEL' in os.environ:
            self.config['whisper_model'] = os.environ['WHISPER_MODEL']
            
        # Notifications
        if 'ENABLE_NOTIFICATIONS' in os.environ:
            self.config['enable_notifications'] = os.environ['ENABLE_NOTIFICATIONS'].lower() in ('true', '1', 'yes')
            
        # Update intervals
        if 'SUMMARY_UPDATE_INTERVAL' in os.environ:
            try:
                self.config['summary_update_interval'] = int(os.environ['SUMMARY_UPDATE_INTERVAL'])
            except ValueError:
                pass
                
        if 'ACTION_ITEMS_UPDATE_INTERVAL' in os.environ:
            try:
                self.config['action_items_update_interval'] = int(os.environ['ACTION_ITEMS_UPDATE_INTERVAL'])
            except ValueError:
                pass
                
        if 'INSIGHT_COOLDOWN' in os.environ:
            try:
                self.config['insight_cooldown'] = int(os.environ['INSIGHT_COOLDOWN'])
            except ValueError:
                pass
                
        # Export directory
        if 'EXPORT_DIRECTORY' in os.environ:
            self.config['export_directory'] = os.environ['EXPORT_DIRECTORY']
            
    def save_config(self):
        """Save the current configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Error saving config file: {e}")
            
    def get(self, key, default=None):
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            The configuration value or default
        """
        return self.config.get(key, default)
        
    def set(self, key, value):
        """
        Set a configuration value.
        
        Args:
            key (str): Configuration key
            value: Configuration value
        """
        self.config[key] = value
        
    def has_api_key(self):
        """
        Check if the OpenAI API key is set.
        
        Returns:
            bool: True if API key is set, False otherwise
        """
        return bool(self.get('openai_api_key'))
        
    def get_export_dir(self):
        """
        Get the export directory, creating it if it doesn't exist.
        
        Returns:
            Path: Path to export directory
        """
        export_dir = Path(self.get('export_directory'))
        
        # Create the directory if it doesn't exist
        export_dir.mkdir(exist_ok=True)
        
        return export_dir
