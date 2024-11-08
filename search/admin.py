from django.contrib import admin

from search.models import UniversityTag, GenreTag, StackTag, Platform

# Register your models here.
admin.site.register(UniversityTag)
admin.site.register(GenreTag)
admin.site.register(StackTag)
admin.site.register(Platform)