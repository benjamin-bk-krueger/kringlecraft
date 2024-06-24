import flask
from flask_login import (login_user, logout_user, login_required)  # to manage user sessions

from kringlecraft.utils.mail_tools import (send_admin_mail, send_mail)

blueprint = flask.Blueprint('home', __name__, template_folder='templates')

''' 
All route follow the same flow:
# (1) import forms and utilities
# (2) initialize form data
# (3) check valid form data
# (4a) perform operations
# (4b) perform closing operations
# (5) preset form with existing data
# (6a) show rendered page
# (6b) redirect to new page after successful operation
# (6c) show rendered page with possible error messages
# (6d) redirect to new page after errors occurred
# (6e) show dedicated error page
'''


# Displays a form to send a message to the site admin - implements a simple captcha as well
@blueprint.route('/contact', methods=['GET'])
def contact():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import ContactForm
    from kringlecraft.utils.misc_tools import create_captcha

    # (2) initialize form data
    check_captcha = create_captcha()
    contact_form = ContactForm(check_captcha["res"])
    contact_form.process()

    # (6a) show rendered page
    return flask.render_template('home/contact.html', contact_form=contact_form, check_captcha=check_captcha)


@blueprint.route('/contact', methods=['POST'])
def contact_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import ContactForm
    from kringlecraft.utils.misc_tools import create_captcha

    # (2) initialize form data
    contact_form = ContactForm()

    # (3) check valid form data
    if contact_form.validate_on_submit():
        # (4a) perform operations
        send_admin_mail(f"{contact_form.name_content} - {contact_form.email_content}",
                        f"{contact_form.message_content}")

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    contact_form.set_field_defaults()
    check_captcha = create_captcha()
    contact_form.set_captcha(check_captcha["res"])
    contact_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('home/contact.html', contact_form=contact_form, check_captcha=check_captcha)


# Show error page  - for all "hard" crashes a mail is sent to the site admin
@blueprint.route('/error', methods=['GET'])
def error():
    # (6a) show rendered page
    return flask.render_template('home/error.html')


# Show index page
@blueprint.route('/', methods=['GET'])
def index():
    # (6a) show rendered page
    return flask.render_template('home/index.html')


# Show user log-in page
@blueprint.route('/login', methods=['GET'])
def login():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import LoginForm

    # (2) initialize form data
    login_form = LoginForm()
    login_form.process()

    # (6a) show rendered page
    return flask.render_template('home/login.html', login_form=login_form)


@blueprint.route('/login', methods=['POST'])
def login_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import LoginForm
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    login_form = LoginForm()

    # (3) check valid form data
    if login_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.login_user(login_form.email_content, login_form.password_content)

        if not user:
            # (6d) redirect to new page after errors occurred
            return flask.redirect(flask.url_for('home.login'))

        # (4b) perform closing operations
        login_user(user, remember=login_form.remember_content)

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    login_form.set_field_defaults()
    login_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('home/login.html', login_form=login_form)


# Log out user and return to the site index afterward
@blueprint.route('/logout', methods=['GET'])
def logout():
    # (4a) perform operations
    logout_user()

    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('home.index'))


# Force user log-in and return to the site index afterward
@blueprint.route('/logged', methods=['GET'])
@login_required
def logged():
    # (6b) redirect to new page after successful operation
    return flask.redirect(flask.url_for('home.index'))


# Show user password reset page
@blueprint.route('/password', methods=['GET'])
def password():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import PasswordForm

    # (2) initialize form data
    password_form = PasswordForm()
    password_form.process()

    # (6a) show rendered page
    return flask.render_template('home/password.html', password_form=password_form)


@blueprint.route('/password', methods=['POST'])
def password_post():
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import PasswordForm
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    password_form = PasswordForm()

    # (3) check valid form data
    if password_form.validate_on_submit():
        # (4a) perform operations
        user = user_services.prepare_user(password_form.email_content)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User does not exist.")

        # (4b) perform closing operations
        send_mail("Password Reset Link",
                  f"Reset your password here: {flask.current_app.config['app.www_server']}/reset/"
                  f"{user.reset_password}", [user.email])

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    password_form.set_field_defaults()
    password_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('home/password.html', password_form=password_form)


# Show user password reset page
@blueprint.route('/reset/<string:random_hash>', methods=['GET'])
def reset(random_hash):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import ResetForm

    # (2) initialize form data
    reset_form = ResetForm()
    reset_form.process()

    # (6a) show rendered page
    return flask.render_template('home/reset.html', reset_form=reset_form, random_hash=random_hash)


@blueprint.route('/reset/<string:random_hash>', methods=['POST'])
def reset_post(random_hash):
    # (1) import forms and utilities
    from kringlecraft.viewmodels.home_forms import ResetForm
    import kringlecraft.services.user_services as user_services

    # (2) initialize form data
    reset_form = ResetForm()

    # (3) check valid form data
    if reset_form.validate_on_submit() and len(random_hash) > 30:
        # (4a) perform operations
        user = user_services.reset_user(random_hash, reset_form.password_content)

        if not user:
            # (6e) show dedicated error page
            return flask.render_template('home/error.html', error_message="User does not exist.")

        # (4b) perform closing operations
        send_mail(f"{user.name} - Password Reset", "Your password has been reset.", [user.email])

        # (6b) redirect to new page after successful operation
        return flask.redirect(flask.url_for('home.index'))

    # (5) preset form with existing data
    reset_form.process()

    # (6c) show rendered page with possible error messages
    return flask.render_template('home/reset.html', reset_form=reset_form, random_hash=random_hash)


# Show privacy policy
@blueprint.route('/privacy', methods=['GET'])
def privacy():
    # (6a) show rendered page
    return flask.render_template('home/privacy.html')


# Show information about all major releases
@blueprint.route('/release', methods=['GET'])
def release():
    # (6a) show rendered page
    return flask.render_template('home/release.html')
