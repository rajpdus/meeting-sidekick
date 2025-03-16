# Meeting Sidekick Architecture

This document provides an overview of the Meeting Sidekick application architecture, explaining the design decisions, component interactions, and data flow.

## System Overview

Meeting Sidekick is a Python application that provides real-time meeting assistance through speech recognition, natural language processing, and a rich command-line interface. The application is designed to be modular, extensible, and easy to understand.

## Component Architecture

The application is organized into several key modules, each with a specific responsibility:

```
meeting_sidekick/
├── __main__.py                # Entry point
├── audio/                     # Audio capture and processing
│   └── recorder.py            # Contains SpeechRecognizer class
├── processing/                # OpenAI API integration
│   └── assistant.py           # Contains MeetingAssistant class
│   └── insights.py            # Real-time insight generation
├── ui/                        # User interface
│   └── cli.py                 # Command-line interface
│   └── notifications.py       # Handles insight notifications
└── utils/                     # Utility functions
    ├── config.py              # Configuration handling
    └── export.py              # Export functionality
```

### Core Components

#### 1. Audio Module (`audio/recorder.py`)

The `SpeechRecognizer` class is responsible for:
- Capturing audio from the system microphone
- Processing audio chunks in real-time
- Using OpenAI's Whisper model for speech-to-text conversion
- Providing a callback mechanism for new transcription segments

Key design decisions:
- Uses threading to handle audio capture and processing concurrently
- Implements a buffer system to process audio in chunks for optimal recognition
- Provides a simple interface for starting and stopping recording

#### 2. Processing Module (`processing/assistant.py`, `processing/insights.py`)

The `MeetingAssistant` class is the core of the application, responsible for:
- Managing the meeting transcript
- Generating meeting summaries using OpenAI GPT models
- Extracting action items from the transcript
- Generating real-time insights during the meeting

The `insights.py` module provides supporting functions for:
- Formatting insights for display
- Categorizing insights by type
- Prioritizing insights based on relevance

Key design decisions:
- Uses OpenAI's GPT models for all language processing tasks
- Maintains a conversation context for generating relevant insights
- Implements cooldown periods to avoid overwhelming the user with insights
- Handles JSON parsing with robust error handling

#### 3. UI Module (`ui/cli.py`, `ui/notifications.py`)

The `MeetingSidekickCLI` class provides:
- A rich, interactive terminal interface using the Rich library
- Real-time updates of transcript, summary, insights, and action items
- Keyboard shortcuts for controlling the application

The `NotificationManager` class handles:
- Desktop notifications for insights and events
- Platform-specific notification behavior

Key design decisions:
- Uses Rich library for a beautiful and responsive terminal interface
- Implements a layout system with separate panels for different information types
- Uses threading for background updates of summary and action items
- Provides a simple keyboard-based interface for commands

#### 4. Utilities Module (`utils/config.py`, `utils/export.py`)

The `Config` class handles:
- Loading configuration from environment variables and files
- Providing default values for configuration options
- Saving configuration changes

The export module provides functions for:
- Exporting meeting data to different formats (Markdown, JSON)
- Generating appropriate filenames
- Formatting meeting data for export

Key design decisions:
- Uses a layered approach to configuration (defaults, file, environment variables)
- Implements a simple but flexible export system
- Handles file operations with proper error handling

### Data Flow

1. **Audio Capture and Transcription**:
   - Audio is captured from the system microphone
   - Audio chunks are processed by the Whisper model
   - Transcribed text is added to the transcript and passed to callbacks

2. **Transcript Processing**:
   - New transcript segments are added to the meeting assistant
   - The assistant updates the conversation context
   - Periodically, the assistant generates summaries and extracts action items
   - The assistant checks for opportunities to generate insights

3. **User Interface Updates**:
   - The CLI periodically updates its display with new information
   - Insights are displayed in the UI and sent as desktop notifications
   - User commands are processed to control recording, export data, etc.

4. **Data Export**:
   - Meeting data (transcript, summary, action items) is formatted
   - Data is written to files in the specified format
   - File paths are returned to the user

## API Integration

Meeting Sidekick integrates with the following external APIs:

1. **OpenAI API**:
   - Used for speech recognition via Whisper models
   - Used for natural language processing via GPT models
   - Handles all text generation, summarization, and insight creation

## Extension Points

The application is designed to be extensible in several ways:

1. **Alternative Speech Recognition**:
   - The `SpeechRecognizer` class could be extended or replaced to use different speech recognition engines

2. **Additional Export Formats**:
   - New export formats can be added by implementing additional export functions in `export.py`

3. **UI Alternatives**:
   - The CLI interface could be replaced with a web or desktop GUI
   - The notification system could be extended to support additional platforms

4. **Enhanced Insights**:
   - The insight generation system could be extended with domain-specific knowledge
   - Additional categorization and prioritization algorithms could be implemented

## Performance Considerations

1. **Speech Recognition**:
   - Whisper model size affects both accuracy and performance
   - Smaller models run faster but may have lower accuracy
   - Audio preprocessing affects recognition quality

2. **API Usage**:
   - OpenAI API calls are rate-limited and incur costs
   - The application implements cooldown periods to manage API usage
   - Batch processing is used where appropriate to minimize API calls

3. **Memory Usage**:
   - The application maintains the full transcript in memory
   - For very long meetings, this could potentially cause memory issues
   - Future versions could implement streaming or database storage for transcripts

## Security and Privacy

1. **API Keys**:
   - OpenAI API keys are stored in configuration files or environment variables
   - Keys are never exposed in the UI or exported data

2. **Data Storage**:
   - Meeting data is only stored locally when explicitly exported
   - No data is sent to external services except through the OpenAI API
   - Exported files contain potentially sensitive meeting information and should be handled accordingly

## Future Architecture Directions

1. **Web Interface**:
   - A web-based interface could provide more flexibility and remote access
   - WebSocket connections could enable real-time updates in a browser

2. **Meeting Platform Integration**:
   - Direct integration with platforms like Zoom, Teams, or Google Meet
   - Capture audio directly from meeting platforms instead of system microphone

3. **Database Backend**:
   - Store meeting data in a database for persistence and search
   - Enable historical analysis of meeting patterns and action items

4. **Multi-user Support**:
   - Allow multiple users to access the same meeting data
   - Implement user authentication and authorization

5. **Offline Mode**:
   - Implement local models for basic functionality without internet access
   - Cache frequently used prompts and responses 