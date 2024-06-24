from flask import current_app
from flask_mail import Message  # to send mails


# Send an e-mail to admin user
def send_admin_mail(header: str, body: str):
    if current_app.config.get("app.mail_enable") == "true":
        print(f"INFO: Sending mail to admin: {body}")
        msg = Message(header, sender=current_app.config.get("app.mail_sender"),
                      recipients=[current_app.config.get("app.mail_admin")])
        msg.body = body
        current_app.config.get("mail.send")(msg)
    else:
        print("INFO: Sending mail disabled")
        print(f"MAIL Header: {header}")
        print(f"MAIL Sender: {current_app.config.get('app.mail_sender')}")
        print(f"MAIL Recipients: {[current_app.config.get('app.mail_admin')]}")
        print(f"MAIL Body: {body}")


# Send an e-mail to any user
def send_mail(header: str, body: str, recipients: list):
    if current_app.config.get("app.mail_enable") == "true":
        print(f"INFO: Sending mail to users {recipients}: {body}")
        msg = Message(header, sender=current_app.config.get("app.mail_sender"),
                      recipients=recipients)
        msg.body = body
        current_app.config.get("mail.send")(msg)
    else:
        print("INFO: Sending mail disabled")
        print(f"Mail Header: {header}")
        print(f"Mail Sender: {current_app.config.get('app.mail_sender')}")
        print(f"Mail recipients: {recipients}")
        print(f"Mail Body: {body}")
