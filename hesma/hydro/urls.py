from django.urls import path

from hesma.hydro.views import (
    hydro_download_info,
    hydro_download_readme,
    hydro_edit,
    hydro_landing_view,
    hydro_model_view,
    hydro_upload_view,
)

app_name = "hydro"
urlpatterns = [
    path("", view=hydro_landing_view, name="hydro_landing"),
    path("<int:hydrosimulation_id>/", view=hydro_model_view, name="detail"),
    path("upload/", view=hydro_upload_view, name="hydro_upload"),
    path("<int:hydrosimulation_id>/download", view=hydro_download_info, name="hydro_download_info"),
    path("<int:hydrosimulation_id>/download_readme", view=hydro_download_readme, name="hydro_download_readme"),
    path("<int:hydrosimulation_id>/edit", view=hydro_edit, name="hydro_edit"),
]
