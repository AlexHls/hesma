from django.contrib import admin

from hesma.hydro.models import HydroSimulation, HydroSimulation1DModelFile


@admin.action(description="Generate interactive plot")
def generate_interactive_plot(modeladmin, request, queryset):
    for obj in queryset:
        if obj.is_valid_hesma_file:
            obj.interactive_plot = obj.get_plot_json()
        obj.save()


@admin.register(HydroSimulation1DModelFile)
class HydroSimulation1DModelFileAdmin(admin.ModelAdmin):
    actions = [generate_interactive_plot]


admin.site.register(HydroSimulation)
