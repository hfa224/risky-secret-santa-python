"""Encapsulates send email functionality"""

from flask import flash, current_app
from flask_mail import Message, Mail

mail = Mail(current_app)

def send_email(recipient_email, msg):
    """
    Method that sends an email using flask_mail to recipient email
    """
    recipient = recipient_email
    msg = Message("Twilio SendGrid Test Email", recipients=[recipient])
    mail.send(msg)
    flash(f"A test message was sent to {recipient}.")
