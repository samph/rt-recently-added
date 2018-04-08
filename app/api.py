"""API Helper functions."""

from collections import namedtuple
from datetime import datetime
import dateutil.parser
import json
import pytz
import requests

DOMAIN = "https://roosterteeth.com"
YOUTUBE_API_KEY = "..."

def api_call(url, domain="https://svod-be.roosterteeth.com"):
    """Make an API call."""
    result = None
    reply = requests.get(domain+url)

    if reply.status_code == 200:
        result = reply.json()
    return result

def get_youtube_videos(channel_playlist, videos="50"):
    domain = "https://www.googleapis.com/youtube"
    url = "/v3/playlistItems?part=snippet&playlistId="+\
            channel_playlist+"&maxResults=" + videos +\
             "&key="+YOUTUBE_API_KEY
    res = api_call(url, domain)

    items = res['items']

    videos = {}

    youtube_watch = "https://www.youtube.com/watch?v="

    for i in items:
        snippet = i['snippet']
        title = snippet['title']
        videoId = snippet['resourceId']['videoId']
        videos[title] = youtube_watch+videoId

    return videos


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


def _sponsor_notation(sponsors_only, pub_at):
    notation = ""
    if sponsors_only:
        notation =  "(***) "
    else:
        now = datetime.now(pytz.utc)
        vid_pub = dateutil.parser.parse(pub_at)
        if vid_pub > now:
            notation = "(*) "
    return notation


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
        EpisodeData = namedtuple('EpisodeData', 'name title link thumb date sponsor')
        for ep in eps_data:
            length = ep['attributes']['length']
            timestamp = _timestamp_string(length)
            sponsor_only = ep['attributes']['is_sponsors_only']
            pub_at = ep['attributes']['member_golive_at']
            name = _sponsor_notation(sponsor_only, pub_at) + \
                     ep['attributes']['show_title'] + \
                     " - " + ep['attributes']['title'] + " " + timestamp
            title = ep['attributes']['title']
            link = DOMAIN + ep['canonical_links']['self']
            thumb = ep['included']['images'][0]['attributes']['small']
            live_at = ep['attributes']['sponsor_golive_at']
            episodes.append(EpisodeData(name,
                                        title,
                                        link,
                                        thumb,
                                        dateutil.parser.parse(live_at),
                                        sponsor_only))

        return episodes
