from django.contrib import admin
from . models import *
# Register your models here.
class CustomerProfileAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return CustomerProfile.all_objects.all()
admin.site.register(CustomerProfile, CustomerProfileAdmin)
# admin.site.register(CustomerProfile)
admin.site.register(ProviderProfile)
admin.site.register(Job)