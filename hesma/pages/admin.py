from django.contrib import admin

from hesma.pages.models import FAQ, ContactMessage, FAQTopic, News

admin.site.register(FAQTopic)
admin.site.register(FAQ)
admin.site.register(News)
admin.site.register(ContactMessage)
