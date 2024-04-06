from django.contrib import admin

from hesma.rt.models import RTSimulation, RTSimulationLightcurveFile, RTSimulationSpectrumFile


@admin.action(description="Generate interactive plot")
def generate_interactive_plot(modeladmin, request, queryset):
    for obj in queryset:
        if obj.is_valid_hesma_file:
            obj.interactive_plot = obj.get_plot_json()
        obj.save()


@admin.register(RTSimulationLightcurveFile)
class RTSimulationLightcurveFileAdmin(admin.ModelAdmin):
    actions = [generate_interactive_plot]


@admin.register(RTSimulationSpectrumFile)
class RTSimulationSpectrumFileAdmin(admin.ModelAdmin):
    actions = [generate_interactive_plot]


admin.site.register(RTSimulation)
