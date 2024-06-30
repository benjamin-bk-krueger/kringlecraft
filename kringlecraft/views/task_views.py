import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.file_tools import get_sub_images
from kringlecraft.utils.misc_tools import get_markdown, convert_markdown

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
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    objective_form = ObjectiveForm(my_objective)
    objective_form.process()
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_challenge = objective_services.get_objective_challenge(my_objective.id)

    image_files = get_sub_images("objective", str(my_objective.id))

    www_server = flask.current_app.config['app.www_server']

    # (6a) show rendered page
    return flask.render_template('task/challenge.html', objective_form=objective_form,
                                 objective=my_objective, room=my_room, world=my_world, challenge=my_challenge,
                                 image_files=image_files, www_server=www_server, page_mode="init")


# Post a change in an objective's challenge
@blueprint.route('/challenge/<int:objective_id>', methods=['POST'])
@login_required
def challenge_post(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit objectives.")

    # (2) initialize form data
    objective_form = ObjectiveForm()
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
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    objective_form = ObjectiveForm()
    objective_form.process()
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_challenge = flask.request.form["challenge"]

    image_files = get_sub_images("objective", str(my_objective.id))

    www_server = flask.current_app.config['app.www_server']

    # (6a) show rendered page
    return flask.render_template('task/challenge.html', objective_form=objective_form,
                                 objective=my_objective, room=my_room, world=my_world, challenge=my_challenge,
                                 image_files=image_files, www_server=www_server, page_mode="init")


# Shows information about a specific report's notes
@blueprint.route('/summary/<int:world_id>', methods=['GET'])
@login_required
def summary(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.task_forms import SummaryForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.summary_services as summary_services

    # (2) initialize form data
    my_world = world_services.find_world_by_id(world_id)
    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    my_summary = summary_services.find_world_summary_for_user(world_id, current_user.id)
    summary_form = SummaryForm(my_summary)
    summary_form.process()
    my_notes = "New notes" if my_summary is None else convert_markdown(my_summary.notes)

    # (6a) show rendered page
    return flask.render_template('task/summary.html', summary_form=summary_form, notes=my_notes,
                                 world=my_world)


# Post a change in a report's notes
@blueprint.route('/summary/<int:world_id>', methods=['POST'])
@login_required
def summary_post(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.task_forms import SummaryForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.summary_services as summary_services

    # (2) initialize form data
    summary_form = SummaryForm()
    my_world = world_services.find_world_by_id(world_id)
    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    # (4a) perform operations
    my_summary = summary_services.create_or_edit_summary(world_id, current_user.id, summary_form.visible_content)
    my_summary = summary_services.set_world_notes_for_user(my_world.id, current_user.id,
                                                           flask.request.form["notes"].encode())

    if not my_summary:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Summary could not be edited.")

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.world', world_id=my_world.id))


# Shows information about a specific objective's solution
@blueprint.route('/solution/<int:objective_id>', methods=['GET'])
@login_required
def solution(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.task_forms import SolutionForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_solution = solution_services.find_objective_solution_for_user(objective_id, current_user.id)
    solution_form = SolutionForm(my_solution)
    solution_form.process()
    my_notes = "New notes" if my_solution is None else convert_markdown(my_solution.notes)

    image_files = get_sub_images("profile", str(current_user.id) + "/" + str(my_objective.id))

    www_server = flask.current_app.config['app.www_server']

    md_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)

    # (6a) show rendered page
    return flask.render_template('task/solution.html', solution_form=solution_form, notes=my_notes,
                                 world=my_world, room=my_room, objective=my_objective, md_challenge=md_challenge,
                                 image_files=image_files, www_server=www_server)


# Post a change in an objective's solution
@blueprint.route('/solution/<int:objective_id>', methods=['POST'])
@login_required
def solution_post(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.task_forms import SolutionForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    solution_form = SolutionForm()
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    # (4a) perform operations
    my_solution = solution_services.create_or_edit_solution(objective_id, current_user.id,
                                                            solution_form.visible_content,
                                                            solution_form.completed_content,
                                                            solution_form.ctf_flag_content)
    my_solution = solution_services.set_objective_notes_for_user(my_objective.id, current_user.id,
                                                                 flask.request.form["notes"].encode())

    if not my_solution:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Solution could not be edited.")

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.objective', objective_id=my_objective.id))


@blueprint.route('/solution/continue/<int:objective_id>', methods=['POST'])
@login_required
def solution_continue(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.task_forms import SolutionForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)
    my_solution = solution_services.find_objective_solution_for_user(objective_id, current_user.id)
    solution_form = SolutionForm(my_solution)
    solution_form.process()
    my_notes = flask.request.form["notes"]

    image_files = get_sub_images("profile", str(current_user.id) + "/" + str(my_objective.id))

    www_server = flask.current_app.config['app.www_server']

    md_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)

    # (6a) show rendered page
    return flask.render_template('task/solution.html', solution_form=solution_form, notes=my_notes,
                                 world=my_world, room=my_room, objective=my_objective, md_challenge=md_challenge,
                                 image_files=image_files, www_server=www_server)
