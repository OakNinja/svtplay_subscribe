import re
import requests
from bs4 import BeautifulSoup

import svtplay_dl
from svtplay_dl import setup_defaults as svtplay_options

import config


class SvtPlaySubscriber:

    def __init__(self):
        self.options = svtplay_options()
        self.options.subtitle = True
        self.options.verbose = True
        self.options.stream_prio = "hds"
        self.options.quality = 2793
        self.options.flexibleq = 100
        self.config = config

    def load_search_terms_from_search_terms_file(self):
        with open(self.config.search_terms_file) as f:
            return f.read().splitlines()

    def get_episodes_matching_search_terms(self):
        svt_program_page = requests.get(self.config.svt_all_shows_page).text
        soup = BeautifulSoup(svt_program_page, 'html.parser')
        shows = soup.find_all('a', {'class': 'play_link-list__link'})
        matched_shows = []

        for show in shows:
            for word in self.load_search_terms_from_search_terms_file():
                if word in show.text.lower():
                    matched_shows.append(f'{self.config.svt_video_base_url}{show.attrs["href"]}')
        matching_episodes = []
        for show in matched_shows:
            raw = requests.get(show, 'html.parser').text
            js_data = set(re.findall(self.config.video_url_on_page, raw))

            for episode_relative_url in js_data:
                url_match = self.config.svt_video_url_pattern.match(episode_relative_url)
                if url_match:
                    matching_episodes.append(episode_relative_url)
        return matching_episodes

    def get_downloaded_episodes(self):
        try:
            with open(self.config.downloaded_file) as f:
                return f.read().splitlines()
        except FileNotFoundError:
            return []

    def download(self):
        episodes = self.get_episodes_matching_search_terms()
        downloaded_episodes = self.get_downloaded_episodes()
        episodes = [episode for episode in episodes if episode not in downloaded_episodes]
        for episode in sorted(episodes):
            try:
                svtplay_dl.get_media(f'{self.config.svt_video_base_url}{episode}', self.options)
            except KeyboardInterrupt:
                exit(1)
            except:
                print('ERROR!!!!111one')
            with open(self.config.downloaded_file, 'a') as f:
                f.write(f'{episode}' + '\n')
                
                
if __name__ == '__main__':
    SvtPlaySubscriber().download()
