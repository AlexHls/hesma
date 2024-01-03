from django.urls import path

from hesma.meta import views

app_name = "meta"
urlpatterns = [
    path("doi/create/", views.DOICreateViewHydro.as_view(), name="doi_create"),
]
