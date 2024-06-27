import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import get_image_files

blueprint = flask.Blueprint('task', __name__, template_folder='templates')


# Shows information about a specific objective's challenge
@blueprint.route('/challenge/<int:objective_id>', methods=['GET'])
@login_required
def challenge(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit challenges.")

    # (2) initialize form data
    objective_form = ObjectiveForm()
    objective_form.process()
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_challenge = objective_services.get_objective_challenge(my_objective.id)

    image_files = get_image_files("world")

    # (6a) show rendered page
    return flask.render_template('task/challenge.html', objective_form=objective_form, objective=my_objective,
                                 room=my_room, world=my_world, challenge=my_challenge, image_files=image_files, page_mode="init")


# Post a change in an objective's challenge
@blueprint.route('/challenge/<int:objective_id>', methods=['POST'])
@login_required
def challenge_post(objective_id):
    # (1) import forms and utilities
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit objectives.")

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    # (4a) perform operations
    my_objective = objective_services.set_objective_challenge(my_objective.id, flask.request.form["challenge"].encode())

    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective could not be edited.")

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.objective', objective_id=my_objective.id))


@blueprint.route('/challenge/continue/<int:objective_id>', methods=['POST'])
@login_required
def challenge_continue(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit challenges.")

    # (2) initialize form data
    objective_form = ObjectiveForm()
    objective_form.process()
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_challenge = flask.request.form["challenge"]

    image_files = get_image_files("world")

    # (6a) show rendered page
    return flask.render_template('task/challenge.html', objective_form=objective_form, objective=my_objective,
                                 room=my_room, world=my_world, challenge=my_challenge, image_files=image_files, page_mode="init")

