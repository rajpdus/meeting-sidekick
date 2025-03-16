#!/usr/bin/env python3
"""
Simple test script for Meeting Sidekick recording functionality.
"""

import time
import unittest
from meeting_sidekick.audio.recorder import SpeechRecognizer

class TestMeetingSidekickRecording(unittest.TestCase):
    def setUp(self):
        # Initialize the speech recognizer with the smallest model for faster testing
        self.recognizer = SpeechRecognizer(model_name="tiny")
        self.transcription_results = []
        
    def transcription_callback(self, text):
        """Callback function to collect transcription results"""
        print(f"Transcribed: {text}")
        self.transcription_results.append(text)
        
    def test_recording(self):
        """Test basic recording functionality"""
        # Set up the callback
        self.recognizer.set_transcription_callback(self.transcription_callback)
        
        # Start recording
        print("Starting recording for 10 seconds. Please speak clearly...")
        self.recognizer.start_capture()
        
        # Record for 10 seconds
        time.sleep(10)
        
        # Stop recording
        self.recognizer.stop_capture()
        print("Recording stopped.")
        
        # Get the full transcript
        full_transcript = self.recognizer.get_full_transcript()
        print(f"\nFull transcript: {full_transcript}")
        
        # Check if any transcription was captured
        self.assertTrue(len(self.transcription_results) > 0 or full_transcript.strip() != "", 
                        "No transcription was captured. Make sure your microphone is working.")

def manual_test():
    """Run a manual test without unittest framework"""
    print("Initializing speech recognizer...")
    recognizer = SpeechRecognizer(model_name="tiny")
    
    def on_transcription(text):
        print(f"Transcribed: {text}")
    
    recognizer.set_transcription_callback(on_transcription)
    
    print("\nStarting recording for 10 seconds. Please speak clearly...")
    recognizer.start_capture()
    
    # Record for 10 seconds
    for i in range(10, 0, -1):
        print(f"Recording... {i} seconds remaining")
        time.sleep(1)
    
    # Stop recording
    recognizer.stop_capture()
    print("Recording stopped.")
    
    # Get the full transcript
    full_transcript = recognizer.get_full_transcript()
    print(f"\nFull transcript: {full_transcript}")
    
    if full_transcript.strip() == "":
        print("WARNING: No transcription was captured. Make sure your microphone is working.")
    else:
        print("Test successful! Transcription was captured.")

if __name__ == "__main__":
    # Choose between unittest or manual test
    use_unittest = False
    
    if use_unittest:
        unittest.main()
    else:
        manual_test() 