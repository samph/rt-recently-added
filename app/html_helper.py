"""HTML Helper functions."""
from flask import url_for


def episode_html(episode):
    """Construct HTML element for an episode."""
    ep_template = "<li><a href=\"{0}\"><div class=\"block-container\">" +\
                  "<div class=\"image-container\"><img src=\"{1}\"></div>" +\
                  "</div><p class=\"name\">{2}</p></a></li>"

    ep_html = ep_template.format(episode.link, episode.thumb, episode.name)

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

    eps = "Episodes per page (between 1 and 100):" + \
          "<input type=\"number\" name=\"episodes\" " + \
          "min=\"1\" max=\"100\" value=\"20\"></br>"
    pages = "Pages (between 1 and 3):" + \
            "<input type=\"number\" name=\"pages\" " + \
            "min=\"1\" max=\"3\" value=\"1\"></br>"

    form = "<form action=\"/rt-recently-added\" method=\"post\">{0}{1}{2}" + \
           "<input type=\"submit\"></form>"

    form = form.format(channel_form_html, eps, pages)

    return form
