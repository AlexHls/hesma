from django.urls import path

from hesma.tracer.views import (
    tracer_download_info,
    tracer_download_readme,
    tracer_edit,
    tracer_landing_view,
    tracer_model_view,
    tracer_upload_view,
)

app_name = "tracer"
urlpatterns = [
    path("", view=tracer_landing_view, name="tracer_landing"),
    path("<int:tracersimulation_id>/", view=tracer_model_view, name="detail"),
    path("upload/", view=tracer_upload_view, name="tracer_upload"),
    path("<int:tracersimulation_id>/download", view=tracer_download_info, name="tracer_download_info"),
    path("<int:tracersimulation_id>/download_readme", view=tracer_download_readme, name="tracer_download_readme"),
    path("<int:tracersimulation_id>/edit", view=tracer_edit, name="tracer_edit"),
]
