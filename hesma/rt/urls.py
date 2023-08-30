from django.urls import path

from hesma.rt.views import (
    rt_download_info,
    rt_download_readme,
    rt_edit,
    rt_landing_view,
    rt_model_view,
    rt_upload_view,
)

app_name = "rt"
urlpatterns = [
    path("", view=rt_landing_view, name="rt_landing"),
    path("<int:rtsimulation_id>/", view=rt_model_view, name="detail"),
    path("upload/", view=rt_upload_view, name="rt_upload"),
    path("<int:rtsimulation_id>/download", view=rt_download_info, name="rt_download_info"),
    path("<int:rtsimulation_id>/download_readme", view=rt_download_readme, name="rt_download_readme"),
    path("<int:rtsimulation_id>/edit", view=rt_edit, name="rt_edit"),
]
