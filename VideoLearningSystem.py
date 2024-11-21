from typing import List, Dict, Set
import json
import logging
from pathlib import Path

from analyzer import analyze
from chatgpt import generate_quiz

class VideoLearningSystem:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_name = Path(video_path).name
        self.transcript = None
        self.summary = None
        self.pause_points = set()
        self.quiz = None
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def process_video(self):
        """Main workflow to process a video"""
        self._generate_transcript()
        self._generate_summary()
        self._extract_pause_points()
        self._generate_quiz()
        return self.get_video_config()
    
    def _generate_transcript(self):
        """Generate transcript using the analyzer"""
        try:
            self.transcript = analyze(self.video_name)
            self._save_transcript()
        except Exception as e:
            self.logger.error(f"Failed to generate transcript: {str(e)}")
            raise
    
    def _save_transcript(self):
        """Save transcript to file"""
        transcript_path = f"transcripts/{Path(self.video_name).stem}_transcript.txt"
        Path("transcripts").mkdir(exist_ok=True)
        with open(transcript_path, 'w') as f:
            f.write(self.transcript)
        self.transcript_path = transcript_path
    
    def _generate_summary(self):
        """Generate summary using ChatGPT"""
        from chatgpt import generateSummary
        try:
            self.summary = generateSummary(self.transcript_path)
            self._save_summary()
        except Exception as e:
            self.logger.error(f"Failed to generate summary: {str(e)}")
            raise
    
    def _save_summary(self):
        """Save summary to file"""
        summary_path = f"summaries/{Path(self.video_name).stem}_summary.txt"
        Path("summaries").mkdir(exist_ok=True)
        with open(summary_path, 'w') as f:
            f.write(self.summary)
    
    def _extract_pause_points(self):
        """Extract timestamps from summary to use as pause points"""
        import re
        
        # Look for timestamps in the format [MM:SS] or MM:SS
        timestamp_pattern = r'(?:\[)?(\d{1,2}:\d{2})(?:\])?'
        
        timestamps = re.findall(timestamp_pattern, self.summary)
        
        for timestamp in timestamps:
            minutes, seconds = map(int, timestamp.split(':'))
            total_seconds = minutes * 60 + seconds
            self.pause_points.add(total_seconds)
    
    def _generate_quiz(self):
        """Generate quiz questions based on the summary"""
        try:
            self.quiz = generate_quiz(self.summary)
            self._save_quiz()
        except Exception as e:
            self.logger.error(f"Failed to generate quiz: {str(e)}")
            raise
    
    def _save_quiz(self):
        """Save quiz to file"""
        quiz_path = f"quizzes/{Path(self.video_name).stem}_quiz.json"
        Path("quizzes").mkdir(exist_ok=True)
        with open(quiz_path, 'w') as f:
            json.dump(self.quiz, f, indent=2)
    
    def get_video_config(self) -> Dict:
        """Get configuration for video player"""
        return {
            "video_path": self.video_path,
            "pause_points": list(self.pause_points),
            "transcript_path": self.transcript_path,
            "summary": self.summary,
            "quiz": self.quiz
        }

    def play_video(self):
        """Play video with automatic pausing at key points"""
        import Video

        # Update the pause_times in Video.py
        Video.pause_times = self.pause_points
        
        # Start video playback
        Video.play_video(self.video_path)


# Initialize the system with a video
learning_system = VideoLearningSystem("data/Video.mp4")

# Process the video (generates transcript, summary, and quiz)
config = learning_system.process_video()

# Play the video with automatic pausing
learning_system.play_video()