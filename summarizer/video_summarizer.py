from youtube_transcript_api import YouTubeTranscriptApi
import re

def get_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(pattern, url)
    return match.group(1) if match else None

def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t['text'] for t in transcript_list])
