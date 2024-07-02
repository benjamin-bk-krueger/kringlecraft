import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import read_file_without_extension
from kringlecraft.utils.misc_tools import get_markdown

blueprint = flask.Blueprint('report', __name__, template_folder='templates')


# Show a report containing information about a specific objective and its solution in different formats
@blueprint.route('/single/<int:objective_id>', methods=['GET'])
@login_required
def single(objective_id):
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    objective_image = read_file_without_extension("objective", my_objective.id)
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    html_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)
    html_solution = "" if solution_services.find_objective_solution_for_user(objective_id, current_user.id) is None else (
        get_markdown(solution_services.find_objective_solution_for_user(objective_id, current_user.id).notes))

    # (6a) show rendered page
    return flask.render_template('report/single.html', objective=my_objective,
                                 objective_image=objective_image, room=my_room, world=my_world,
                                 objective_types=objective_services.get_objective_types(),
                                 html_challenge=html_challenge, html_solution=html_solution)
