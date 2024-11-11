import re
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, UniversityTag, GenreTag

# 해름님 파트
class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # user_university = serializers.PrimaryKeyRelatedField(queryset=UniversityTag.objects.all())
    user_university = serializers.SlugRelatedField(
        slug_field='university_name',
        queryset=UniversityTag.objects.all()
    )
    # favorite_genre = serializers.PrimaryKeyRelatedField(
    #     queryset=GenreTag.objects.all(),
    #     many=True,
    #     required=False
    # )
    favorite_genre = serializers.SlugRelatedField(
        slug_field='genre_name',
        queryset=GenreTag.objects.all(),
        many=True,
        required=False
    )
    nickname = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'nickname', 'user_university','favorite_genre', 'description']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("중복된 아이디가 존재합니다")
        return value

    def validate_password(self, value):
        if len(value) < 8 or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("올바르지 않은 비밀번호 양식입니다")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        account = Account.objects.create(
            user=user,
            user_university=validated_data['user_university'],
            nickname=validated_data['nickname'],
            name=validated_data['name'],
            description=validated_data.get('description', "")
        )
        return account