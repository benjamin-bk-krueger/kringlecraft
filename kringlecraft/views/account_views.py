import flask
from flask_login import (login_required, current_user, logout_user)  # to manage user sessions

from kringlecraft.utils.file_tools import file_hash
from kringlecraft.utils.mail_tools import (send_admin_mail, send_mail)

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


# Displays a form to create a new user
@blueprint.route('/profile/create', methods=['GET'])
def profile_create():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import AccountForm

    # (2) initialize form data
    account_form = AccountForm()
    account_form.process()

    # (6a) show rendered page
    return flask.render_template('account/create.html', account_form=account_form)


@blueprint.route('/profile/create', methods=['POST'])
def profile_create_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import AccountForm
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    account_form = AccountForm()

    # (3) check valid form data
    if account_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.create_user(account_form.name_content, account_form.email_content,
                                         account_form.password_content)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User could not be created.")

        # (4b) perform closing operations
        send_admin_mail(f"{account_form.name_content} - Approval required",
                        "A new user has registered, please approve registration.")
        send_mail(f"{account_form.name_content} - Registration pending",
                  "Your registration needs to be approved. This should not take too long.",
                  [account_form.email_content])

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    account_form.set_field_defaults()
    account_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('account/create.html', account_form=account_form)


# Displays various forms to change the currently logged-in user
@blueprint.route('/profile/edit', methods=['GET'])
@login_required
def profile_edit():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    user = user_services.find_user_by_id(current_user.id)
    user_hash = file_hash(user.email)
    user_image = user_services.get_user_image(user.id)
    mail_form = MailForm(user)
    password_form = PasswordForm()
    deletion_form = DeletionForm()
    mail_form.process()
    password_form.process()
    deletion_form.process()

    # (6a) show rendered page
    return flask.render_template('account/edit.html', mail_form=mail_form, password_form=password_form,
                                 deletion_form=deletion_form, user_hash=user_hash, user_image=user_image)


@blueprint.route('/profile/edit/mail', methods=['POST'])
@login_required
def profile_edit_mail_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # (3) check valid form data
    if mail_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.edit_user(current_user.id, mail_form.email_content, mail_form.description_content,
                                       mail_form.notification_content)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User does not exist.")

        # (4b) perform closing operations
        send_mail("Notification: E-Mail changed",
                  f"You have changed your e-mail address to {user.email}.", [user.email])

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('account.profile_edit'))

    # (5) preset form with existing data
    mail_form.set_field_defaults()
    mail_form.process()
    password_form.process()
    deletion_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('account/edit.html', mail_form=mail_form,
                                 password_form=password_form, deletion_form=deletion_form)


@blueprint.route('/profile/edit/password', methods=['POST'])
@login_required
def profile_edit_password_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # (3) check valid form data
    if password_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.change_user_password(current_user.id, password_form.password_content)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User does not exist.")

        # (4b) perform closing operations
        send_mail("Notification: Password changed",
                  f"You have changed your password for your account {user.email}.", [user.email])
        logout_user()

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    mail_form.process()
    password_form.process()
    deletion_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('account/edit.html', mail_form=mail_form,
                                 password_form=password_form, deletion_form=deletion_form)


@blueprint.route('/profile/edit/deletion', methods=['POST'])
@login_required
def profile_edit_deletion_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.account_forms import (MailForm, PasswordForm, DeletionForm)
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    mail_form = MailForm()
    password_form = PasswordForm()
    deletion_form = DeletionForm()

    # (3) check valid form data
    if deletion_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.delete_user(current_user.id)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User does not exist.")

        # (4b) perform closing operations
        send_mail("Notification: Account deleted", f"You have deleted your account {user.email}.", [user.email])
        logout_user()

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    mail_form.process()
    password_form.process()
    deletion_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('account/edit.html', mail_form=mail_form,
                                 password_form=password_form, deletion_form=deletion_form)
