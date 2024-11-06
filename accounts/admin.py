from django.contrib import admin
from .models import Account, UniversityTag, GenreTag, StackTag

# Register your models here.
admin.site.register(Account)
admin.site.register(UniversityTag)
admin.site.register(GenreTag)
admin.site.register(StackTag)