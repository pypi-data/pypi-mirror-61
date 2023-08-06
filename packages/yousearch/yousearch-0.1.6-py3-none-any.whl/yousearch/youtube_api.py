import urllib.parse
import urllib.request
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from yousearch import config
import os


def extract_vid(url):
    """Extracts the video id from a Youtube URL
    """
    try:
        url_data = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(url_data.query)
        return query['v'][0]
    except KeyError:
        return


def get_transcript(vid, lang=["en"]):
    """Returns a transcript for a specific Video ID

    Takes a video ID and returns its Trascript in
    the following format:
    [{
        'text': 'Hey there',
        'start': 7.58,
        'duration': 6.13
    }]
    For further information:
    https://github.com/jdepoix/youtube-transcript-api

    :vid: video id
    :lang: List of languages, sorted by priority. If one
           is not available, the next one is fetched.

    TODO: Error handling
    """
    try:
        return YouTubeTranscriptApi.get_transcript(vid, languages=lang)
    except:
        return


def get_video_title(url):
    """Returns the title of the website
    """
    resp = urllib.request.urlopen(url).read()
    parsed_response = BeautifulSoup(resp, features="html.parser")
    return parsed_response.head.find('title').text


class Video:
    def __init__(self, url):
        self.url = url
        self.vid = extract_vid(self.url)
        self.transcript_dict = None
        self.transcript = None
        self.title = None

    def fetch_transcript(self):
        self.transcript_dict = get_transcript(self.vid)
        if self.transcript_dict is None:
            return
        self.transcript = ' '.join([i['text'] for i in self.transcript_dict])
        self.title = get_video_title(self.url)

    def export_transcript(self, path=config.TRANSCRIPT_PATH, file_format=None):
        """Export transcript to a file
        """
        f = open(os.path.join(path, self.title), 'w+')
        f.write(self.transcript)
        return

    def search_string(self, word):
        """Very simple search procedure.
        """
        results = [i for i in self.transcript_dict if
                   word.lower() in i["text"].lower()]
        [result.update({"title": self.title}) for result in results]
        return results
