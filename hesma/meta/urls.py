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
    path(
        "doi/create/rt_upload",
        views.DOICreateViewRT.as_view(),
        name="doi_create_rt",
    ),
    path(
        "doi/create/rt_edit",
        views.DOICreateViewRTEdit.as_view(),
        name="doi_create_rt_edit",
    ),
    path(
        "doi/create/tracer_upload",
        views.DOICreateViewTracer.as_view(),
        name="doi_create_tracer",
    ),
    path(
        "doi/create/tracer_edit",
        views.DOICreateViewTracerEdit.as_view(),
        name="doi_create_tracer_edit",
    ),
]
