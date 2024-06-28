import os
import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import (file_extension, file_name_without_extension, delete_temp_files, build_path, delete_image, create_path, save_new_file, save_file, save_sub_file)

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
    save_new_file(f, category, "_temp")

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image/<string:category>', methods=['POST'])
@login_required
def upload_image_post(category):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    f = flask.request.files.get('file')
    save_file(f, category)

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image-sub/<string:category>/<int:object_id>', methods=['POST'])
@login_required
def upload_image_sub_post(category, object_id):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    f = flask.request.files.get('file')
    create_path(category, object_id)

    save_sub_file(f, category, str(object_id))

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})


@blueprint.route('/upload/image/<string:category>/<int:image_id>', methods=['POST'])
@login_required
def upload_image_id_post(category, image_id):
    # (2) initialize form data
    if category not in ("profile", "world", "room", "objective"):
        # (6e) show dedicated error page
        return flask.jsonify({"status": "error", "message": "Category does not exist."})

    # (4a) perform operations
    delete_image(category, image_id)
    f = flask.request.files.get('file')
    save_new_file(f, category, str(image_id))

    # (6f) other result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})