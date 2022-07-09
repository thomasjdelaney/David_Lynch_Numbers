import json
import requests
import datetime as dt
from youtube_search import YoutubeSearch
from typing import Optional


def find_value(html: str, key: str, num_sep_chars: int = 2, separator: str = '"'):
    """For getting the value for the given key from the given html request.
    Arguments:
        html: the request text
        key: the key for which we want the value
        num_sep_chars: number of characters in the separating string
        separator: the character"""
    start_pos = html.find(key) + len(key) + num_sep_chars
    end_pos = html.find(separator, start_pos)
    return html[start_pos:end_pos]


class DavidLynchNumberScraper:
    """A class for attempting to scrape the latest set of David Lynch Numbers from YouTube."""

    def __init__(self) -> None:
        """For initialising the object"""
        self.most_recent_url: Optional[str] = None
        self.set_most_recent_video_url()

    def set_most_recent_video_url(self) -> None:
        """For setting the most_recent_url attribute."""
        today_str = dt.datetime.today().date().strftime('%-m/%d/%y')
        yesterday_str = (dt.datetime.today() + dt.timedelta(days=-1)).strftime('%-m/%d/%y')
        today_query = f"David Lynch's Weather Report {today_str}"
        yesterday_query = f"David Lynch's Weather Report {yesterday_str}"
        results = YoutubeSearch(today_query, max_results=1).to_dict()
        if not len(results):
            results = YoutubeSearch(yesterday_query, max_results=1).to_dict()
        for result in results:
            url = f"https://youtube.com{result['url_suffix']}"
            title = result['title']
            print(f"{title}: {url}")
            self.most_recent_url = url

    def get_comments(self):
        session = requests.Session()
        res = session.get(self.most_recent_url)
        xsrf_token = find_value(res.text, "XSRF_TOKEN", num_sep_chars=3)
        # parse the YouTube initial data in the <script> tag
        data_str = find_value(res.text, 'window["ytInitialData"] = ', num_sep_chars=0, separator="\n").rstrip(";")
        # convert to Python dictionary instead of plain text string
        data = json.loads(data_str)


if __name__ == '__main__':
    dln_scraper = DavidLynchNumberScraper()
