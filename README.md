# Meeting Sidekick

Meeting Sidekick is a powerful AI-powered virtual assistant designed to enhance your meeting experiences by automating note-taking, summarizing discussions, tracking action items, and providing contextual insights in real-time.

## Features

- **Real-time Speech Recognition**: Automatically captures and transcribes spoken conversations during meetings using OpenAI Whisper
- **Smart Note Taking**: Organizes content into structured notes via OpenAI GPT models
- **Action Item Detection**: Identifies tasks, assignments, deadlines, and responsible parties
- **Meeting Summarization**: Generates concise summaries highlighting main topics and decisions
- **Real-time Insights Engine**: Analyzes conversations to provide relevant information and talking points
- **Beautiful CLI Interface**: Rich, interactive terminal interface with color-coded sections and real-time updates

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/meeting-sidekick.git
   cd meeting-sidekick
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your OpenAI API key:
   ```bash
   # Option 1: Use the setup command
   python -m meeting_sidekick setup
   
   # Option 2: Set as environment variable
   export OPENAI_API_KEY=your_api_key_here
   
   # Option 3: Pass directly when running
   python -m meeting_sidekick run --api-key your_api_key_here
   ```

## Usage

Start the Meeting Sidekick:
```bash
python -m meeting_sidekick run
```

### Commands

Once the Meeting Sidekick is running, you can use the following keyboard commands:

- `r`: Start/stop recording
- `s`: Force update summary
- `a`: Force update action items
- `e`: Export meeting data (markdown or JSON)
- `t`: Set meeting title
- `h`: Show help
- `q`: Quit

## Interface Layout

The Meeting Sidekick interface is divided into four main sections:

1. **Live Transcript**: Shows the real-time transcription of the meeting
2. **Meeting Summary**: Displays an automatically generated and continuously updated summary
3. **Insights**: Shows contextual insights that you can use during the conversation
4. **Action Items**: Lists detected action items with assignments and deadlines

## Configuration

You can configure Meeting Sidekick using environment variables or the built-in setup command:

```bash
python -m meeting_sidekick setup
```

Configuration options include:
- OpenAI API key
- Whisper model selection (tiny, base, small, medium, large)
- Desktop notifications toggle
- Update intervals for summary and action items

## Export Formats

Meeting Sidekick supports exporting meeting data in the following formats:

- **Markdown**: Structured document with summary, action items, and full transcript
- **JSON**: Machine-readable format for integration with other tools

## Requirements

- Python 3.9+
- OpenAI API key
- Audio input device (microphone)

## Privacy and Data Handling

- All processing happens via OpenAI's API
- Transcripts and meeting data are saved locally only when explicitly exported
- No data is stored or retained by default

## Project Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md): Detailed explanation of the application architecture, components, and design decisions
- [CONTRIBUTING.md](CONTRIBUTING.md): Guidelines for contributing to the project

## License

Meeting Sidekick is released under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute to this project.
