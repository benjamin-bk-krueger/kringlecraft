import flask
from flask_login import (login_user, logout_user, login_required)  # to manage user sessions

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


# Show index page
@blueprint.route('/')
def index():
    return flask.render_template('home/index.html')


# Show user log-in page
@blueprint.route('/login', methods=['GET'])
def login_get():
    from kringlecraft.viewmodels.home_forms import LoginForm

    # initialize form data
    login_form = LoginForm()
    login_form.process()

    return flask.render_template('home/login.html', login_form=login_form)


@blueprint.route('/login', methods=['POST'])
def login_post():
    from kringlecraft.viewmodels.home_forms import LoginForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    login_form = LoginForm()
    login_form.escape_fields()

    # check valid student account and password match
    if login_form.validate_on_submit():
        user = user_services.login_user(login_form.email.data, login_form.password.data)
        if not user:
            print(f"Login Failure for user {login_form.email.data}")

            return flask.redirect(flask.url_for('home.login_get'))
        else:
            login_user(user, remember=login_form.remember.data)
            print(f"Login Successful for user {login_form.email.data}")

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


# Show privacy policy
@blueprint.route('/privacy')
def privacy():
    return flask.render_template('home/privacy.html')


# Show information about all major releases
@blueprint.route('/release')
def release():
    return flask.render_template('home/release.html')
