import json
import mimetypes
import os
import zipfile
from io import BytesIO, StringIO

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hesma.hydro.forms import HydroSimulation1DModelFileForm, HydroSimulationForm
from hesma.hydro.models import HydroSimulation


def hydro_landing_view(request):
    latest_model_list = HydroSimulation.objects.order_by("-date")[:5]
    return render(request, "hydro/landing.html", {"latest_model_list": latest_model_list})


def hydro_model_view(request, hydrosimulation_id):
    try:
        model = HydroSimulation.objects.get(pk=hydrosimulation_id)
    except HydroSimulation.DoesNotExist:
        raise Http404("Hydro simulation does not exist")
    return render(request, "hydro/detail.html", {"model": model})


def hydro_upload_view(request):
    if request.method == "POST":
        form = HydroSimulationForm(request.POST, request.FILES)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.user = request.user
            sim.date = timezone.now()
            sim.save()
            return render(request, "hydro/upload_success.html")
    else:
        form = HydroSimulationForm()
    return render(request, "hydro/upload.html", {"form": form})


def hydro_download_readme(request, hydrosimulation_id):
    obj = HydroSimulation.objects.get(id=hydrosimulation_id)
    filename = os.path.basename(obj.readme.path)
    filepath = obj.readme.path

    path = open(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def hydro_download_info(request, hydrosimulation_id):
    obj = HydroSimulation.objects.get(id=hydrosimulation_id)

    zip_filename = "%s.zip" % obj.name

    # Write object data to json file
    json_data = {
        "id": hydrosimulation_id,
        "name": obj.name,
        "description": obj.description,
        "date": obj.date.strftime("%Y-%m-%d %H:%M:%S"),
        "user": obj.user.username,
    }
    json_file = StringIO()
    json.dump(json_data, json_file)

    # Create zip file
    s = BytesIO()
    zf = zipfile.ZipFile(s, "w")

    # Write files to zip
    zf.writestr("info.json", bytes(json_file.getvalue(), encoding="utf-8"))
    if obj.readme:
        readme_file = obj.readme.path
        zf.write(readme_file, os.path.basename(readme_file))

    # Must close zip for all contents to be written
    zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
    response = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    # ..and correct content-disposition
    response["Content-Disposition"] = "attachment; filename=%s" % zip_filename

    return response


def hydro_edit(request, hydrosimulation_id):
    model = HydroSimulation.objects.get(id=hydrosimulation_id)
    if request.method == "POST":
        form = HydroSimulationForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.save()
            return render(request, "hydro/detail.html", {"model": model})
    else:
        form = HydroSimulationForm(instance=model)
    context = {"form": form, "model": model}
    return render(request, "hydro/edit.html", context)


def hydro_upload_hydro1d(request, hydrosimulation_id):
    model = HydroSimulation.objects.get(id=hydrosimulation_id)
    if request.method == "POST":
        form = HydroSimulation1DModelFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.date = timezone.now()
            file.hydro_simulation = model
            if form.cleaned_data["generate_interactive_plot"]:
                file.interactive_plot = file.get_plot_json()
            file.save()
            return render(request, "hydro/upload_success.html")
    else:
        form = HydroSimulation1DModelFileForm()
    return render(request, "hydro/upload_hydro1d.html", {"form": form})
