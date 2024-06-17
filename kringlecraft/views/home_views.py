import flask
from markupsafe import escape  # to safely escape form data

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

    # show page again and print possible errors in form
    return flask.render_template('home/login.html', login_form=login_form)


@blueprint.route('/login', methods=['POST'])
def login_post():
    from kringlecraft.viewmodels.home_forms import LoginForm
    import kringlecraft.services.user_services as user_services

    # initialize form data
    login_form = LoginForm()

    # in case of login request
    if login_form.validate_on_submit():
        # read form and find matching student for login request
        user_mail = escape(login_form.email.data)
        user_password = login_form.password.data
        user_remember = bool(escape(login_form.remember.data))
        user = user_services.login_user(user_mail, user_password)

        # check valid student account and password match
        if not user:
            print("Login Failure")

            # redirect to login page after unsuccessful login
            return flask.redirect(flask.url_for('home.index'))
        else:
            print("Login Successful")

            # redirect to index page after successful login
            return flask.redirect(flask.url_for('home.index'))


# Show privacy policy
@blueprint.route('/privacy')
def privacy():
    return flask.render_template('home/privacy.html')


# Show information about all major releases
@blueprint.route('/release')
def release():
    return flask.render_template('home/release.html')
