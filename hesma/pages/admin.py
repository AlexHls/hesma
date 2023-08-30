from django.contrib import admin

from hesma.pages.models import FAQ, FAQTopic

admin.site.register(FAQTopic)
admin.site.register(FAQ)
