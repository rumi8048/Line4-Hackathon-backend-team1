from django.db import models
from django.contrib.auth.models import User

class UniversityTag(models.Model):
    # 대학교 이름
    university_name = models.CharField(null=False, max_length=255)

class GenreTag(models.Model):
    # 장르 이름
    genre_name = models.CharField(null=False, max_length=255)

class StackTag(models.Model):
    # 스택 이름
    stack_name = models.CharField(null=False, max_length=255)


class Account(models.Model):
    # id, username, password, is_staff, is_superuser, last_login, date_joined 필드가 존재
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 여기서부터는 커스텀
    user_university = models.ForeignKey(UniversityTag, on_delete=models.CASCADE)
    favorite_genre = models.ManyToManyField(GenreTag, related_name= "account")
    nickname = models.CharField(max_length=255, unique=True)
    total_point = models.IntegerField(default=0)
    description = models.TextField(max_length=255, default="")

