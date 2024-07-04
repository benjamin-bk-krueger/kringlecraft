import os
import sys
import flask
import logging
from logging.handlers import SMTPHandler  # get crashes via mail

from flask_login import LoginManager  # to manage user sessions
from flask_wtf.csrf import CSRFProtect  # CSRF protection
from flask_mail import Mail  # to send mails
from flask_dropzone import Dropzone  # to allow file upload via dropzone

import kringlecraft.data.db_session as db_session
from utils import config_tools

folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, folder)


app = flask.Flask(__name__)


def main():
    configure_defaults()
    configure_logging()
    register_blueprints()
    setup_db()
    setup_csrf()
    setup_mail()
    setup_dropzone()
    setup_mail_logger()
    setup_login_manager()
    app.run(debug=True, port=5006)


def configure_defaults():
    cfg = config_tools.parse_config('cfg/kringle.json')
    for key in cfg['app']:
        app.config[f"app.{key}"] = cfg['app'][key]
        print(f"CONFIG key: {key}, value: {cfg['app'][key]}")
    for key in cfg['secret']:
        app.config[f"secret.{key}"] = cfg['secret'][key]
        print(f"SECRET key: {key}, value: ********")


def configure_logging():
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


def register_blueprints():
    from kringlecraft.views import (home_views, account_views, storage_views, data_views, task_views, report_views)

    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(account_views.blueprint)
    app.register_blueprint(storage_views.blueprint)
    app.register_blueprint(data_views.blueprint)
    app.register_blueprint(task_views.blueprint)
    app.register_blueprint(report_views.blueprint)


def setup_db():
    db_file = os.path.join(os.path.dirname(__file__), 'db', 'kringlecraft.sqlite')
    db_session.global_init(db_file, False)


def setup_csrf():
    # Enable CSRF protection for the app
    app.config['SECRET_KEY'] = app.config["secret.key"]  # Replace with an actual secret key
    csrf = CSRFProtect(app)


def setup_mail():
    # E-Mail configuration
    app.config['MAIL_SERVER'] = app.config["app.mail_server"]
    mail = Mail(app)
    app.config["mail.send"] = mail.send


def setup_dropzone():
    # Dropzone click and drop file upload
    dropzone = Dropzone(app)

    # Dropzone settings
    app.config['DROPZONE_UPLOAD_MULTIPLE'] = False
    app.config['DROPZONE_MAX_FILES'] = 1
    app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
    app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
    app.config['DROPZONE_ENABLE_CSRF'] = True
    app.config['DROPZONE_MAX_FILE_SIZE'] = 10


def setup_mail_logger():
    # Enable logging and crashes via mail
    if app.config["app.mail_enable"] == "true":
        mail_handler = SMTPHandler(
            mailhost=app.config["app.mail_server"],
            fromaddr=app.config["app.mail_sender"],
            toaddrs=[app.config["app.mail_admin"]],
            subject='kringlecraft.com: Application Error'
        )
        mail_handler.setLevel(logging.ERROR)
        mail_handler.setFormatter(logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        ))

        if not app.debug:
            app.logger.addHandler(mail_handler)


def setup_login_manager():
    from kringlecraft.services.user_services import find_active_user_by_id

    # Login Manager configuration
    login_manager = LoginManager()
    login_manager.login_view = 'home.login'  # show this page if a login is required
    login_manager.init_app(app)

    # link the Login Manager to the correct user entry
    @login_manager.user_loader
    def load_user(user_id):
        # since the student_id is just the primary key of our user table, use it in the query for the user
        return find_active_user_by_id(user_id)


if __name__ == '__main__':
    main()
else:
    configure_defaults()
    configure_logging()
    register_blueprints()
    setup_db()
    setup_csrf()
    setup_mail()
    setup_dropzone()
    setup_mail_logger()
    setup_login_manager()
