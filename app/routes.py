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
    rt_channels_to_youtube = {}
    #RT, RVB
    rt_channels_to_youtube['Rooster Teeth'] = ['UUzH3iADRIq1IJlIXjfNgTpA', 'UUII0hP2Ycmhh5j8lS4cexBQ']
    #AH, LP
    rt_channels_to_youtube['Achievement Hunter'] = ['UUsB0LwkHPWyjfZ-JwvtwEXw', 'UUkxctb0jr8vwa4Do6c6su0Q']
    rt_channels_to_youtube['Funhaus'] = ['UUboMX_UNgaPBsUOIgasn3-Q']
    rt_channels_to_youtube['ScrewAttack'] = ['UUB9_VH_CNbbH4GfKu8qh63w']
    rt_channels_to_youtube['Cow Chop'] = ['UUmYBTQilY7p8EQ9IsyA3oLw']
    rt_channels_to_youtube['Sugar Pine 7'] = ['UUEY0yxj6QxG4RBVRSe5orig']
    rt_channels_to_youtube['Game Attack'] = ['UUWDIL65Y3kHmLjfp_0ZrpfQ']
    rt_channels_to_youtube['The Know'] = ['UU4w_tMnHl6sw5VD93tVymGw']


    channels = api.get_channels()
    if request.method == 'GET':
        return html_helper.channel_form(channels)

    if request.method == 'POST':
        selected_channels = request.form.getlist('channel')
        eps_requested = request.form.get('episodes')
        pages_requested = request.form.get('pages')

        all_eps = []
        all_youtube_eps = {}
        for channel in selected_channels:
            episodes = api.get_episode_pages(channel,
                                             channels[channel],
                                             pages_requested,
                                             eps_requested)
            if channel in rt_channels_to_youtube:
                for playlist in rt_channels_to_youtube[channel]:
                    all_youtube_eps.update(api.get_youtube_videos(playlist, str(eps_requested)))
            all_eps.extend(episodes)

        episodes_html = []
        all_eps.sort(key=operator.itemgetter(4), reverse=True)
        for e in all_eps:
            episodes_html.append(html_helper.episode_html(e, all_youtube_eps))
        ra_html = html_helper.recently_added_html(episodes_html)

        return ra_html
