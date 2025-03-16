import openai
import json
import time
from datetime import datetime
from ..utils.export import export_to_file

class MeetingAssistant:
    def __init__(self, api_key):
        """
        Initialize the meeting assistant with OpenAI API key.
        
        Args:
            api_key (str): OpenAI API key
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.meeting_transcript = []
        self.current_summary = ""
        self.action_items = []
        self.conversation_context = []
        self.last_insight_time = 0
        self.insight_cooldown = 30  # seconds between insights
        self.meeting_title = f"Meeting {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.insight_callback = None
        
    def set_insight_callback(self, callback):
        """Set callback for when new insights are generated."""
        self.insight_callback = callback
        
    def set_meeting_title(self, title):
        """Set the title of the current meeting."""
        self.meeting_title = title
        
    def add_transcript(self, text_segment):
        """
        Add a new transcript segment and process it.
        
        Args:
            text_segment (str): New transcript segment
        """
        if not text_segment.strip():
            return
            
        self.meeting_transcript.append(text_segment)
        self.conversation_context.append(text_segment)
        
        # Keep conversation context to a manageable size
        if len(self.conversation_context) > 20:
            self.conversation_context = self.conversation_context[-20:]
            
        # Check for potential insights
        self._generate_real_time_insights()
        
    def update_summary(self):
        """Update the meeting summary with recent transcript segments."""
        # If there are no transcript segments, return empty string
        if not self.meeting_transcript:
            return ""
            
        # Create a prompt for summarization using recent segments
        recent_transcript = " ".join(self.meeting_transcript[-10:])
        
        prompt = f"""
        Previous summary: {self.current_summary}
        
        New meeting transcript segment: 
        {recent_transcript}
        
        Please update the summary to incorporate this new information. 
        Focus on key points, decisions, and important discussion topics.
        Keep the summary concise but comprehensive.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes meetings."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            self.current_summary = response.choices[0].message.content
            return self.current_summary
        except Exception as e:
            print(f"Error updating summary: {e}")
            return self.current_summary or "Unable to generate summary at this time."
    
    def extract_action_items(self):
        """Extract action items from the meeting transcript."""
        # If there are no transcript segments, return empty list
        if not self.meeting_transcript:
            return []
            
        # Create a prompt for action item extraction
        full_transcript = " ".join(self.meeting_transcript)
        
        prompt = f"""
        Based on the following meeting transcript, identify all action items.
        For each action item, extract:
        1. The responsible person
        2. The specific task
        3. The deadline (if mentioned)
        4. Priority level (if indicated)
        
        Format the output as a JSON array of objects with the following structure:
        [
            {{"person": "Name", "task": "Task description", "deadline": "Deadline or null", "priority": "Priority or null"}}
        ]
        
        Meeting transcript:
        {full_transcript}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts action items from meeting transcripts."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                # Find JSON array in the response if it's not pure JSON
                if content.strip().startswith('[') and content.strip().endswith(']'):
                    self.action_items = json.loads(content)
                else:
                    # Try to extract JSON from text
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        self.action_items = json.loads(json_str)
                    else:
                        raise ValueError("No JSON array found in response")
            except json.JSONDecodeError:
                # Fallback if response isn't valid JSON
                self.action_items = [{"task": "Error parsing action items, please check transcript manually"}]
                
            return self.action_items
        except Exception as e:
            print(f"Error extracting action items: {e}")
            return [{"task": "Error extracting action items, please try again later"}]
        
    def get_full_transcript(self):
        """Get the complete meeting transcript."""
        return "\n".join(self.meeting_transcript)
        
    def _generate_real_time_insights(self):
        """Generate real-time insights from the conversation context."""
        current_time = time.time()
        
        # Check if enough time has passed since last insight
        if current_time - self.last_insight_time < self.insight_cooldown:
            return
            
        if len(self.conversation_context) < 3:
            return  # Not enough context yet
            
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
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that provides real-time conversational insights."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content
            
            # Try to parse the JSON response
            try:
                # Find JSON object in the response if it's not pure JSON
                if content.strip().startswith('{') and content.strip().endswith('}'):
                    insights_data = json.loads(content)
                else:
                    # Try to extract JSON from text
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx >= 0 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        insights_data = json.loads(json_str)
                    else:
                        raise ValueError("No JSON object found in response")
                
                if insights_data and "insights" in insights_data and len(insights_data["insights"]) > 0:
                    # Update last insight time
                    self.last_insight_time = current_time
                    
                    # Call the insight callback if set
                    if self.insight_callback:
                        self.insight_callback(insights_data["insights"])
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing insights: {e}")
                # Silently fail - insights are optional and shouldn't disrupt the meeting
                pass
        except Exception as e:
            print(f"Error generating insights: {e}")
            
    def export_meeting_data(self, output_format="markdown"):
        """
        Export all meeting data to a file.
        
        Args:
            output_format (str): Format to export (markdown or json)
            
        Returns:
            str: Path to the exported file
        """
        meeting_data = {
            "title": self.meeting_title,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": self.current_summary,
            "action_items": self.action_items,
            "transcript": self.get_full_transcript()
        }
        
        return export_to_file(meeting_data, output_format)
