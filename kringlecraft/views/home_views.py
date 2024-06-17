import flask

blueprint = flask.Blueprint('home', __name__, template_folder='templates')


# Show index page
@blueprint.route('/')
def index():
    return flask.render_template('home/index.html')


# Show privacy policy
@blueprint.route('/privacy')
def privacy():
    return flask.render_template('home/privacy.html')


# Show information about all major releases
@blueprint.route('/release')
def release():
    return flask.render_template('home/release.html')
