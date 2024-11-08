from django.db import models

# Create your models here.
class UniversityTag(models.Model):
    # 대학교 이름
    university_name = models.CharField(null=False, max_length=255)

class GenreTag(models.Model):
    # 장르 이름
    genre_name = models.CharField(null=False, max_length=255)

class StackTag(models.Model):
    # 스택 이름
    stack_name = models.CharField(null=False, max_length=255)

class Platform(models.Model):
    platform = models.CharField(null=False, max_length=255)