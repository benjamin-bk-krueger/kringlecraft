from flask import current_app
from flask_mail import Message  # to send mails


# Send an e-mail to admin user
def send_admin_mail(mail_header: str, mail_body: str):
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
