import requests
from threading import Thread, Event


class ExtractYouTube(Thread):
    Comment_Url = 'https://www.googleapis.com/youtube/v3/commentThreads'
    Search_Url = 'https://www.googleapis.com/youtube/v3/search'

    def __init__(self, total_count, query, key, call, rcode=None, interval=5):
        self.stop_event = Event()
        Thread.__init__(self)
        self.key = key
        self.query = query
        self.total_count = 50 if total_count > 50 else total_count
        self.callback = call
        self.rcode = rcode
        self.interval = interval
        self.video_ids = None
        self.last_comment_per_video = None

    def get_all_vids(self):
        params = {
            'key': self.key,
            'part': 'snippet',
            'maxResults': self.total_count,
            'order': 'date',
            'type': 'video',
            'q': self.query
        }

        if self.rcode is not None:
            params['regionCode'] = self.rcode

        extracted_jsons = requests.get(self.Search_Url, params).json()
        # print(extracted_jsons)

        if not extracted_jsons['items']:
            raise ValueError(extracted_jsons)

        self.last_comment_per_video = {}
        self.video_ids = []

        for json in extracted_jsons['items']:
            self.video_ids.append(json['id']['videoId'])
            self.last_comment_per_video[json['id']['videoId']] = []

    def get_all_comments(self, v_id, page_token = None):
        params = {
            'key' : self.key,
            'part': 'snippet',
            'maxResults': 100,
            'order': 'time',
            'textFormat': 'plainText'
        }

        if page_token is not None:
            params['pageToken'] = page_token

        params['videoId'] = v_id

        json = requests.get(self.Comment_Url, params).json()

        if 'items' not in json or len(json['items']) == 0:
            return None

        for element in json['items']:
            comment_id = element['id']

            if len(self.last_comment_per_video[v_id]) > 0 and comment_id == \
                    self.last_comment_per_video[v_id][0]:
                break

            if comment_id in self.last_comment_per_video[v_id]:
                continue

            comment = element['snippet']['topLevelComment']['snippet'][
                'textOriginal']
            self.callback(v_id, comment)
            self.last_comment_per_video[v_id].append(comment_id)

        return json

    def get_new_comments(self):
        for v_id in self.video_ids:
            json = self.get_all_comments(v_id)

    def run(self):

        if self.video_ids is None:
            raise ValueError('No video ids available, call fetch_videos first.')

        for v_id in self.video_ids:
            json = self.get_all_comments(v_id)

            if json is None:
                self.last_comment_per_video[v_id] = []
                print('{} has no comments.'.format(v_id))
                continue

            while 'nextPageToken' in json:
                json = self.get_all_comments(v_id, json[
                    'nextPageToken'])

        print('Started monitoring')
        while not self.stop_event.wait(self.interval):
            self.get_new_comments()

    def stop(self):
        """
        Sets the stop_event
        """
        self.stop_event.set()