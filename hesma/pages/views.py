from django.shortcuts import render

from hesma.hydro.models import HydroSimulation
from hesma.pages.models import FAQ, FAQTopic
from hesma.rt.models import RTSimulation
from hesma.tracer.models import TracerSimulation


def faq_view(request):
    # Render all FAQ topics and questions
    topics = FAQTopic.objects.all().order_by("order")
    for topic in topics:
        topic.questions = FAQ.objects.filter(topic=topic).order_by("order")

    return render(request, "pages/faq.html", {"topics": topics})


def mymodel_view(request):
    # Get all models that are published by the current user
    hydro_models = HydroSimulation.objects.filter(user=request.user)
    rt_models = RTSimulation.objects.filter(user=request.user)
    tracer_models = TracerSimulation.objects.filter(user=request.user)

    context = {
        "hydro_models": hydro_models,
        "rt_models": rt_models,
        "tracer_models": tracer_models,
    }

    return render(request, "pages/mymodels.html", context)
