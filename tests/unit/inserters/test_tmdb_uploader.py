import os
from unittest import TestCase
from unittest.mock import patch

from RatS.inserters.tmdb_uploader import TMDBUploader

TESTDATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, 'assets'))


class TMDBUploaderTest(TestCase):
    def setUp(self):
        self.movie = dict()
        self.movie['title'] = 'Fight Club'
        self.movie['imdb'] = dict()
        self.movie['imdb']['id'] = 'tt0137523'
        self.movie['imdb']['url'] = 'http://www.imdb.com/title/tt0137523'
        self.movie['imdb']['my_rating'] = 9

    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_init(self, browser_mock, base_init_mock):
        TMDBUploader()

        self.assertTrue(base_init_mock.called)

    @patch('RatS.inserters.tmdb_uploader.save_movies_to_csv')
    @patch('RatS.inserters.tmdb_uploader.TMDB')
    @patch('RatS.inserters.base_inserter.Inserter.__init__')
    @patch('RatS.sites.base_site.Firefox')
    def test_insert(self, browser_mock, base_init_mock, site_mock, impex_mock):  # pylint: disable=too-many-arguments
        site_mock.browser = browser_mock
        inserter = TMDBUploader()
        inserter.site = site_mock
        inserter.site.site_name = 'trakt'
        inserter.failed_movies = []
        inserter.exports_folder = TESTDATA_PATH

        inserter.insert([self.movie], 'imdb')

        self.assertTrue(base_init_mock.called)
        self.assertTrue(impex_mock.called)
