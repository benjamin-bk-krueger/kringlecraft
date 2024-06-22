import flask
from flask_login import (login_required, current_user, logout_user)  # to manage user sessions
from kringlecraft.utils.mail_tools import (send_admin_mail, send_mail)

ADMIN = 0
USER = 1

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# Displays a form to create a new user
@blueprint.route('/account/create', methods=['GET'])
def create_get():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import AccountForm

    # initialize form data
    account_form = AccountForm()
    account_form.process()

    # show rendered page
    return flask.render_template('account/create.html', account_form=account_form)


@blueprint.route('/account/create', methods=['POST'])
def create_post():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import AccountForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    account_form = AccountForm()

    # check valid contact data
    if account_form.validate_on_submit():
        user = user_services.create_user(account_form.user_content, account_form.email_content,
                                         account_form.password_content)
        if user:
            send_admin_mail(f"{account_form.user_content} - Approval required",
                            "A new user has registered, please approve registration.")
            send_mail(f"{account_form.user_content} - Registration pending",
                      "Your registration needs to be approved. This should not take too long.",
                      [account_form.email_content])

        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        account_form.set_field_defaults()
        account_form.process()

        # show page again and print possible errors in form
        return flask.render_template('account/create.html', account_form=account_form)


# Displays various forms to change the currently logged-in user
@blueprint.route('/account/edit', methods=['GET'])
@login_required
def edit_get():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # initialize elements
    user = user_services.find_user_by_id(current_user.id)

    # initialize form data
    user_hash = user_services.user_hash(user.email)
    user_image = user_services.get_user_image(user.id)
    mail_form = MailForm(user)
    password_form = PasswordForm()
    deletion_form = DeletionForm()
    mail_form.process()
    password_form.process()
    deletion_form.process()

    # show rendered page
    return flask.render_template('account/edit.html', mail_form=mail_form, password_form=password_form,
                                 deletion_form=deletion_form, user_hash=user_hash, user_image=user_image)


@blueprint.route('/account/edit/mail', methods=['POST'])
@login_required
def edit_mail_post():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # check valid contact data
    if mail_form.validate_on_submit():
        user = user_services.edit_user(current_user.id, mail_form.email_content, mail_form.description_content,
                                       mail_form.notification_content)
        if user:
            send_mail("Notification: E-Mail changed",
                      f"You have changed your e-mail address to {user.email}.", [user.email])

        return flask.redirect(flask.url_for('account.edit_get'))
    else:
        # preset form with existing data
        mail_form.set_field_defaults()
        mail_form.process()
        password_form.process()
        deletion_form.process()

        # show page again and print possible errors in form
        return flask.render_template('account/edit.html', mail_form=mail_form,
                                     password_form=password_form, deletion_form=deletion_form)


@blueprint.route('/account/edit/password', methods=['POST'])
@login_required
def edit_password_post():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # check valid contact data
    if password_form.validate_on_submit():
        user = user_services.change_user_password(current_user.id, password_form.password_content)
        if user:
            send_mail("Notification: Password changed",
                      f"You have changed your password for your account {user.email}.", [user.email])

        logout_user()
        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        mail_form.process()
        password_form.process()
        deletion_form.process()

        # show page again and print possible errors in form
        return flask.render_template('account/edit.html', mail_form=mail_form,
                                     password_form=password_form, deletion_form=deletion_form)


@blueprint.route('/account/edit/deletion', methods=['POST'])
@login_required
def edit_deletion_post():
    # import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # check valid contact data
    if deletion_form.validate_on_submit():
        user = user_services.delete_user(current_user.id)
        if user:
            send_mail("Notification: Account deleted", f"You have deleted your account {user.email}.", [user.email])

        logout_user()
        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        mail_form.process()
        password_form.process()
        deletion_form.process()

        # show page again and print possible errors in form
        return flask.render_template('account/edit.html', mail_form=mail_form,
                                     password_form=password_form, deletion_form=deletion_form)


# Displays all available users
@blueprint.route('/users', methods=['GET'])
@login_required
def users():
    # import forms and utilities
    import kringlecraft.services.user_services as user_services

    # initialize elements
    users = user_services.find_all_users() if current_user.role == ADMIN else user_services.find_active_users()
    user_images = user_services.get_all_images()

    # show rendered page
    return flask.render_template('account/users.html', users=users, user_images=user_images)
