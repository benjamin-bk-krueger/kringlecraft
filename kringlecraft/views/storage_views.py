import os
import flask
from flask_login import (login_required, current_user)  # to manage user sessions

blueprint = flask.Blueprint('storage', __name__, template_folder='templates')


@blueprint.route('/profile/image/clear', methods=['GET'])
@login_required
def profile_image_clear():
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services

    # (4a) perform operations
    user = user_services.set_user_image(current_user.id, None)

    if not user:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="User does not exist.")

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('account.profile_edit'))


@blueprint.route('/profile/image/<string:user_hash>', methods=['POST'])
@login_required
def profile_image_post(user_hash):
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    f = flask.request.files.get('file')
    ending = os.path.splitext(f.filename)[1][1:]
    # f.save(os.path.join('static/uploads/profile', f.filename))
    f.save(os.path.join('static/uploads/profile/', user_hash) + "." + ending)

    # (4a) perform operations
    user = user_services.set_user_image(current_user.id, user_hash + "." + ending)

    if not user:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="User does not exist.")

    # (6f) other result
    return "Uploaded successfully"
