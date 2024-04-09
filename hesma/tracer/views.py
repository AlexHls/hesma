import json
import mimetypes
import os
import zipfile
from io import BytesIO, StringIO

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hesma.tracer.forms import TracerSimulationForm
from hesma.tracer.models import TracerSimulation


def tracer_landing_view(request):
    latest_model_list = TracerSimulation.objects.order_by("-date")[:5]
    model_list = TracerSimulation.objects.all().order_by("name")
    return render(
        request,
        "tracer/landing.html",
        {"latest_model_list": latest_model_list, "model_list": model_list},
    )


def tracer_model_view(request, tracersimulation_id):
    try:
        model = TracerSimulation.objects.get(pk=tracersimulation_id)
    except TracerSimulation.DoesNotExist:
        raise Http404("Tracer simulation does not exist")
    return render(request, "tracer/detail.html", {"model": model})


def tracer_upload_view(request):
    if request.method == "POST":
        form = TracerSimulationForm(request.POST, request.FILES)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.user = request.user
            sim.date = timezone.now()
            sim.save()
            return render(request, "tracer/upload_success.html")
    else:
        form = TracerSimulationForm()
    return render(request, "tracer/upload.html", {"form": form})


def tracer_download_readme(request, tracersimulation_id):
    obj = TracerSimulation.objects.get(id=tracersimulation_id)
    filename = os.path.basename(obj.readme.path)
    filepath = obj.readme.path

    path = open(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def tracer_download_info(request, tracersimulation_id):
    obj = TracerSimulation.objects.get(id=tracersimulation_id)

    zip_filename = "%s.zip" % obj.name

    # Write object data to json file
    json_data = {
        "id": tracersimulation_id,
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


def tracer_edit(request, tracersimulation_id):
    model = TracerSimulation.objects.get(id=tracersimulation_id)
    if request.method == "POST":
        form = TracerSimulationForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.save()
            return render(request, "tracer/detail.html", {"model": model})
    else:
        form = TracerSimulationForm(instance=model)
    context = {"form": form, "model": model}
    return render(request, "tracer/edit.html", context)
