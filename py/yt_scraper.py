import datetime as dt
from typing import Optional
from youtube_search import YoutubeSearch


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


if __name__ == '__main__':
    dln_scraper = DavidLynchNumberScraper()
