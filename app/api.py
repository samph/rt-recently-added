"""API Helper functions."""

from collections import namedtuple
import dateutil.parser
import json
import requests

DOMAIN = "https://roosterteeth.com"


def api_call(url, domain="https://svod-be.roosterteeth.com"):
    """Make an API call."""
    result = None
    reply = requests.get(domain+url)
    if reply.status_code == 200:
        result = reply.json()
    return result


def get_channels():
    """Get a list of RT channels and their API URLs."""
    channel_reply = api_call('/api/v1/channels')
    channel_data = channel_reply['data']
    channels = dict()
    for channel in channel_data:
        name = channel['attributes']['name']
        eps_api_url = channel['links']['episodes']
        channels[name] = eps_api_url

    return channels


def get_episode_pages(channel_name,
                      channel_eps_api_url,
                      pages="1",
                      episode_count="20"):
    """Retrieve episodes for the given amount of pages and items per page."""
    try:
        i = int(pages)
    except ValueError:
        i = 1

    episodes = []
    for x in range(i):
        episodes.extend(get_episodes(channel_name,
                                     channel_eps_api_url,
                                     str(x+1),
                                     episode_count))

    return episodes


def _timestamp_string(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h > 0:
        timestamp = ("(%d:%02d:%02d)" % (h, m, s))
    else:
        timestamp = ("(%d:%02d)" % (m, s))
    return timestamp


def get_episodes(channel_name,
                 channel_eps_api_url,
                 page="1",
                 episode_count="20"):
        """Get a page of episodes."""
        url = channel_eps_api_url +\
            "?page={0}&per_page={1}".format(page, episode_count)

        eps_reply = api_call(url)
        eps_data = eps_reply['data']
        episodes = []
        EpisodeData = namedtuple('EpisodeData', 'name link thumb date')
        for ep in eps_data:
            length = ep['attributes']['length']
            timestamp = _timestamp_string(length)
            title = ep['attributes']['show_title'] + \
                     " - " + ep['attributes']['title'] + " " + timestamp
            link = DOMAIN + ep['canonical_links']['self']
            thumb = ep['included']['images'][0]['attributes']['small']
            live_at = ep['attributes']['sponsor_golive_at']
            episodes.append(EpisodeData(title,
                                        link,
                                        thumb,
                                        dateutil.parser.parse(live_at)))

        return episodes
