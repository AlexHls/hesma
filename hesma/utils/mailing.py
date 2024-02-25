from smtplib import SMTPException

from django.conf import settings


def send_contact_email(contact):
    # Unpack the contact message
    if settings.DEBUG:
        print("Sending contact email")
        print(f"Subject: {contact.subject}\n\nFrom: {contact.email}\n\nMessage: {contact.message}")
    else:
        try:
            mail = contact.create_email_message()
            mail.send(fail_silently=False)
        except SMTPException:
            raise SMTPException("Failed to send email")
    return
