from django.db import models
from django.contrib.auth.models import User
from search.models import UniversityTag, GenreTag

class Account(models.Model):
    # id, username, password, is_staff, is_superuser, last_login, date_joined 필드가 존재
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 여기서부터는 커스텀
    user_university = models.ForeignKey(UniversityTag, on_delete=models.CASCADE)
    favorite_genre = models.ManyToManyField(GenreTag, related_name= "account")
    nickname = models.CharField(null=False, max_length=255, unique=True)
    total_point = models.IntegerField(default=0)
    description = models.TextField(max_length=255, default="")

