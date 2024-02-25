from captcha.fields import CaptchaField
from django.forms import ModelForm

from hesma.pages.models import ContactMessage


class ContactMessageForm(ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = ContactMessage
        fields = "__all__"
        exclude = ["date"]
