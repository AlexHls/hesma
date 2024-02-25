from django.urls import path

from hesma.pages.views import contact_view, faq_view, mymodel_view

app_name = "pages"
urlpatterns = [
    path("faq/", faq_view, name="faq"),
    path("mymodels/", mymodel_view, name="mymodels"),
    path("contact/", contact_view, name="contact"),
]
