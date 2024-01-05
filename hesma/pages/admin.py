from django.contrib import admin

from hesma.pages.models import FAQ, FAQTopic, News

admin.site.register(FAQTopic)
admin.site.register(FAQ)
admin.site.register(News)
