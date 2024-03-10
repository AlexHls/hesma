import json
import mimetypes
import os
from io import StringIO
from wsgiref.util import FileWrapper

from django.http import Http404, HttpResponse, StreamingHttpResponse
from django.shortcuts import render
from django.utils import timezone

from config.settings.base import STREAMING_CHUNK_SIZE
from hesma.hydro.forms import HydroSimulation1DModelFileForm, HydroSimulationForm
from hesma.hydro.models import HydroSimulation, HydroSimulation1DModelFile
from hesma.utils.zip_generator import ZipFileGenerator


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

    json_data = {
        "id": hydrosimulation_id,
        "name": obj.name,
        "description": obj.description,
        "date": obj.date.strftime("%Y-%m-%d %H:%M:%S"),
        "user": obj.user.username,
    }

    hydro1d_files = obj.hydrosimulation1dmodelfile_set.all()
    if hydro1d_files:
        json_data["hydro1d_files"] = [
            {
                "id": file.id,
                "name": file.name,
                "date": file.date.strftime("%Y-%m-%d %H:%M:%S"),
                "description": file.description,
            }
            for file in hydro1d_files
        ]
        selected_files = [file.file.path for file in hydro1d_files]
    else:
        selected_files = []

    selected_files.append(obj.readme.path)

    json_file = StringIO()
    json.dump(json_data, json_file)

    zip_generator = ZipFileGenerator(
        selected_files=selected_files,
        info_json=json_file,
        file_name=f"{obj.name}.zip",
    )
    return zip_generator.get_response()


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


def hydro_hydro1d_interactive_plot(request, hydrosimulation_id, hydrosimulation1dmodelfile_id):
    model = HydroSimulation.objects.get(id=hydrosimulation_id)
    file = model.hydrosimulation1dmodelfile_set.get(id=hydrosimulation1dmodelfile_id)
    return render(request, "hydro/hydro1d_interactive_plot.html", {"model": model, "file": file})


def hydro_download_hydro1d(request, hydrosimulation_id, hydrosimulation1dmodelfile_id):
    file = HydroSimulation1DModelFile.objects.get(id=hydrosimulation1dmodelfile_id)
    filename = os.path.basename(file.file.path)
    filepath = file.file.path

    response = StreamingHttpResponse(
        FileWrapper(open(filepath, "rb"), STREAMING_CHUNK_SIZE),
        content_type=mimetypes.guess_type(filepath)[0],
    )
    response["Content-Length"] = os.path.getsize(filepath)
    response["Content-Disposition"] = f"attachment; filename={filename}"

    return response
