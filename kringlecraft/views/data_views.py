import flask
from flask_login import (login_required, current_user, logout_user)  # to manage user sessions
from kringlecraft.utils.mail_tools import (send_admin_mail, send_mail)


blueprint = flask.Blueprint('data', __name__, template_folder='templates')


# Show statistics regarding available elements stored in the database and on S3 storage
@blueprint.route('/stats')
def stats():
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize elements
    counts = dict()
    counts['user'] = user_services.get_user_count()

    # show rendered page
    return flask.render_template('data/stats.html', counts=counts)
