import os
import svtplay_dl
import re
import feedparser

__author__ = 'oakninja'


class Subscriber:

    def __init__(self):
        self.home = os.path.expanduser("~")
        self.url_pattern = re.compile('http://www.svtplay.se/video/([0-9]+)/(.+)/(.+)')

        self.create_file('svt_downloaded')
        self.create_file('svt_keywords')

    def create_file(self, file_name):
        path = self.home + '/' + file_name
        if not os.path.isfile(path):
            open(path, 'w').close()

    def read_file(self, file_name):
        path = self.home + '/' + file_name
        with open(path) as f:
            content = f.readlines()
            f.close()
        return content

    @staticmethod
    def find(keywords, text):
        for keyword in keywords:
            cleaned_keyword = keyword.strip(' \t\n\r').lower()
            if len(cleaned_keyword) > 1 and cleaned_keyword in text.lower():
                return True
        return False

    def is_new(self, downloaded, link):
        parsed_url = self.url_pattern.search(link)
        video_id = parsed_url.group(1)
        already_downloaded = self.find(downloaded, video_id)
        if video_id and not already_downloaded:
            return True
        return False

    def find_new_downloads(self, feed, keywords, downloaded):
        new_downloads = []
        for entry in feed.entries:
            if self.find(keywords, entry.title) and self.is_new(downloaded, entry.link):
                new_downloads.append(entry)
        return new_downloads

    def download_new_streams(self, new_downloads):
        downloaded = []
        options = svtplay_dl.Options()
        options.subtitle = True
        options.verbose = False
        options.stream_prio = "hds"
        options.quality = 2793
        options.flexibleq = 100
        for item in new_downloads:
            parsed_url = self.url_pattern.search(item.link)
            title = "{}-{}".format(parsed_url.group(2), parsed_url.group(3))
            options.output = self.home + '/Movies/' + title + '.mp4'
            print("\nDownloading item {}".format(title))
            svtplay_dl.get_media(item.link, options)
            stream_id = self.url_pattern.search(item.link)
            if stream_id:
                downloaded.append({"id": stream_id.group(1), "title": title})
        f = open(self.home + '/' + 'svt_downloaded', 'a+')
        for item in downloaded:
            print>>f, item["title"]
            print('\nDownloaded ' + item["id"])
        f.close()

    def run(self):
        downloaded = self.read_file('svt_downloaded')
        keywords = self.read_file('svt_keywords')
        print('Looking for ...')
        print(keywords)
        feed = feedparser.parse('http://www.svtplay.se/rss.xml')

        new_downloads = self.find_new_downloads(feed, keywords, downloaded)

        self.download_new_streams(new_downloads)


subscriber = Subscriber()
subscriber.run()
