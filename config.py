import os
import re

home_path = os.path.expanduser("~")
search_terms_file = "./search_terms.txt"
downloaded_file = "./downloaded.txt"

svt_video_base_url = 'https://svtplay.se'

# Scraping
svt_all_shows_page = f'{svt_video_base_url}/program'
video_url_on_page = r'\"svtplay\":\"(\/video.+?)\"'

#
svt_video_url_pattern = re.compile('/video/([0-9]+)/(.+)/(.+)')
