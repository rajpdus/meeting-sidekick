# Meeting Sidekick: Simplified Implementation Plan

## Overview

Meeting Sidekick is a real-time virtual assistant designed to enhance meeting experiences by automating note-taking, summarizing discussions, tracking action items, and providing contextual insights. This document outlines a simplified technical implementation for a standalone Python application using OpenAI APIs and Whisper.

## Core Features

1. **Real-time Speech Recognition**
   - Capture and transcribe spoken conversations during meetings using Whisper
   - Support for audio from system microphone or meeting platforms
   - Basic noise filtering

2. **Note Taking**
   - Automatic generation of meeting transcripts
   - Organization of content into structured notes via OpenAI GPT models

3. **Action Item Detection**
   - Identification of tasks and assignments via OpenAI API
   - Extraction of deadlines and responsible parties
   - Compilation of action items into a structured list

4. **Meeting Summarization**
   - Generation of concise meeting summaries using OpenAI GPT models
   - Identification of main topics and decisions
   - Highlighting of important insights

5. **Real-time Insights Engine** 
   - Continuous analysis of conversation to surface relevant information
   - Suggestion of talking points, facts, and contextual information
   - Discreet notification of opportunities to contribute valuable insights
   - Quick reference to key data points to help users sound more knowledgeable

6. **User Interaction**
   - Simple command interface for controlling the assistant during meetings
   - Export capabilities for notes, summaries, and action items
   - Discreet notifications for real-time insights

## Simplified Technical Architecture

### System Components

1. **Audio Capture Module**
   - Uses system microphone or meeting platform audio
   - Handles audio stream processing and buffering
   - Basic audio preprocessing

2. **Speech Recognition Engine**
   - Uses Whisper/OpenWhisper for real-time speech-to-text conversion
   - Optimized for meeting terminology
   - Processes audio in chunks for real-time transcription

3. **Text Processing Pipeline**
   - Uses OpenAI GPT models for all text analysis and generation
   - Single API interface for multiple language tasks
   - Configurable prompts for different analysis needs

4. **Insights Generator**
   - Monitors conversation flow to identify opportunities for input
   - Cross-references discussion with knowledge base and relevant facts
   - Generates contextually relevant suggestions and talking points
   - Prioritizes insights based on relevance and conversational timing

5. **User Interface**
   - Simple command-line interface
   - Text output for meeting insights
   - Non-intrusive notification system for real-time suggestions
   - Export capabilities for notes, summaries, and action items

### Data Flow

1. Meeting audio is captured through the system microphone
2. Speech is transcribed in real-time via Whisper
3. Transcribed text is sent to OpenAI API with appropriate prompts for:
   - Action item extraction
   - Summary generation
   - Context analysis
   - Real-time insight generation
4. Insights are immediately surfaced to the user through non-intrusive notifications
5. Results are formatted and displayed to the user
6. At the end of the meeting, a comprehensive summary with action items is generated

## Implementation Details

### Python Stack

1. **Core Components**
   - **Speech Recognition**: Whisper or OpenAI Whisper API
   - **Language Processing**: OpenAI GPT API
   - **Basic UI**: Command-line interface with rich text formatting
   - **Notification System**: Desktop notifications or subtle CLI indicators

2. **Key Dependencies**
   - Python 3.9+
   - OpenAI API (for both Whisper and GPT)
   - PyAudio (for audio capture)
   - Rich (for improved CLI formatting)
   - Plyer (for desktop notifications)

### Speech Recognition Implementation

```python
# Simplified implementation of speech recognition module
import pyaudio
import numpy as np
import whisper
import threading
from queue import Queue

class SpeechRecognizer:
    def __init__(self):
        self.audio_queue = Queue()
        self.model = whisper.Whisper.load_model("base")  # or use OpenAI API
        self.is_capturing = False
        self.transcription = []
        
    def start_capture(self):
        self.is_capturing = True
        threading.Thread(target=self._capture_audio).start()
        threading.Thread(target=self._process_audio).start()
        
    def _capture_audio(self):
        # Simple audio capture using PyAudio
        # Configured for optimal speech recognition
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=4000
        )
        
        while self.is_capturing:
            audio_chunk = stream.read(4000)
            self.audio_queue.put(audio_chunk)
        
    def _process_audio(self):
        # Process audio chunks in batches for efficient recognition
        buffer = []
        
        while self.is_capturing:
            if not self.audio_queue.empty():
                chunk = self.audio_queue.get()
                buffer.append(chunk)
                
                # Process when buffer reaches sufficient size
                if len(buffer) > 10:  # ~2.5 seconds of audio
                    audio_data = b''.join(buffer)
                    # Convert to format needed by Whisper
                    audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                    
                    # Get transcription from Whisper
                    result = self.model.transcribe(audio_np)
                    if result["text"].strip():
                        self.transcription.append(result["text"])
                        print(f"Transcribed: {result['text']}")
                    
                    # Reset buffer but keep a small overlap
                    buffer = buffer[-2:]
```

### OpenAI API Implementation

