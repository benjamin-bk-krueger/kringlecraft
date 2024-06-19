import flask
from flask_login import (login_user, logout_user, login_required)  # to manage user sessions
from kringlecraft.utils.mail_tools import send_admin_mail

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


# Displays a form to send a message to the site admin - implements a simple captcha as well
@blueprint.route('/contact', methods=['GET'])
def contact_get():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import ContactForm
    from kringlecraft.utils.misc_tools import create_captcha

    # initialize form data
    check_captcha = create_captcha()
    contact_form = ContactForm(check_captcha["res"])
    contact_form.process()

    # show rendered page
    return flask.render_template('home/contact.html', contact_form=contact_form, check_captcha=check_captcha)


@blueprint.route('/contact', methods=['POST'])
def contact_post():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import ContactForm
    from kringlecraft.utils.misc_tools import create_captcha

    # initialize form data
    contact_form = ContactForm()

    # check valid contact data
    if contact_form.validate_on_submit():
        send_admin_mail(f"{contact_form.contact_content} - {contact_form.email_content}", f"{contact_form.message_content}")

        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        contact_form.set_field_defaults()
        check_captcha = create_captcha()
        contact_form.set_captcha(check_captcha["res"])
        contact_form.process()

        # show page again and print possible errors in form
        return flask.render_template('home/contact.html', contact_form=contact_form, check_captcha=check_captcha)


# Show error page  - for all "hard" crashes a mail is sent to the site admin
@blueprint.route('/error')
def error():
    return flask.render_template('home/error.html')


# Show index page
@blueprint.route('/')
def index():
    return flask.render_template('home/index.html')


# Show user log-in page
@blueprint.route('/login', methods=['GET'])
def login_get():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import LoginForm

    # initialize form data
    login_form = LoginForm()
    login_form.process()

    # show rendered page
    return flask.render_template('home/login.html', login_form=login_form)


@blueprint.route('/login', methods=['POST'])
def login_post():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import LoginForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    login_form = LoginForm()

    # check valid student account and password match
    if login_form.validate_on_submit():
        user = user_services.login_user(login_form.email_content, login_form.password_content)
        if not user:
            return flask.redirect(flask.url_for('home.login_get'))
        else:
            login_user(user, remember=login_form.remember_content)

            return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        login_form.set_field_defaults()
        login_form.process()

        # show page again and print possible errors in form
        return flask.render_template('home/login.html', login_form=login_form)


# Log out user and return to the site index afterward
@blueprint.route('/logout')
def logout():
    logout_user()

    return flask.redirect(flask.url_for('home.index'))


# Force user log-in and return to the site index afterward
@blueprint.route('/logged')
@login_required
def logged():
    return flask.redirect(flask.url_for('home.index'))


# Show user password reset page
@blueprint.route('/password', methods=['GET'])
def password_get():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import PasswordForm

    # initialize form data
    password_form = PasswordForm()
    password_form.process()

    # show rendered page
    return flask.render_template('home/password.html', password_form=password_form)


@blueprint.route('/password', methods=['POST'])
def password_post():
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import PasswordForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    password_form = PasswordForm()

    # in case of password reset request and enabled e-mail account
    if password_form.validate_on_submit():
        user_services.prepare_user(password_form.email_content, flask.current_app.config["app.www_server"])

        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        password_form.set_field_defaults()
        password_form.process()

        # show page again and print possible errors in form
        return flask.render_template('home/password.html', password_form=password_form)


# Show user password reset page
@blueprint.route('/reset/<string:random_hash>', methods=['GET'])
def reset_get(random_hash):
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import ResetForm

    # initialize form data
    reset_form = ResetForm()
    reset_form.process()

    # show rendered page
    return flask.render_template('home/reset.html', reset_form=reset_form, random_hash=random_hash)


@blueprint.route('/reset/<string:random_hash>', methods=['POST'])
def reset_post(random_hash):
    # import forms and utilities
    from kringlecraft.viewmodels.home_forms import ResetForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    reset_form = ResetForm()

    # in case of password reset request follow-up
    if reset_form.validate_on_submit() and len(random_hash) > 30:
        user_services.reset_user(random_hash, reset_form.password_content)

        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        reset_form.process()

        # show page again and print possible errors in form
        return flask.render_template('home/reset.html', reset_form=reset_form, random_hash=random_hash)


# Show privacy policy
@blueprint.route('/privacy')
def privacy():
    return flask.render_template('home/privacy.html')


# Show information about all major releases
@blueprint.route('/release')
def release():
    return flask.render_template('home/release.html')
