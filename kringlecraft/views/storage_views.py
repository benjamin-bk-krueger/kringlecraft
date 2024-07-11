import flask
from flask_login import (login_required)  # to manage user sessions

from kringlecraft.utils.file_tools import (is_valid_filename, is_valid_path, is_valid_sub_path, remove_image,
                                           store_file, remove_all_images)

blueprint = flask.Blueprint('storage', __name__, template_folder='templates')


@blueprint.route('/delete/image/<string:path>/<string:sub_path>/<string:filename>/<string:redirect>/<int:target_id>',  methods=['GET'])
@login_required
def delete_image(path, sub_path, filename, redirect, target_id):
    # (2) initialize form data
    if not is_valid_path(path) or not is_valid_sub_path(sub_path):
        return flask.jsonify({"status": "error", "message": "Path does not exist."})

    if redirect not in ('account.profile_edit', 'data.world', 'data.room', 'data.objective', 'task.challenge',
                        'task.solution'):
        return flask.jsonify({"status": "error", "message": "Redirect does not exist."})

    if not is_valid_filename(filename):
        return flask.jsonify({"status": "error", "message": "Filename is not valid."})

    # (4a) perform operations
    remove_image(f"{path}/{sub_path}", filename)

    # (6b) redirect to new page after successful operation
    if redirect == "account.profile_edit":
        return flask.redirect(flask.url_for(redirect))
    if redirect == "data.world":
        return flask.redirect(flask.url_for(redirect, world_id=target_id, page_mode="edit"))
    if redirect == "data.room":
        return flask.redirect(flask.url_for(redirect, room_id=target_id, page_mode="edit"))
    if redirect == "data.objective":
        return flask.redirect(flask.url_for(redirect, objective_id=target_id, page_mode="edit"))
    if redirect == "task.challenge":
        return flask.redirect(flask.url_for(redirect, objective_id=target_id))
    if redirect == "task.solution":
        return flask.redirect(flask.url_for(redirect, objective_id=target_id))


@blueprint.route('/upload/image/<string:path>/<string:sub_path>/<int:overwrite>', methods=['POST'])
@login_required
def upload_image_post(path, sub_path, overwrite):
    # (2) initialize form data
    if not is_valid_path(path) or not is_valid_sub_path(sub_path):
        return flask.jsonify({"status": "error", "message": "Path does not exist."})

    # (4a) perform operations
    f = flask.request.files.get('file')

    if overwrite:
        remove_all_images(f"{path}/{sub_path}")

    store_file(f, f"{path}/{sub_path}")

    # (6f) another result
    return flask.jsonify({"status": "success", "message": "File uploaded successfully"})
