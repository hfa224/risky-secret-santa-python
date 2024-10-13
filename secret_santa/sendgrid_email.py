"""
Method for sending email via sendgrid API
"""
import os
import sendgrid
from sendgrid.helpers.mail import Email, To, Content, Mail
from flask import flash

MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")


def send_email(recipient_email, msg):
    """
    Method that sends an email using sendgrid API to recipient email
    """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get("SENDGRID_API_KEY"))
    from_email = Email(MAIL_DEFAULT_SENDER)
    to_email = To(recipient_email)
    subject = "Secret Santa Info"
    content = Content("text/plain", msg)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

    flash(f"A test message was sent to {recipient_email}.")
