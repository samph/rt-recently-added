"""HTML Helper functions."""
from flask import url_for


def episode_html(episode, youtube_episodes):
    """Construct HTML element for an episode."""
    print("EPISODE HTML FOR " + episode.title)
    ep_template = "<li><a href=\"{0}\"><div class=\"block-container\">" +\
                  "<div class=\"image-container\"><img src=\"{1}\"></div>" +\
                  "</div><p class=\"name\">{2}</p></a>{3}</li>"

    youtube_template = "</br>YouTube Link: <a href=\"{0}\">{1}</a>"
    extra_link = ""

    if not episode.sponsor:
        for ep in youtube_episodes:
            if episode.title[:-7].lower() in ep.lower():
                extra_link = youtube_template.format(youtube_episodes[ep], ep)
                break

    ep_html = ep_template.format(episode.link, episode.thumb, episode.name, extra_link)

    return ep_html


def recently_added_html(episode_html_list):
    """Construct HTML for the recently added page."""
    episodes_html = ""
    for ep_html in episode_html_list:
        episodes_html = episodes_html + ep_html
    style = url_for('static', filename='css/style.css')
    page_template = "<!DOCTYPE html><html><head>" +\
                    "<link rel=\"stylesheet\" href=\""+style+"\"></head>" +\
                    "<body><ul class=\"grid-blocks\">{0}</ul></body></html>"

    return page_template.format(episodes_html)


def channel_form(channels):
    """Construct HTML for the channel selection form."""
    channel_checkbox_form_html = \
        "<input type=\"checkbox\" name=\"channel\" value=\"{0}\">{0}"
    channel_form_html = ""
    for channel in channels:
        channel_form_html = \
            channel_form_html + \
            channel_checkbox_form_html.format(channel) + "</br>"

    eps = "Episodes per page (between 1 and 50):" + \
          "<input type=\"number\" name=\"episodes\" " + \
          "min=\"1\" max=\"50\" value=\"20\"></br>"
    pages = "Pages (between 1 and 6):" + \
            "<input type=\"number\" name=\"pages\" " + \
            "min=\"1\" max=\"6\" value=\"1\"></br>"

    form = "<form action=\"/rt-recently-added\" method=\"post\">{0}{1}{2}" + \
           "<input type=\"submit\"></form>"

    form = form.format(channel_form_html, eps, pages)

    return form
