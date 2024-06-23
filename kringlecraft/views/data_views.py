import flask
from flask_login import (login_required, current_user)  # to manage user sessions
from kringlecraft.utils.mail_tools import (send_mail)

ADMIN = 0
USER = 1

blueprint = flask.Blueprint('data', __name__, template_folder='templates')


# Show statistics regarding available elements stored in the database and on S3 storage
@blueprint.route('/stats', methods=['GET'])
def stats():
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize elements
    counts = dict()
    counts['user'] = user_services.get_user_count()

    # show rendered page
    return flask.render_template('data/stats.html', counts=counts)


# Displays all available users
@blueprint.route('/users', methods=['GET'])
@login_required
def users():
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize elements
    all_users = user_services.find_all_users() if current_user.role == ADMIN else user_services.find_active_users()
    user_images = user_services.get_all_images()

    # show rendered page
    return flask.render_template('account/users.html', users=all_users, user_images=user_images)


# Shows information about a specific student
@blueprint.route('/user/<int:user_id>', methods=['GET'])
@login_required
def user(user_id):
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize elements
    my_user = user_services.find_user_by_id(user_id) if current_user.role == ADMIN else user_services.find_active_user_by_id(user_id)
    user_image = user_services.get_user_image(user_id)

    # show rendered page
    return flask.render_template('account/user.html', user=my_user, user_image=user_image)


# Approve a user's registration
@blueprint.route('/user/<int:user_id>/approve', methods=['GET'])
@login_required
def user_approve(user_id):
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # check valid contact data
    my_user = user_services.enable_user(user_id)
    if my_user:
        send_mail(f"{my_user.name} - Registration complete", "Your registration has been approved. You can use your login now.", [my_user.email])

    return flask.redirect(flask.url_for('data.users'))
