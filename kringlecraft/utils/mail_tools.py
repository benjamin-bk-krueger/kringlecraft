from flask import current_app
from flask_mail import Message  # to send mails


# Send an e-mail to admin user
def send_admin_mail(mail_header: str, mail_body: str):
    """
    :param mail_header: the subject/header of the email
    :param mail_body: the content/body of the email
    :return: None

    This method sends an email to the admin. It requires a mail_header and mail_body as parameters. If the mail sending feature is enabled in the configuration (app.mail_enable set to "true"), the email will be sent using the current_app's mail configuration. The mail_header will be used as the subject of the email, and the mail_body as the email message content. The recipient of the email will be specified by the configuration value app.mail_admin.

    If the mail sending feature is disabled, the method will print the details of the email that would have been sent, including the mail_header, mail_sender, recipients, and mail_body.
    """
    if current_app.config.get("app.mail_enable") == "true":
        print(f"Sending mail to admin: {mail_body}")
        msg = Message(mail_header, sender=current_app.config.get("app.mail_sender"),
                      recipients=[current_app.config.get("app.mail_admin")])
        msg.body = mail_body
        current_app.config.get("mail.send")(msg)
    else:
        print("Sending mail disabled")
        print(f"Mail Header: {mail_header}")
        print(f"Mail Sender: {current_app.config.get('app.mail_sender')}")
        print(f"Mail recipients: {[current_app.config.get('app.mail_admin')]}")
        print(f"Mail Body: {mail_body}")


# Send an e-mail to any user
def send_mail(mail_header: str, mail_body: str, recipients: list):
    """
    Sends an email with the given mail header, mail body, and recipients.

    :param mail_header: The header of the email.
    :param mail_body: The body of the email.
    :param recipients: A list of email addresses of the recipients.
    :return: None

    """
    if current_app.config.get("app.mail_enable") == "true":
        print(f"Sending mail to users {recipients}: {mail_body}")
        msg = Message(mail_header, sender=current_app.config.get("app.mail_sender"),
                      recipients=recipients)
        msg.body = mail_body
        current_app.config.get("mail.send")(msg)
    else:
        print("Sending mail disabled")
        print(f"Mail Header: {mail_header}")
        print(f"Mail Sender: {current_app.config.get('app.mail_sender')}")
        print(f"Mail recipients: {recipients}")
        print(f"Mail Body: {mail_body}")
