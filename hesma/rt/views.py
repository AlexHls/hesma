import json
import mimetypes
import os
import zipfile
from io import BytesIO, StringIO

from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hesma.rt.forms import RTSimulationForm
from hesma.rt.models import RTSimulation


def rt_landing_view(request):
    latest_model_list = RTSimulation.objects.order_by("-date")[:5]
    return render(request, "rt/landing.html", {"latest_model_list": latest_model_list})


def rt_model_view(request, rtsimulation_id):
    try:
        model = RTSimulation.objects.get(pk=rtsimulation_id)
    except RTSimulation.DoesNotExist:
        raise Http404("RT simulation does not exist")
    return render(request, "rt/detail.html", {"model": model})


def rt_upload_view(request):
    if request.method == "POST":
        form = RTSimulationForm(request.POST, request.FILES)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.user = request.user
            sim.date = timezone.now()
            sim.save()
            return render(request, "rt/upload_success.html")
    else:
        form = RTSimulationForm()
    return render(request, "rt/upload.html", {"form": form})


def rt_download_readme(request, rtsimulation_id):
    obj = RTSimulation.objects.get(id=rtsimulation_id)
    filename = os.path.basename(obj.readme.path)
    filepath = obj.readme.path

    path = open(filepath)
    mime_type, _ = mimetypes.guess_type(filepath)
    response = HttpResponse(path, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % filename

    return response


def rt_download_info(request, rtsimulation_id):
    obj = RTSimulation.objects.get(id=rtsimulation_id)

    zip_filename = "%s.zip" % obj.name

    # Write object data to json file
    json_data = {
        "id": rtsimulation_id,
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


def rt_edit(request, rtsimulation_id):
    model = RTSimulation.objects.get(id=rtsimulation_id)
    if request.method == "POST":
        form = RTSimulationForm(request.POST, request.FILES, instance=model)
        if form.is_valid():
            sim = form.save(commit=False)
            sim.save()
            return render(request, "rt/detail.html", {"model": model})
    else:
        form = RTSimulationForm(instance=model)
    context = {"form": form, "model": model}
    return render(request, "rt/edit.html", context)
