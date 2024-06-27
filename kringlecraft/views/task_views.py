import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.mail_tools import (send_mail)
from kringlecraft.utils.file_tools import (get_temp_file, file_ending)

blueprint = flask.Blueprint('task', __name__, template_folder='templates')


# Shows information about a specific objective's quest
@blueprint.route('/challenge/<int:objective_id>', methods=['GET'])
@login_required
def challenge(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    # (6a) show rendered page
    return flask.render_template('task/challenge.html', objective=my_objective,
                                 room=my_room, world=my_world, page_mode="init")
