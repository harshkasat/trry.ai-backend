from django.contrib import admin
from core.models import URLTable, ExtraURLTable, StressTable, PerformanceLighthouseTable, ResponsiveTable

# Register your models here.
admin.site.register(URLTable)
admin.site.register(ExtraURLTable)
admin.site.register(StressTable)
admin.site.register(PerformanceLighthouseTable)
admin.site.register(ResponsiveTable)
