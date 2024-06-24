import flask
from flask_login import (login_required, current_user)  # to manage user sessions

import kringlecraft.services.misc_services
from kringlecraft.utils.mail_tools import (send_mail)


blueprint = flask.Blueprint('data', __name__, template_folder='templates')


# Show statistics regarding available elements stored in the database and on S3 storage
@blueprint.route('/stats', methods=['GET'])
def stats():
    # (1) import forms and utilities
    import kringlecraft.services.user_services as user_services
    import kringlecraft.services.world_services as world_services

    # (2) initialize form data
    counts = dict()
    counts['user'] = user_services.get_user_count()
    counts['world'] = world_services.get_world_count()

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
    user_images = user_services.get_all_images()

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
    user_image = user_services.get_user_image(user_id)

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
    all_worlds = world_services.find_all_worlds()
    world_images = world_services.get_all_images()

    # (6a) show rendered page
    return flask.render_template('data/worlds.html', world_form=world_form, worlds=all_worlds,
                                 world_images=world_images, page_mode="init", file_mode="init")


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
    file_mode = "init" if world_services.get_temp_image() is None else kringlecraft.services.misc_services.file_ending(world_services.get_temp_image())

    # (3) check valid form data
    if world_form.validate_on_submit() and conflicting_world is None:
        # (4a) perform operations
        my_world = world_services.create_world(world_form.name_content, world_form.description_content,
                                               world_form.url_content, world_form.visible_content,
                                               world_form.archived_content, current_user.id)
        world_services.enable_world_image(my_world.id)

        if not my_world:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="World could not be created.")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('data.worlds'))
    else:
        # (5) preset form with existing data
        world_form.set_field_defaults(conflicting_world is not None)
        world_form.process()
        all_worlds = world_services.find_all_worlds()
        world_images = world_services.get_all_images()

        # (6c) show rendered page with possible error messages
        return flask.render_template('data/worlds.html', world_form=world_form, worlds=all_worlds,
                                     world_images=world_images, page_mode="add", file_mode=file_mode)
