"""
Export module for Meeting Sidekick.
Handles exporting meeting data to various formats.
"""

import json
import os
from datetime import datetime
from pathlib import Path

def sanitize_filename(filename):
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def generate_filename(meeting_title, extension):
    """
    Generate a filename for the meeting export.
    
    Args:
        meeting_title (str): Meeting title
        extension (str): File extension
        
    Returns:
        str: Generated filename
    """
    # Get current date and time
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Sanitize the meeting title
    safe_title = sanitize_filename(meeting_title)
    
    # Generate the filename
    return f"{safe_title}_{date_str}.{extension}"

def export_to_markdown(meeting_data, export_dir):
    """
    Export meeting data to a Markdown file.
    
    Args:
        meeting_data (dict): Meeting data
        export_dir (Path): Export directory
        
    Returns:
        str: Path to the exported file
    """
    # Generate filename
    filename = generate_filename(meeting_data['title'], "md")
    filepath = export_dir / filename
    
    # Format the markdown content
    content = f"# {meeting_data['title']}\n\n"
    content += f"**Date:** {meeting_data['date']}\n\n"
    
    # Add summary
    content += "## Summary\n\n"
    content += f"{meeting_data['summary']}\n\n"
    
    # Add action items
    content += "## Action Items\n\n"
    if meeting_data['action_items']:
        for item in meeting_data['action_items']:
            person = item.get('person', 'Unassigned')
            task = item.get('task', 'No task')
            deadline = item.get('deadline', '')
            priority = item.get('priority', '')
            
            content += f"- **{person}:** {task}"
            if deadline:
                content += f" (Deadline: {deadline})"
            if priority:
                content += f" [Priority: {priority}]"
            content += "\n"
    else:
        content += "No action items.\n"
    
    # Add transcript
    content += "\n## Full Transcript\n\n"
    content += "```\n"
    content += meeting_data['transcript']
    content += "\n```\n"
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    return str(filepath)

def export_to_json(meeting_data, export_dir):
    """
    Export meeting data to a JSON file.
    
    Args:
        meeting_data (dict): Meeting data
        export_dir (Path): Export directory
        
    Returns:
        str: Path to the exported file
    """
    # Generate filename
    filename = generate_filename(meeting_data['title'], "json")
    filepath = export_dir / filename
    
    # Write to file
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(meeting_data, f, indent=2)
        
    return str(filepath)

def export_to_file(meeting_data, output_format="markdown"):
    """
    Export meeting data to a file.
    
    Args:
        meeting_data (dict): Meeting data
        output_format (str): Output format ("markdown" or "json")
        
    Returns:
        str: Path to the exported file
    """
    # Create the export directory if it doesn't exist
    export_dir = Path("meeting_exports")
    export_dir.mkdir(exist_ok=True)
    
    # Export based on the format
    if output_format.lower() == "json":
        return export_to_json(meeting_data, export_dir)
    else:
        return export_to_markdown(meeting_data, export_dir)
