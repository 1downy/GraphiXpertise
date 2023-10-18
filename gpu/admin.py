from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, GPUList, GPU
admin.site.register(User, UserAdmin)

admin.AdminSite.site_header = "GraphiXpertise Administration"
admin.AdminSite.index_title = "GraphiXpertise"
admin.AdminSite.site_title = "Admin Panel"


@admin.register(GPUList)
class GPUListAdmin(admin.ModelAdmin):
    list_display = ['ProductName', 'Released', 'Bus',
                    'Memory', 'Shaders_TMUs_ROPs', 'URL']
    list_display_links = ['ProductName', 'Released', 'Bus',
                          'Memory', 'Shaders_TMUs_ROPs', 'URL']
    search_fields = ['ProductName', 'Released']


@admin.register(GPU)
class GPUAdmin(admin.ModelAdmin):
    list_display = ['id', 'gpu_name', 'name', 'variant', 'release_date', 'bus_interface',
                    'memory_size', 'gpu_clock', 'memory_type',
                    'shading_units', 'tmus', 'rops']
    list_display_links = ['name', 'variant', 'release_date', 'bus_interface',
                          'memory_size']

    def gpu_name(self, obj):
        return GPUList.objects.get(gpu_specs=obj).ProductName if GPUList.objects.get(gpu_specs=obj) else None
    gpu_name.short_description = 'GPU Name'
