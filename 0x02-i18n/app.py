#!/usr/bin/env python3
""" App module. """
from typing import Union
from flask import Flask, request
from flask.templating import render_template
from flask_babel import Babel, format_datetime
from datetime import datetime
import flask
import pytz
app = Flask(__name__)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config():
    """ Config class. """
    LANGUAGES = ["en", "fr"]

    Babel.default_locale = "en"
    Babel.default_timezone = "UTC"


app.config.from_object(Config)
babel = Babel(app)


def get_user() -> Union[dict, None]:
    """ get_user function. """
    try:
        login_as: int = int(request.args.get("login_as"))
        user: dict = users.get(login_as)
        return user
    except Exception:
        return None


@babel.localeselector
def get_locale():
    """ Determines the best match with our supported language. """
    h_locale = request.args.get("locale")
    if h_locale and h_locale in Config.LANGUAGES:
        return h_locale

    if flask.g.user:
        u_locale = flask.g.user.get("locale", None)
        if u_locale and u_locale in Config.LANGUAGES:
            return u_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """ Determines the best match for the timezone. """
    h_timezone = request.args.get("timezone")
    if h_timezone:
        try:
            pytz.timezone(h_timezone)
            return h_timezone
        except pytz.UnknownTimeZoneError:
            pass

    if flask.g.user:
        u_timezone = flask.g.user.get("timezone", None)
        if u_timezone:
            try:
                pytz.timezone(h_timezone)
                return h_timezone
            except pytz.UnknownTimeZoneError:
                pass

    return "UTC"


@app.before_request
def before_request():
    """ Find a user if any, set it as global. """
    flask.g.user = get_user()


@app.route("/")
def hello_world():
    """ / endpoint. """
    current_time = format_datetime(datetime.now())
    return render_template("index.html", user=flask.g.user, time=current_time)
