"""Flask routes specification."""
from app import api
from app import app
from app import html_helper

from flask import request
import operator


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/rt-recently-added', methods=['GET', 'POST'])
def rt_recently_added():
    """Produce the recently added page.

    First return a form to select which channels should be populated.
    Then return a recently added grid page displaying episodes.
    """
    channels = api.get_channels()
    if request.method == 'GET':
        return html_helper.channel_form(channels)

    if request.method == 'POST':
        selected_channels = request.form.getlist('channel')
        eps_requested = request.form.get('episodes')
        pages_requested = request.form.get('pages')

        all_eps = []

        for channel in selected_channels:
            episodes = api.get_episode_pages(channel,
                                             channels[channel],
                                             pages_requested,
                                             eps_requested)

            all_eps.extend(episodes)

        episodes_html = []
        all_eps.sort(key=operator.itemgetter(3), reverse=True)
        for e in all_eps:
            episodes_html.append(html_helper.episode_html(e))
        ra_html = html_helper.recently_added_html(episodes_html)

        return ra_html
