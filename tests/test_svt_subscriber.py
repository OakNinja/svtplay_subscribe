import os

from svt_scraper import SvtPlaySubscriber


def test_load_search_terms_file():
    subscriber = SvtPlaySubscriber()
    subscriber.config.search_terms_file = 'search_terms.txt'
    if os.path.exists(subscriber.config.search_terms_file):
        os.remove(subscriber.config.search_terms_file)
    with open(subscriber.config.search_terms_file, 'a+') as f:
        f.writelines(['test\n', 'test2\n'])
    assert subscriber.load_search_terms_from_search_terms_file() == ['test', 'test2']
