from collections import namedtuple
import dateutil.parser

import unittest
from app import html_helper


class TestHTMLHelper(unittest.TestCase):

    def test_episode_html(self):
        """Test that episode_html generates expected list item html."""
        # TODO Expose the named tuple definition
        EpisodeData = namedtuple('EpisodeData', 'name link thumb date')

        e = EpisodeData("title", "link", "thumb", None)
        html = html_helper.episode_html(e)

        expected_html = "<li><a href=\"link\"><div class=\"block-container\">" +\
              "<div class=\"image-container\"><img src=\"thumb\"></div>" +\
              "</div><p class=\"name\">title</p></a></li>"

        self.assertEqual(html, expected_html)

if __name__ == '__main__':
    unittest.main()
