"""
Command-line interface for the Meeting Sidekick application.
Uses the Rich library for enhanced terminal visuals.
"""

import time
import threading
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
import click

from ..processing.insights import format_insight_for_display

class MeetingSidekickCLI:
    def __init__(self, recorder, assistant):
        """
        Initialize the CLI interface.
        
        Args:
            recorder: SpeechRecognizer instance
            assistant: MeetingAssistant instance
        """
        self.recorder = recorder
        self.assistant = assistant
        self.console = Console()
        self.layout = None
        self.live = None
        self.recording = False
        self.transcript_text = []
        self.current_insights = []
        self.summary_text = ""
        self.action_items = []
        
        # Set up callbacks
        self.recorder.set_transcription_callback(self.on_new_transcription)
        self.assistant.set_insight_callback(self.on_new_insights)
        
        # Thread for updating summary and action items
        self.update_thread = None
        self.should_update = False
        
    def on_new_transcription(self, text):
        """Handle new transcription from the recorder."""
        self.transcript_text.append(text)
        self.assistant.add_transcript(text)
        
    def on_new_insights(self, insights):
        """Handle new insights from the assistant."""
        self.current_insights = insights
        
    def generate_layout(self):
        """Generate the Rich layout for the application."""
        layout = Layout(name="root")
        
        # Split the screen into two main sections
        layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1)
        )
        
        # Split the main section into body and sidebar
        layout["main"].split_row(
            Layout(name="body", ratio=2),
            Layout(name="sidebar", ratio=1)
        )
        
        # Split the body into transcript and summary
        layout["body"].split(
            Layout(name="transcript", ratio=2),
            Layout(name="summary", ratio=1)
        )
        
        # Split the sidebar into insights and action items
        layout["sidebar"].split(
            Layout(name="insights", ratio=1),
            Layout(name="action_items", ratio=1)
        )
        
        return layout
        
    def update_layout(self):
        """Update the layout with current data."""
        # Header
        status = "[bold green]Recording[/bold green]" if self.recording else "[bold red]Not Recording[/bold red]"
        self.layout["header"].update(
            Panel(f"Meeting Sidekick - {status}", 
                  style="bold white on blue")
        )
        
        # Transcript
        transcript_content = "\n".join(self.transcript_text[-20:])  # Show last 20 lines
        self.layout["transcript"].update(
            Panel(
                Text(transcript_content) if transcript_content else Text("No transcript yet...", style="dim"),
                title="Live Transcript",
                border_style="green" if self.recording else "red"
            )
        )
        
        # Summary
        self.layout["summary"].update(
            Panel(
                Markdown(self.summary_text) if self.summary_text else Text("Summary will appear here...", style="dim"),
                title="Meeting Summary",
                border_style="cyan"
            )
        )
        
        # Insights
        insights_content = ""
        for insight in self.current_insights:
            insights_content += format_insight_for_display(insight) + "\n\n"
            
        self.layout["insights"].update(
            Panel(
                Text.from_markup(insights_content) if insights_content else Text("Insights will appear here...", style="dim"),
                title="Insights",
                border_style="magenta"
            )
        )
        
        # Action Items
        action_table = Table(box=None)
        action_table.add_column("Person", style="cyan")
        action_table.add_column("Task", style="green")
        action_table.add_column("Deadline", style="yellow")
        action_table.add_column("Priority", style="red")
        
        for item in self.action_items:
            action_table.add_row(
                item.get("person", "Unknown"),
                item.get("task", "No task"),
                item.get("deadline", ""),
                item.get("priority", "")
            )
            
        self.layout["action_items"].update(
            Panel(
                action_table if self.action_items else Text("Action items will appear here...", style="dim"),
                title="Action Items",
                border_style="yellow"
            )
        )
    
    def update_thread_func(self):
        """Thread function to periodically update summary and action items."""
        update_counter = 0
        
        while self.should_update:
            update_counter += 1
            
            # Update summary every 5 cycles (approx. every 25 seconds)
            if update_counter % 5 == 0:
                self.summary_text = self.assistant.update_summary()
                
            # Update action items every 10 cycles (approx. every 50 seconds)
            if update_counter % 10 == 0:
                self.action_items = self.assistant.extract_action_items()
                
            time.sleep(5)  # Sleep for 5 seconds between updates
    
    def start_recording(self):
        """Start recording and processing."""
        if not self.recording:
            self.recording = True
            self.recorder.start_capture()
            self.should_update = True
            self.update_thread = threading.Thread(target=self.update_thread_func)
            self.update_thread.daemon = True
            self.update_thread.start()
            
    def stop_recording(self):
        """Stop recording and processing."""
        if self.recording:
            self.recording = False
            self.recorder.stop_capture()
            self.should_update = False
            if self.update_thread:
                self.update_thread.join(timeout=1.0)
                
            # Final update of summary and action items
            self.summary_text = self.assistant.update_summary()
            self.action_items = self.assistant.extract_action_items()
    
    def run(self):
        """Run the CLI application."""
        self.layout = self.generate_layout()
        
        # Initial update
        self.update_layout()
        
        # Create Live display
        with Live(self.layout, refresh_per_second=2, screen=True) as self.live:
            try:
                while True:
                    self.update_layout()
                    
                    # Check for keyboard input (in a real implementation, this would be more sophisticated)
                    command = click.getchar(echo=False)
                    
                    if command == 'q':
                        # Quit
                        if self.recording:
                            self.stop_recording()
                        break
                    elif command == 'r':
                        # Toggle recording
                        if self.recording:
                            self.stop_recording()
                        else:
                            self.start_recording()
                    elif command == 's':
                        # Force update summary
                        self.summary_text = self.assistant.update_summary()
                    elif command == 'a':
                        # Force update action items
                        self.action_items = self.assistant.extract_action_items()
                    elif command == 'e':
                        # Export meeting data
                        self.live.stop()
                        self.console.print("\n[bold]Exporting meeting data...[/bold]")
                        output_format = Prompt.ask(
                            "Export format", 
                            choices=["markdown", "json"], 
                            default="markdown"
                        )
                        filepath = self.assistant.export_meeting_data(output_format)
                        self.console.print(f"[bold green]Exported to:[/bold green] {filepath}")
                        self.console.print("Press any key to continue...")
                        click.getchar(echo=False)
                        self.live.start()
                    elif command == 't':
                        # Set meeting title
                        self.live.stop()
                        title = Prompt.ask("\nEnter meeting title")
                        self.assistant.set_meeting_title(title)
                        self.console.print(f"[bold green]Title set to:[/bold green] {title}")
                        self.console.print("Press any key to continue...")
                        click.getchar(echo=False)
                        self.live.start()
                    elif command == 'h':
                        # Show help
                        self.live.stop()
                        self.console.print("\n[bold]Meeting Sidekick Commands:[/bold]")
                        self.console.print("  [bold cyan]r[/bold cyan] - Toggle recording")
                        self.console.print("  [bold cyan]s[/bold cyan] - Update summary")
                        self.console.print("  [bold cyan]a[/bold cyan] - Update action items")
                        self.console.print("  [bold cyan]e[/bold cyan] - Export meeting data")
                        self.console.print("  [bold cyan]t[/bold cyan] - Set meeting title")
                        self.console.print("  [bold cyan]h[/bold cyan] - Show this help")
                        self.console.print("  [bold cyan]q[/bold cyan] - Quit")
                        self.console.print("\nPress any key to continue...")
                        click.getchar(echo=False)
                        self.live.start()
            
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                if self.recording:
                    self.stop_recording()
        
        # Clean up
        if self.recording:
            self.stop_recording()
            
        # Final summary
        self.console.print("\n[bold]Meeting Summary:[/bold]")
        self.console.print(Markdown(self.summary_text))
        
        # Final action items
        self.console.print("\n[bold]Action Items:[/bold]")
        action_table = Table()
        action_table.add_column("Person", style="cyan")
        action_table.add_column("Task", style="green")
        action_table.add_column("Deadline", style="yellow")
        action_table.add_column("Priority", style="red")
        
        for item in self.action_items:
            action_table.add_row(
                item.get("person", "Unknown"),
                item.get("task", "No task"),
                item.get("deadline", ""),
                item.get("priority", "")
            )
        
        self.console.print(action_table)
        
        # Export offer
        if Confirm.ask("Export meeting data?"):
            output_format = Prompt.ask(
                "Export format", 
                choices=["markdown", "json"], 
                default="markdown"
            )
            filepath = self.assistant.export_meeting_data(output_format)
            self.console.print(f"[bold green]Exported to:[/bold green] {filepath}")
            
        self.console.print("[bold green]Meeting Sidekick session ended.[/bold green]")
