# rt-recently-added

A basic implementation of the previous Rooster Teeth Recently Added Episodes page which is missing from the new website.

Implemented as a Python Flask webserver, it is intended to be run locally, rather than hosted somewhere centrally for many users.

This is because this implementation has a number of shortcomings. (Mostly that there is no caching)

## Instructions
* setup.bat and run.bat should cover starting up the server - assuming python3 and pip3 are installed and on the PATH and the PYTHONPATH is set correctly.

Failing that, the steps broadly are:

* Install python3, make sure to add it to the PATH and set up the PYTHONPATH correctly.
* Set up a virtualenv, installing the requirements as detailed in requirements.txt
* Set the FLASK_APP environment variable to point at rt-ra.py
* Call ``flask run`` within the virtualenv

# TODO

* Consider implementing in Javascript / NPM - so that one centralised server wouldn't be hammering the API
* Consider implementing caching so API calls are not made on every request
* Implement tests
* Improve setup scripts and make cross platform.
* Improve CSS
* Allow specification of date ranges rather than number of episodes
* Allow distinct number of episodes retrieved for each channel

# Images

![Form](https://i.imgur.com/oOtMOtS.png)

![Grid](https://i.imgur.com/qCOgUg8.jpg)