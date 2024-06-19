import flask

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
