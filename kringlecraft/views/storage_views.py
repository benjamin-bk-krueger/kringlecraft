import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import (file_ending, delete_temp_files, build_path)

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
        return flask.render_template('home/error.html', error_message="User does not exist.")

    # (6f) other result
    return "Uploaded successfully"


@blueprint.route('/world/image/<int:world_id>/<string:world_hash>', methods=['POST'])
@login_required
def world_image_post(world_id, world_hash):
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services

    # (2) initialize form data
    delete_temp_files("world")
    f = flask.request.files.get('file')
    f.save(build_path("world", world_hash, file_ending(f.filename)))

    # (4a) perform operations
    if world_id == 0:
        return "Uploaded successfully (temp file)"

    world = world_services.set_world_image(world_id, world_hash + "." + file_ending(f.filename))

    if not world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    # (6f) other result
    return "Uploaded successfully"


@blueprint.route('/room/image/<int:room_id>/<string:room_hash>', methods=['POST'])
@login_required
def room_image_post(room_id, room_hash):
    # (1) import forms and utilities
    import kringlecraft.services.room_services as room_services

    # (2) initialize form data
    delete_temp_files("room")
    f = flask.request.files.get('file')
    f.save(build_path("room", room_hash, file_ending(f.filename)))

    # (4a) perform operations
    if room_id == 0:
        return "Uploaded successfully (temp file)"

    room = room_services.set_room_image(room_id, room_hash + "." + file_ending(f.filename))

    if not room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    # (6f) other result
    return "Uploaded successfully"


@blueprint.route('/objective/image/<int:objective_id>/<string:objective_hash>', methods=['POST'])
@login_required
def objective_image_post(objective_id, objective_hash):
    # (1) import forms and utilities
    import kringlecraft.services.objective_services as objective_services

    # (2) initialize form data
    delete_temp_files("objective")
    f = flask.request.files.get('file')
    f.save(build_path("objective", objective_hash, file_ending(f.filename)))

    # (4a) perform operations
    if objective_id == 0:
        return "Uploaded successfully (temp file)"

    objective = objective_services.set_objective_image(objective_id, objective_hash + "." + file_ending(f.filename))

    if not objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    # (6f) other result
    return "Uploaded successfully"
