import os
import flask
from flask_login import current_user  # to manage user sessions

blueprint = flask.Blueprint('storage', __name__, template_folder='templates')


@blueprint.route('/uploads/profile/<string:user_hash>', methods=['GET'])
def upload_get(user_hash):
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize form data
    user = user_services.set_user_image(current_user.id, None)

    return flask.redirect(flask.url_for('account.edit_get'))


@blueprint.route('/uploads/profile/<string:user_hash>', methods=['POST'])
def upload_post(user_hash):
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize form data
    f = flask.request.files.get('file')
    ending = os.path.splitext(f.filename)[1][1:]
    # f.save(os.path.join('static/uploads/profile', f.filename))
    f.save(os.path.join('static/uploads/profile/', user_hash) + "." + ending)

    user = user_services.set_user_image(current_user.id, user_hash + "." + ending)

    return "Uploaded successfully"
