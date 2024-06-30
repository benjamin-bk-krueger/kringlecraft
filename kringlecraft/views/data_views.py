import flask
from flask_login import (login_required, current_user)  # to manage user sessions

from kringlecraft.utils.mail_tools import (send_mail)
from kringlecraft.utils.file_tools import (get_temp_file, file_extension, get_all_images, get_image, enable_image)
from kringlecraft.utils.misc_tools import get_markdown

blueprint = flask.Blueprint('data', __name__, template_folder='templates')


# Show statistics regarding available elements stored in the database and on local file storage
@blueprint.route('/stats', methods=['GET'])
def stats():
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services

    # (2) initialize form data
    counts = dict()
    counts['user'] = user_services.get_user_count()
    counts['world'] = world_services.get_world_count()
    counts['room'] = room_services.get_room_count()
    counts['objective'] = objective_services.get_objective_count()
    counts['solution'] = solution_services.get_active_count()

    # (6a) show rendered page
    return flask.render_template('data/stats.html', counts=counts)


# Displays all available users
@blueprint.route('/users', methods=['GET'])
@login_required
def users():
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    all_users = user_services.find_all_users() if current_user.role == 0 else user_services.find_active_users()
    user_images = get_all_images("profile")

    # (6a) show rendered page
    return flask.render_template('account/users.html', users=all_users, user_images=user_images)


# Shows information about a specific student
@blueprint.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    my_user = user_services.find_user_by_id(user_id) if current_user.role == 0 else (
        user_services.find_active_user_by_id(user_id))
    if not my_user:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="User does not exist.")

    user_image = get_image("profile", my_user.id)

    # (6a) show rendered page
    return flask.render_template('account/user.html', user=my_user, user_image=user_image)


# Approve a user's registration
@blueprint.route('/user/<int:user_id>/approve', methods=['GET'])
@login_required
def user_approve(user_id):
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to approve users.")

    # (4a) perform operations
    my_user = user_services.enable_user(user_id)

    if not my_user:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="User does not exist.")

    # (4b) perform closing operations
    send_mail(f"{my_user.name} - Registration complete",
              "Your registration has been approved. You can use your login now.", [my_user.email])

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.users'))


# Displays all available worlds
@blueprint.route('/worlds', methods=['GET'])
def worlds():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import WorldForm
    import kringlecraft.services.world_services as world_services

    # (2) initialize form data
    world_form = WorldForm()
    world_form.process()
    all_worlds = world_services.find_all_worlds()
    world_images = get_all_images("world")

    # (6a) show rendered page
    return flask.render_template('data/worlds.html', world_form=world_form, worlds=all_worlds,
                                 world_images=world_images, page_mode="init")


# Post a new world - if it doesn't already exist
@blueprint.route('/worlds', methods=['POST'])
@login_required
def worlds_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import WorldForm
    import kringlecraft.services.world_services as world_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to create worlds.")

    # (2) initialize form data
    world_form = WorldForm()
    conflicting_world = world_services.find_world_by_name(world_form.name_content)
    temp_ending = None if get_temp_file("world") is None else (file_extension(get_temp_file("world")))

    # (3) check valid form data
    if world_form.validate_on_submit() and conflicting_world is None:
        # (4a) perform operations
        my_world = world_services.create_world(world_form.name_content, world_form.description_content,
                                               world_form.url_content, world_form.visible_content,
                                               world_form.archived_content, current_user.id)
        enable_image("world", my_world.id)

        if not my_world:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="World could not be created.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.worlds'))

    # (5) preset form with existing data
    world_form.set_field_defaults(conflicting_world is not None)
    world_form.process()
    all_worlds = world_services.find_all_worlds()
    world_images = get_all_images("world")

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/worlds.html', world_form=world_form, worlds=all_worlds,
                                 world_images=world_images, page_mode="add", temp_ending=temp_ending)


