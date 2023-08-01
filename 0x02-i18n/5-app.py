#!/usr/bin/env python3
""" App module. """
from typing import Union
from flask import Flask, request
from flask.templating import render_template
from flask_babel import Babel
import flask
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
    locale = request.args.get("locale")
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.before_request
def before_request():
    """ Find a user if any, set it as global. """
    flask.g.user = get_user()


@app.route("/")
def hello_world():
    """ / endpoint. """
    return render_template("5-index.html", user=flask.g.user)
