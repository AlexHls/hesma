from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from hesma.rt.views import (
    rt_download_info,
    rt_download_lightcurve,
    rt_download_readme,
    rt_download_spectrum,
    rt_edit,
    rt_landing_view,
    rt_lightcurve_interactive_plot,
    rt_model_view,
    rt_spectrum_interactive_plot,
    rt_upload_lightcurve,
    rt_upload_spectrum,
    rt_upload_view,
)

app_name = "rt"
urlpatterns = [
    path("", view=rt_landing_view, name="rt_landing"),
    path("<int:rtsimulation_id>/", view=rt_model_view, name="detail"),
    path("upload/", view=rt_upload_view, name="rt_upload"),
    path("<int:rtsimulation_id>/download", view=rt_download_info, name="rt_download_info"),
    path(
        "<int:rtsimulation_id>/download_readme",
        view=rt_download_readme,
        name="rt_download_readme",
    ),
    path("<int:rtsimulation_id>/edit", view=rt_edit, name="rt_edit"),
    path(
        "<int:rtsimulation_id>/upload_lightcurve",
        view=rt_upload_lightcurve,
        name="rt_upload_lightcurve",
    ),
    path(
        "<int:rtsimulation_id>/upload_spectrum",
        view=rt_upload_spectrum,
        name="rt_upload_spectrum",
    ),
    path(
        "<int:rtsimulation_id>/lc/<int:rtsimulationlightcurvefile_id>/interactive_plot",
        view=rt_lightcurve_interactive_plot,
        name="rt_interactive_lightcurve",
    ),
    path(
        "<int:rtsimulation_id>/spec/<int:rtsimulationspectrumfile_id>/interactive_plot",
        view=rt_spectrum_interactive_plot,
        name="rt_interactive_spectrum",
    ),
    path(
        "<int:rtsimulation_id>/lc/<int:rtsimulationlightcurvefile_id>/download",
        view=rt_download_lightcurve,
        name="rt_download_lightcurve",
    ),
    path(
        "<int:rtsimulation_id>/spec/<int:rtsimulationspectrumfile_id>/download",
        view=rt_download_spectrum,
        name="rt_download_spectrum",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
