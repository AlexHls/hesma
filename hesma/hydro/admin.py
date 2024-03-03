from django.contrib import admin

from hesma.hydro.models import HydroSimulation, HydroSimulation1DModelFile

admin.site.register(HydroSimulation)
admin.site.register(HydroSimulation1DModelFile)
