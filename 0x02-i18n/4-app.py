#!/usr/bin/env python3
""" Route module for the API """
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config(object):
    """ Available languages class """
    LANGUAGES = ['en', 'fr']
    # these are the inherent defaults just btw
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# set the above class object as the configuration for the app
app.config.from_object('4-app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return:
      - 4-index.html
    """
    return render_template('4-index.html')


@babel.localeselector
def get_locale() -> str:
    """ Determines best match for supported languages """
    # check if there is a locale parameter/query string
    if request.args.get('locale'):
        locale = request.args.get('locale')
        if locale in app.config['LANGUAGES']:
            return locale
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
