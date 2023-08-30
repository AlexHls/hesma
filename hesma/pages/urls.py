from django.urls import path

from hesma.pages.views import faq_view, mymodel_view

app_name = "pages"
urlpatterns = [
    path("faq/", faq_view, name="faq"),
    path("mymodels/", mymodel_view, name="mymodels"),
]
