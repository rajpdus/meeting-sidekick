"""
Main entry point for the Meeting Sidekick application.
"""

import os
import click
from rich.console import Console
from rich.prompt import Prompt

from .audio.recorder import SpeechRecognizer
from .processing.assistant import MeetingAssistant
from .ui.cli import MeetingSidekickCLI
from .ui.notifications import NotificationManager
from .utils.config import Config

console = Console()

@click.group()
def cli():
    """Meeting Sidekick: AI-powered meeting assistant"""
    pass

@cli.command()
@click.option('--api-key', help='OpenAI API key')
@click.option('--whisper-model', default='base', help='Whisper model to use for transcription')
def run(api_key, whisper_model):
    """Run the Meeting Sidekick application"""
    # Load configuration
    config = Config()
    
    # Check if API key is provided
    if api_key:
        config.set('openai_api_key', api_key)
    
    # Check if we have an API key
    if not config.has_api_key():
        console.print("[bold red]Error:[/bold red] OpenAI API key is required.")
        api_key = Prompt.ask("Please enter your OpenAI API key")
        config.set('openai_api_key', api_key)
        config.save_config()
    
    # Update whisper model if provided
    if whisper_model:
        config.set('whisper_model', whisper_model)
    
    # Initialize components
    console.print("[bold blue]Initializing Meeting Sidekick...[/bold blue]")
    
    # Initialize notification manager
    notification_manager = NotificationManager()
    if not config.get('enable_notifications', True):
        notification_manager.disable()
    
    try:
        # Initialize speech recognition
        console.print("Loading Whisper model...")
        recorder = SpeechRecognizer(model_name=config.get('whisper_model', 'base'))
        
        # Initialize meeting assistant
        console.print("Initializing OpenAI client...")
        assistant = MeetingAssistant(api_key=config.get('openai_api_key'))
        assistant.insight_cooldown = config.get('insight_cooldown', 30)
        
        # Initialize CLI
        console.print("Setting up interface...")
        cli_app = MeetingSidekickCLI(recorder, assistant)
        
        # Add notification integration
        def on_insight(insights):
            for insight in insights:
                notification_manager.notify_insight(insight)
                
        assistant.set_insight_callback(on_insight)
        
        # Run the application
        console.print("[bold green]Meeting Sidekick is ready![/bold green]")
        console.print("Press [bold cyan]h[/bold cyan] for help, [bold cyan]r[/bold cyan] to start/stop recording, [bold cyan]q[/bold cyan] to quit")
        cli_app.run()
        
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return

@cli.command()
def setup():
    """Set up Meeting Sidekick configuration"""
    config = Config()
    
    console.print("[bold blue]Meeting Sidekick Setup[/bold blue]")
    
    # Get OpenAI API key
    api_key = Prompt.ask("Enter your OpenAI API key", default=config.get('openai_api_key', ''))
    config.set('openai_api_key', api_key)
    
    # Choose Whisper model
    whisper_model = Prompt.ask(
        "Choose Whisper model",
        choices=["tiny", "base", "small", "medium", "large"],
        default=config.get('whisper_model', 'base')
    )
    config.set('whisper_model', whisper_model)
    
    # Enable notifications
    enable_notifications = click.confirm("Enable desktop notifications?", default=config.get('enable_notifications', True))
    config.set('enable_notifications', enable_notifications)
    
    # Save configuration
    config.save_config()
    console.print("[bold green]Configuration saved successfully![/bold green]")

def main():
    """Main entry point"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Meeting Sidekick terminated by user.[/bold yellow]")
    except Exception as e:
        console.print(f"\n[bold red]An error occurred:[/bold red] {e}")

if __name__ == "__main__":
    main()