# Shows information about a specific world
@blueprint.route('/world/<int:world_id>', methods=['GET'])
def world(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import WorldForm
    import kringlecraft.services.world_services as world_services

    # (2) initialize form data
    my_world = world_services.find_world_by_id(world_id)
    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    world_image = get_image("world", my_world.id)
    world_form = WorldForm(my_world)
    world_form.process()

    # (6a) show rendered page
    return flask.render_template('data/world.html', world_form=world_form, world=my_world,
                                 world_image=world_image, page_mode="init")


# Post a change in the world's data
@blueprint.route('/world_post/<int:world_id>', methods=['POST'])
@login_required
def world_post(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import WorldForm
    import kringlecraft.services.world_services as world_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit worlds.")

    # (2) initialize form data
    world_form = WorldForm()
    my_world = world_services.find_world_by_id(world_id)
    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    conflicting_world = world_services.find_world_by_name(world_form.name_content)
    temp_ending = None if get_temp_file("world") is None else (file_extension(get_temp_file("world")))

    # (3) check valid form data
    if world_form.validate_on_submit() and (my_world.name == world_form.name_content or conflicting_world is None):
        # (4a) perform operations
        my_world = world_services.edit_world(world_id, world_form.name_content, world_form.description_content,
                                             world_form.url_content, world_form.visible_content,
                                             world_form.archived_content)
        enable_image("world", my_world.id)

        if not my_world:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="World could not be edited.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.world', world_id=my_world.id))

    # (5) preset form with existing data
    world_form.set_field_defaults(conflicting_world is not None and (my_world.name != world_form.name_content))
    world_form.process()
    world_image = get_image("world", my_world.id)

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/world.html', world_form=world_form, world=my_world,
                                 world_image=world_image, page_mode="edit", temp_ending=temp_ending)


# Delete a specific world - and all included elements!!!
@blueprint.route('/world/delete/<int:world_id>', methods=['GET'])
@login_required
def world_delete(world_id):
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to delete worlds.")

    # (4a) perform operations
    my_world = world_services.delete_world(world_id)
    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.worlds'))


# Displays all available rooms
@blueprint.route('/rooms/<int:world_id>', methods=['GET'])
def rooms(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import RoomForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services

    # (2) initialize form data
    room_form = RoomForm()
    room_form.process()
    my_world = world_services.find_world_by_id(world_id)

    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    all_rooms = room_services.find_world_rooms(my_world.id)
    room_images = get_all_images("room")

    # (6a) show rendered page
    return flask.render_template('data/rooms.html', room_form=room_form, rooms=all_rooms,
                                 room_images=room_images, world=my_world, page_mode="init")


# Post a new room - if it doesn't already exist
@blueprint.route('/rooms/<int:world_id>', methods=['POST'])
@login_required
def rooms_post(world_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import RoomForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to create rooms.")

    # (2) initialize form data
    room_form = RoomForm()
    my_world = world_services.find_world_by_id(world_id)

    if not my_world:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="World does not exist.")

    conflicting_room = room_services.find_world_room_by_name(my_world.id, room_form.name_content)
    temp_ending = None if get_temp_file("room") is None else (file_extension(get_temp_file("room")))

    # (3) check valid form data
    if room_form.validate_on_submit() and conflicting_room is None:
        # (4a) perform operations
        my_room = room_services.create_room(room_form.name_content, room_form.description_content,
                                            my_world.id, current_user.id)
        enable_image("room", my_room.id)

        if not my_room:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="Room could not be created.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.rooms', world_id=my_world.id))

    # (5) preset form with existing data
    room_form.set_field_defaults(conflicting_room is not None)
    room_form.process()
    all_rooms = room_services.find_world_rooms(my_world.id)
    room_images = get_all_images("room")

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/rooms.html', room_form=room_form, rooms=all_rooms,
                                 room_images=room_images, world=my_world, page_mode="add", temp_ending=temp_ending)


# Shows information about a specific room
@blueprint.route('/room/<int:room_id>', methods=['GET'])
def room(room_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import RoomForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services

    # (2) initialize form data
    my_room = room_services.find_room_by_id(room_id)
    if not my_room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    room_image = get_image("room", my_room.id)
    room_form = RoomForm(my_room)
    room_form.process()
    my_world = world_services.find_world_by_id(my_room.world_id)

    room_form.world.choices = world_services.get_world_choices(world_services.find_all_worlds())
    room_form.world.default = my_room.world_id
    room_form.process()

    # (6a) show rendered page
    return flask.render_template('data/room.html', room_form=room_form, room=my_room,
                                 room_image=room_image, world=my_world, page_mode="init")


# Post a change in a room's data
@blueprint.route('/room_post/<int:room_id>', methods=['POST'])
@login_required
def room_post(room_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import RoomForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit rooms.")

    # (2) initialize form data
    room_form = RoomForm()
    my_room = room_services.find_room_by_id(room_id)
    if not my_room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    conflicting_room = room_services.find_world_room_by_name(room_form.world_content, room_form.name_content)
    temp_ending = None if get_temp_file("room") is None else (file_extension(get_temp_file("room")))

    # (3) check valid form data
    if room_form.validate_on_submit() and (conflicting_room is None or my_room.world_id == conflicting_room.world_id and
                                           my_room.name == room_form.name_content):
        # (4a) perform operations
        my_room = room_services.edit_room(room_id, room_form.world_content, room_form.name_content,
                                          room_form.description_content)
        enable_image("room", my_room.id)

        if not my_room:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="Room could not be edited.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.room', room_id=my_room.id))

    # (5) preset form with existing data
    room_form.set_field_defaults(conflicting_room is not None and ((my_room.name != room_form.name_content) or
                                                                   (my_room.world_id != conflicting_room.world_id)))
    room_form.process()
    room_image = get_image("room", my_room.id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    room_form.world.choices = world_services.get_world_choices(world_services.find_all_worlds())
    room_form.world.default = room_form.world_content
    room_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/room.html', room_form=room_form, room=my_room,
                                 room_image=room_image, page_mode="edit", world=my_world, temp_ending=temp_ending)


# Delete a specific room - and all included elements!!!
@blueprint.route('/room/delete/<int:room_id>', methods=['GET'])
@login_required
def room_delete(room_id):
    # (1) import forms and utilities
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to delete rooms.")

    # (4a) perform operations
    my_room = room_services.delete_room(room_id)
    if not my_room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    my_world = world_services.find_world_by_id(my_room.world_id)

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.rooms', world_id=my_world.id))


# Displays all available objectives
@blueprint.route('/objectives/<int:room_id>', methods=['GET'])
def objectives(room_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    # (2) initialize form data
    objective_form = ObjectiveForm()
    objective_form.process()
    my_room = room_services.find_room_by_id(room_id)

    if not my_room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    all_objectives = objective_services.find_room_objectives(my_room.id)
    objective_images = get_all_images("objective")
    my_world = world_services.find_world_by_id(my_room.world_id)

    objective_form.type.choices = objective_services.get_objective_type_choices()
    objective_form.process()

    # (6a) show rendered page
    return flask.render_template('data/objectives.html', objective_form=objective_form,
                                 objectives=all_objectives, objective_images=objective_images, room=my_room,
                                 world=my_world, page_mode="init",
                                 objective_types=objective_services.get_objective_types())


# Post a new objective - if it doesn't already exist
@blueprint.route('/objectives/<int:room_id>', methods=['POST'])
@login_required
def objectives_post(room_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to create objectives.")

    # (2) initialize form data
    objective_form = ObjectiveForm()
    my_room = room_services.find_room_by_id(room_id)

    if not my_room:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Room does not exist.")

    conflicting_objective = objective_services.find_room_objective_by_name(my_room.id, objective_form.name_content)
    temp_ending = None if get_temp_file("objective") is None else (file_extension(get_temp_file("objective")))

    # (3) check valid form data
    if objective_form.validate_on_submit() and conflicting_objective is None:
        # (4a) perform operations
        my_objective = objective_services.create_objective(objective_form.name_content,
                                                           objective_form.description_content,
                                                           objective_form.difficulty_content,
                                                           objective_form.visible_content,
                                                           objective_form.type_content, my_room.id, current_user.id)
        enable_image("objective", my_objective.id)

        if not my_objective:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="Objective could not be created.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.objectives', room_id=my_room.id))

    # (5) preset form with existing data
    objective_form.set_field_defaults(conflicting_objective is not None)
    objective_form.process()
    all_objectives = objective_services.find_room_objectives(my_room.id)
    objective_images = get_all_images("objective")
    my_world = world_services.find_world_by_id(my_room.world_id)

    objective_form.type.choices = objective_services.get_objective_type_choices()
    objective_form.type.default = objective_form.type_content
    objective_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/objectives.html', objective_form=objective_form,
                                 objectives=all_objectives, objective_images=objective_images, room=my_room,
                                 world=my_world, page_mode="add",
                                 objective_types=objective_services.get_objective_types(), temp_ending=temp_ending)


# Shows information about a specific objective
@blueprint.route('/objective/<int:objective_id>', methods=['GET'])
def objective(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    objective_image = get_image("objective", my_objective.id)
    objective_form = ObjectiveForm(my_objective)
    objective_form.process()
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    objective_form.type.choices = objective_services.get_objective_type_choices()
    objective_form.type.default = objective_form.type_content

    objective_form.room.choices = room_services.get_room_choices(room_services.find_all_rooms())
    objective_form.room.default = my_objective.room_id
    objective_form.process()

    md_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)
    all_solutions = solution_services.find_active_solutions(objective_id)
    md_solution = None if len(all_solutions) != 1 else get_markdown(all_solutions[0].notes)
    candidate_solutions = None if len(all_solutions) < 1 else all_solutions
    user_list = {key: value for key, value in user_services.get_user_choices(user_services.find_all_users())}

    # (6a) show rendered page
    return flask.render_template('data/objective.html', objective_form=objective_form,
                                 objective=my_objective, objective_image=objective_image, room=my_room, world=my_world,
                                 page_mode="init", objective_types=objective_services.get_objective_types(),
                                 md_challenge=md_challenge, md_solution=md_solution,
                                 candidate_solutions=candidate_solutions, user_list=user_list)


# Post a change in an objective's data
@blueprint.route('/objective_post/<int:objective_id>', methods=['POST'])
@login_required
def objective_post(objective_id):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.data_forms import ObjectiveForm
    import kringlecraft.services.world_services as world_services
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services
    import kringlecraft.services.solution_services as solution_services
    import kringlecraft.services.user_services as user_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to edit objectives.")

    # (2) initialize form data
    objective_form = ObjectiveForm()
    my_objective = objective_services.find_objective_by_id(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    conflicting_objective = objective_services.find_room_objective_by_name(objective_form.room_content,
                                                                           objective_form.name_content)
    temp_ending = None if get_temp_file("objective") is None else (file_extension(get_temp_file("objective")))

    # (3) check valid form data
    if objective_form.validate_on_submit() and (conflicting_objective is None or my_objective.room_id ==
                                                conflicting_objective.room_id and my_objective.name ==
                                                objective_form.name_content):
        # (4a) perform operations
        my_objective = objective_services.edit_objective(objective_id, objective_form.room_content,
                                                         objective_form.name_content,
                                                         objective_form.description_content,
                                                         objective_form.difficulty_content,
                                                         objective_form.visible_content, objective_form.type_content)
        enable_image("objective", my_objective.id)

        if not my_objective:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="Objective could not be edited.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.objective', objective_id=my_objective.id))

    # (5) preset form with existing data
    objective_form.set_field_defaults(conflicting_objective is not None and ((my_objective.name !=
                                                                              objective_form.name_content) or
                                                                             (my_objective.room_id !=
                                                                              conflicting_objective.room_id)))
    objective_form.process()
    objective_image = get_image("objective", my_objective.id)
    my_room = room_services.find_room_by_id(my_objective.room_id)
    my_world = world_services.find_world_by_id(my_room.world_id)

    objective_form.type.choices = objective_services.get_objective_type_choices()
    objective_form.type.default = objective_form.type_content

    objective_form.room.choices = room_services.get_room_choices(room_services.find_all_rooms())
    objective_form.room.default = objective_form.room_content
    objective_form.process()

    md_challenge = "" if my_objective.challenge is None else get_markdown(my_objective.challenge)
    all_solutions = solution_services.find_active_solutions(objective_id)
    md_solution = None if len(all_solutions) != 1 else get_markdown(all_solutions[0].notes)
    candidate_solutions = None if len(all_solutions) < 1 else all_solutions
    user_list = {key: value for key, value in user_services.get_user_choices(user_services.find_all_users())}

    # (6c) show rendered page with possible error messages
    return flask.render_template('data/objective.html', objective_form=objective_form,
                                 objective=my_objective, objective_image=objective_image, room=my_room, world=my_world,
                                 page_mode="edit", objective_types=objective_services.get_objective_types(),
                                 md_challenge=md_challenge, md_solution=md_solution,
                                 candidate_solutions=candidate_solutions, user_list=user_list, temp_ending=temp_ending)


# Delete a specific objective - and all included elements!!!
@blueprint.route('/objective/delete/<int:objective_id>', methods=['GET'])
@login_required
def objective_delete(objective_id):
    # (1) import forms and utilities
    import kringlecraft.services.room_services as room_services
    import kringlecraft.services.objective_services as objective_services

    if current_user.role != 0:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="You are not authorized to delete objectives.")

    # (4a) perform operations
    my_objective = objective_services.delete_objective(objective_id)
    if not my_objective:
        # (6e) show dedicated error page
        return flask.render_template('home/error.html', error_message="Objective does not exist.")

    my_room = room_services.find_room_by_id(my_objective.room_id)

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('data.objectives', room_id=my_room.id))
