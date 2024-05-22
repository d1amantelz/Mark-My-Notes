from django.contrib import admin
from .models import *


class ReportImageInline(admin.TabularInline):
    model = ReportImage
    extra = 1


class ReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at')
    inlines = [ReportImageInline]


admin.site.register(Report, ReportAdmin)
# admin.site.register(ReportImage)
admin.site.register(Note)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Setting)
admin.site.register(Activity)
