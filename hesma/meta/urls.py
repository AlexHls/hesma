from django.urls import path

from hesma.meta import views

app_name = "meta"
urlpatterns = [
    path(
        "doi/create/hydro_upload",
        views.DOICreateViewHydro.as_view(),
        name="doi_create_hydro",
    ),
    path(
        "doi/create/hydro_edit",
        views.DOICreateViewHydroEdit.as_view(),
        name="doi_create_hydro_edit",
    ),
]
