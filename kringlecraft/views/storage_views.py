import flask
from flask_login import (login_required)  # to manage user sessions

from kringlecraft.utils.file_tools import (delete_temp_files, delete_image, delete_image_in_path, create_path,
                                           save_file_with_name, save_file_in_path)

blueprint = flask.Blueprint('storage', __name__, template_folder='templates')


@blueprint.route('/clear/image/<string:category>/<int:image_id>', methods=['GET'])
@login_required
def clear_image(category, image_id):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    delete_image(category, image_id)

    # (6b) redirect to new page after successful operation
    if category == "profile":
        return flask.redirect(flask.url_for('account.profile_edit'))
    if category == "world":
        return flask.redirect(flask.url_for('data.world', world_id=image_id))
    if category == "room":
        return flask.redirect(flask.url_for('data.room', room_id=image_id))
    if category == "objective":
        return flask.redirect(flask.url_for('data.objective', objective_id=image_id))


@blueprint.route('/clear/image/<string:category>/<string:path>/<string:filename>', methods=['GET'])
@login_required
def clear_image_path(category, path, filename):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    delete_image_in_path(category, path, filename)

    # (6b) redirect to new page after successful operation
    if category == "objective":
        return flask.redirect(flask.url_for('task.challenge', objective_id=path))


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
    save_file_with_name(f, category, "_temp")

    # (6f) another result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image/path/<string:category>/<string:path>', methods=['POST'])
@login_required
def upload_image_path_post(category, path):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    f = flask.request.files.get('file')
    create_path(category, path)

    save_file_in_path(f, category, path)

    # (6f) another result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image/<string:category>/<string:filename>', methods=['POST'])
@login_required
def upload_image_post(category, filename):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    delete_image(category, filename)
    f = flask.request.files.get('file')
    save_file_with_name(f, category, filename)

    # (6f) another result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})
