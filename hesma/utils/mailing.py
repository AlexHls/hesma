from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage


def send_contact_email(contact):
    # Unpack the contact message
    if settings.DEBUG:
        print("Sending contact email")
        print(f"Subject: {contact.subject}\n\nFrom: {contact.email}\n\nMessage: {contact.message}")
    else:
        try:
            mail = create_email_message_from_contact(contact)
            mail.send(fail_silently=False)
        except SMTPException:
            raise SMTPException("Failed to send email")
    return


def create_email_message_from_contact(contact):
    return EmailMessage(
        subject=f"Contact message from {contact.email}",
        body=f"Subject: {contact.subject}\n\nFrom: {contact.email}\n\nMessage: {contact.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.CONTACT_EMAILS,
    )
