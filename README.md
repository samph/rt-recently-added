# rt-recently-added

A basic implementation of the previous Rooster Teeth Recently Added Episodes page which is missing from the new website.

Implemented as a Python Flask webserver, it is intended to be run locally, rather than hosted somewhere centrally for many users.

This is because this implementation has a number of shortcomings. (Mostly that there is no caching)

# TODO

* Consider implementing in Javascript / NPM - so that one centralised server wouldn't be hammering the API
* Consider implementing caching so API calls are not made on every request
* Implement tests
* Improve setup scripts and make cross platform.
* Implement setup script for virtualenv
