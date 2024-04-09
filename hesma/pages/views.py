from smtplib import SMTPException

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from hesma.hydro.models import HydroSimulation
from hesma.pages.forms import ContactMessageForm
from hesma.pages.models import FAQ, FAQTopic, News
from hesma.rt.models import RTSimulation
from hesma.tracer.models import TracerSimulation
from hesma.utils.mailing import send_contact_email


def home_view(request):
    news = News.objects.filter(sticky=False).order_by("-date")[:5]
    sticky_news = News.objects.filter(sticky=True)
    return render(
        request,
        "pages/home.html",
        {"news_list": news, "sticky_news": sticky_news},
    )


def faq_view(request):
    # Render all FAQ topics and questions
    topics = FAQTopic.objects.all().order_by("order")
    for topic in topics:
        topic.questions = FAQ.objects.filter(topic=topic).order_by("order")

    return render(request, "pages/faq.html", {"topics": topics})


def mymodel_view(request):
    try:
        if request.user.is_authenticated:
            # Get all models that are published by the current user
            hydro_models = HydroSimulation.objects.filter(user=request.user)
            rt_models = RTSimulation.objects.filter(user=request.user)
            tracer_models = TracerSimulation.objects.filter(user=request.user)
            context = {
                "hydro_models": hydro_models,
                "rt_models": rt_models,
                "tracer_models": tracer_models,
            }
        else:
            context = {
                "hydro_models": [],
                "rt_models": [],
                "tracer_models": [],
            }
    except AttributeError:
        # Not sure if 403 is the right status code here
        return HttpResponse(status=403)
    return render(request, "pages/mymodels.html", context)


def contact_view(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
            contact = form.save(commit=False)
            contact.date = timezone.now()
            try:
                send_contact_email(contact)
            except SMTPException:
                return HttpResponse(status=500, content="Failed to send email. Please try again later")
            # We only save the contact message if the email was sent successfully
            contact.save()

            return render(request, "pages/contact_success.html")
    else:
        form = ContactMessageForm()
    return render(request, "pages/contact.html", {"form": form})
