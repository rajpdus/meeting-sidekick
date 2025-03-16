"""
Notification module for Meeting Sidekick.
Handles desktop notifications for insights and other events.
"""

import platform
from plyer import notification

class NotificationManager:
    def __init__(self):
        """Initialize the notification manager."""
        self.enabled = True
        self.platform = platform.system()
        
    def enable(self):
        """Enable notifications."""
        self.enabled = True
        
    def disable(self):
        """Disable notifications."""
        self.enabled = False
        
    def notify(self, title, message, timeout=10):
        """
        Send a desktop notification.
        
        Args:
            title (str): Notification title
            message (str): Notification message
            timeout (int): Notification timeout in seconds
        """
        if not self.enabled:
            return
            
        try:
            notification.notify(
                title=title,
                message=message,
                timeout=timeout
            )
        except Exception as e:
            print(f"Error sending notification: {e}")
            
    def notify_insight(self, insight):
        """
        Send a notification for a new insight.
        
        Args:
            insight (dict): Insight dictionary with 'title' and 'detail' keys
        """
        title = f"Meeting Insight: {insight.get('title', 'New Insight')}"
        message = insight.get('detail', 'No details available')
        
        self.notify(title, message)
        
    def notify_action_item(self, action_item):
        """
        Send a notification for a new action item.
        
        Args:
            action_item (dict): Action item dictionary
        """
        person = action_item.get('person', 'Someone')
        task = action_item.get('task', 'Do something')
        
        title = f"New Action Item for {person}"
        message = task
        
        self.notify(title, message)
        
    def notify_recording_started(self):
        """Send a notification that recording has started."""
        self.notify(
            "Meeting Sidekick",
            "Recording started. Your meeting is now being transcribed."
        )
        
    def notify_recording_stopped(self):
        """Send a notification that recording has stopped."""
        self.notify(
            "Meeting Sidekick",
            "Recording stopped. Meeting data is now available for export."
        )
