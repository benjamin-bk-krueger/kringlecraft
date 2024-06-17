import os
import sys
import flask

from utils import config_tools

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)


app = flask.Flask(__name__)


def main():
    configure_defaults()
    register_blueprints()
    app.run(debug=True)


def configure_defaults():
    cfg = config_tools.parse_config('cfg/kringle.json')
    for key in cfg['app']:
        app.config[key] = cfg['app'][key]
        print(f"Config key: {key}, value: {cfg['app'][key]}")


def register_blueprints():
    from kringlecraft.views import home_views

    app.register_blueprint(home_views.blueprint)


if __name__ == '__main__':
    main()