```python
# Simplified implementation using OpenAI API for all language processing
import openai
import json
from plyer import notification

class MeetingAssistant:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.meeting_transcript = []
        self.current_summary = ""
        self.action_items = []
        self.conversation_context = []
        self.last_insight_time = 0
        self.insight_cooldown = 30  # seconds between insights to avoid overwhelming
        
    def add_transcript(self, text_segment):
        self.meeting_transcript.append(text_segment)
        self.conversation_context.append(text_segment)
        # Keep conversation context to a manageable size
        if len(self.conversation_context) > 20:
            self.conversation_context = self.conversation_context[-20:]
        # Check for potential insights
        self._generate_real_time_insights()
        
    def update_summary(self):
        # Create a prompt for summarization
        recent_transcript = " ".join(self.meeting_transcript[-10:])  # Last 10 segments
        
        prompt = f"""
        Previous summary: {self.current_summary}
        
        New meeting transcript segment: 
        {recent_transcript}
        
        Please update the summary to incorporate this new information. 
        Focus on key points, decisions, and important discussion topics.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meetings."},
                {"role": "user", "content": prompt}
            ]
        )
        
        self.current_summary = response.choices[0].message.content
        return self.current_summary
    
    def extract_action_items(self):
        # Create a prompt for action item extraction
        full_transcript = " ".join(self.meeting_transcript)
        
        prompt = f"""
        Based on the following meeting transcript, identify all action items.
        For each action item, extract:
        1. The responsible person
        2. The specific task
        3. The deadline (if mentioned)
        4. Priority level (if indicated)
        
        Format the output as a JSON array.
        
        Meeting transcript:
        {full_transcript}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts action items from meeting transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            self.action_items = json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback if response isn't valid JSON
            self.action_items = [{"task": "Error parsing action items, please check transcript manually"}]
            
        return self.action_items
        
    def _generate_real_time_insights(self):
        import time
        current_time = time.time()
        
        # Check if enough time has passed since last insight
        if current_time - self.last_insight_time < self.insight_cooldown:
            return
            
        # Create a prompt for generating real-time insights
        recent_context = " ".join(self.conversation_context)
        
        prompt = f"""
        Based on the following recent meeting conversation, generate 1-2 highly relevant insights that would help the user contribute meaningfully.
        
        These insights should:
        1. Be directly relevant to the current topic
        2. Provide valuable information the user could mention
        3. Be concise and ready to use in conversation (under 100 words)
        4. Help the user sound more knowledgeable and prepared
        5. Not repeat information already mentioned
        
        Recent conversation:
        {recent_context}
        
        Format as a JSON object with "insights" array containing objects with "title" and "detail" fields.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that provides real-time conversational insights."},
                {"role": "user", "content": prompt}
            ]
        )
        
        try:
            insights = json.loads(response.choices[0].message.content)
            if insights and "insights" in insights and len(insights["insights"]) > 0:
                # Update last insight time
                self.last_insight_time = current_time
                # Display the insights to the user
                self._display_insights(insights["insights"])
        except (json.JSONDecodeError, KeyError):
            # Silently fail - insights are optional and shouldn't disrupt the meeting
            pass
            
    def _display_insights(self, insights):
        # Display insights via desktop notification
        for insight in insights:
            notification.notify(
                title=f"Meeting Insight: {insight['title']}",
                message=insight['detail'],
                timeout=10
            )
            
            # Also display in the console for CLI users
            print("\n")
            print("=" * 50)
            print(f"💡 INSIGHT: {insight['title']}")
            print(f"{insight['detail']}")
            print("=" * 50)
            print("\n")
```

## Deployment Architecture

### Simplified Standalone Script

The application will be packaged as a streamlined Python script with the following structure:

```
meeting_sidekick/
├── __main__.py                # Entry point
├── audio/                     # Audio capture and processing
│   └── recorder.py            # Contains SpeechRecognizer class
├── processing/                # OpenAI API integration
│   └── assistant.py           # Contains MeetingAssistant class
│   └── insights.py            # Real-time insight generation
├── ui/                        # Simple user interface
│   └── cli.py                 # Command-line interface
│   └── notifications.py       # Handles insight notifications
├── utils/                     # Utility functions
│   ├── config.py              # Configuration handling
│   └── export.py              # Export functionality
└── requirements.txt           # Dependencies
```

### Installation and Usage

```bash
# Installation
git clone https://github.com/username/meeting-sidekick.git
cd meeting-sidekick
pip install -r requirements.txt

# Usage (with your OpenAI API key)
python -m meeting_sidekick --api-key YOUR_API_KEY
```

## Privacy and Security Considerations

1. **Data Privacy**
   - API key securely stored in environment variables
   - Option to save transcripts locally
   - Clear disclosure about data sent to OpenAI API

2. **Security**
   - Basic encryption for local storage of meeting data
   - No persistent storage of complete transcripts unless explicitly requested

## Implementation Advantages

1. **Simplified Development**
   - Reduced number of dependencies
   - Single API interface for multiple language tasks
   - Faster development timeline

2. **Performance Benefits**
   - Offloading heavy processing to OpenAI's servers
   - Local processing limited to audio capture and basic management
   - Reduced local resource requirements

3. **Maintenance Advantages**
   - Simplified codebase with fewer components
   - Automatic improvements as OpenAI models are updated
   - Easier troubleshooting with fewer points of failure

4. **User Enhancement Benefits**
   - Real-time insights help users participate more effectively
   - Increases user's perceived knowledge and expertise during meetings
   - Provides contextual information without requiring extensive preparation

## Development Roadmap

1. **Phase 1: Core Functionality** (1-2 weeks)
   - Implement basic audio capture and Whisper transcription
   - Set up OpenAI API integration
   - Create simple command-line interface

2. **Phase 2: Feature Implementation** (2-3 weeks)
   - Implement real-time summarization
   - Add action item extraction
   - Create export functionality
   - Develop real-time insights engine

3. **Phase 3: Testing and Optimization** (1-2 weeks)
   - Test with real meetings
   - Optimize prompts for better results
   - Improve user interface and experience
   - Refine insight relevance and timing

4. **Future Enhancements** (As needed)
   - Add integration with meeting platforms
   - Implement basic web interface
   - Add customization options
   - Develop user knowledge profile to improve insight relevance 