import flask
from kringlecraft.utils.mail_tools import (send_admin_mail, send_mail)

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
        user = user_services.create_user(account_form.user_content, account_form.email_content, account_form.password_content)
        if user:
            send_admin_mail(f"{account_form.user_content} - Approval required", "A new user has registered, please approve registration.")
            send_mail(f"{account_form.user_content} - Registration pending", "Your registration needs to be approved. This should not take too long.", [account_form.email_content])

        return flask.redirect(flask.url_for('home.index'))
    else:
        # preset form with existing data
        account_form.set_field_defaults()
        account_form.process()

        # show page again and print possible errors in form
        return flask.render_template('account/create.html', account_form=account_form)
