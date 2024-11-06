from django.contrib import admin

from search.models import UniversityTag, GenreTag, StackTag

# Register your models here.
admin.site.register(UniversityTag)
admin.site.register(GenreTag)
admin.site.register(StackTag)