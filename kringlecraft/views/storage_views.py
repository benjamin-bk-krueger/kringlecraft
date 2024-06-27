import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import (file_ending, file_name_without_extension, delete_temp_files, build_path)

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
    f.save(build_path("profile", user_hash, file_ending(f.filename)))

    # (4a) perform operations
    user = user_services.set_user_image(current_user.id, user_hash + "." + file_ending(f.filename))

    if not user:
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "User does not exist."})

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/prepare/image/<string:category>', methods=['POST'])
@login_required
def prepare_image_post(category):
    # (2) initialize form data
    if category not in ("world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    delete_temp_files(category)
    f = flask.request.files.get('file')
    f.save(build_path(category, "_temp", file_ending(f.filename)))

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image/<string:category>', methods=['POST'])
@login_required
def upload_image_post(category):
    # (2) initialize form data
    if category not in ("world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    f = flask.request.files.get('file')
    f.save(build_path(category, file_name_without_extension(f.filename), file_ending(f.filename)))

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})
