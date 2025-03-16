import pyaudio
import numpy as np
import whisper
import threading
from queue import Queue
import time

class SpeechRecognizer:
    def __init__(self, model_name="base"):
        """
        Initialize the speech recognizer with a Whisper model.
        
        Args:
            model_name (str): Whisper model name. Defaults to "base".
        """
        self.audio_queue = Queue()
        self.model = whisper.load_model(model_name)
        self.is_capturing = False
        self.transcription = []
        self.new_transcription_callback = None
        
    def set_transcription_callback(self, callback):
        """
        Set a callback function that will be called with new transcription segments.
        
        Args:
            callback (callable): A function that accepts a string parameter.
        """
        self.new_transcription_callback = callback
        
    def start_capture(self):
        """Start capturing and processing audio in separate threads."""
        if self.is_capturing:
            return
            
        self.is_capturing = True
        self.capture_thread = threading.Thread(target=self._capture_audio)
        self.process_thread = threading.Thread(target=self._process_audio)
        
        self.capture_thread.daemon = True
        self.process_thread.daemon = True
        
        self.capture_thread.start()
        self.process_thread.start()
        
    def stop_capture(self):
        """Stop capturing and processing audio."""
        self.is_capturing = False
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join(timeout=1.0)
        if hasattr(self, 'process_thread'):
            self.process_thread.join(timeout=1.0)
        
    def _capture_audio(self):
        """Capture audio from the microphone and add to the queue."""
        # Set up audio capture with PyAudio
        p = pyaudio.PyAudio()
        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4000
            )
            
            while self.is_capturing:
                try:
                    audio_chunk = stream.read(4000)
                    self.audio_queue.put(audio_chunk)
                except Exception as e:
                    print(f"Error reading audio: {e}")
                    time.sleep(0.1)
        finally:
            try:
                stream.stop_stream()
                stream.close()
            except:
                pass
            p.terminate()
        
    def _process_audio(self):
        """Process audio chunks for speech recognition using Whisper."""
        buffer = []
        silence_threshold = 0.01  # Adjust based on your environment
        
        while self.is_capturing:
            try:
                if not self.audio_queue.empty():
                    chunk = self.audio_queue.get(timeout=1.0)
                    buffer.append(chunk)
                    
                    # Process when buffer reaches sufficient size (about 2.5 seconds)
                    if len(buffer) > 10:
                        audio_data = b''.join(buffer)
                        
                        # Convert to format needed by Whisper
                        audio_np = np.frombuffer(audio_data, np.int16).astype(np.float32) / 32768.0
                        
                        # Check if there's actual speech (not just silence)
                        if np.abs(audio_np).mean() > silence_threshold:
                            # Get transcription from Whisper
                            result = self.model.transcribe(audio_np)
                            text = result["text"].strip()
                            
                            if text:
                                self.transcription.append(text)
                                
                                # Call the callback if set
                                if self.new_transcription_callback:
                                    self.new_transcription_callback(text)
                        
                        # Reset buffer but keep a small overlap for context
                        buffer = buffer[-2:]
                else:
                    time.sleep(0.1)
            except Exception as e:
                print(f"Error processing audio: {e}")
                time.sleep(0.1)
                
    def get_full_transcript(self):
        """Get the complete transcript as a string."""
        return " ".join(self.transcription)
