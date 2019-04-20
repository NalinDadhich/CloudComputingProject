import requests
from threading import Thread, Event

class ExtractYouTube(thread):
    Comment_Url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    Search_Url = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(self, total_count, query, key, call, interval=5):
        self.stop_event = Event()
        Thread.__init__(self)
        self.key = key
        self.query = query
        self.total_count = 50 if total_count > 50 else total_count
        self.callback = call
        self.interval = interval
        self.videos_ids = None
        self.last_comment_per_video = None