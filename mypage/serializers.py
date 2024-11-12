from rest_framework import serializers
from accounts.models import Account
from ptn_project.serializers import ProjectSerializer
from search.models import GenreTag, UniversityTag


class AccountCollaborateProjectSerializer(serializers.ModelSerializer):
    collaborator_projects = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['collaborator_projects']

    def get_collaborator_projects(self, obj):
        projects = obj.collaborator_projects.all()
        return ProjectSerializer(projects, many=True).data
    
class AccountScrapProjectSerializer(serializers.ModelSerializer):
    scrap_projects = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['scrap_projects']

    def get_scrap_projects(self, obj):
        projects = obj.scrap_projects.all()
        return ProjectSerializer(projects, many=True).data
    
class AccountInfoSerializer(serializers.ModelSerializer):
    user_university = serializers.SlugRelatedField(
        slug_field='university_name',
        queryset=UniversityTag.objects.all()
    )
    favorite_genre = serializers.SlugRelatedField(
        slug_field='genre_name',
        queryset=GenreTag.objects.all(),
        many=True,
        required=False
    )
    userid = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ['id', 'nickname', 'total_point', 'description', 'userid', 'user_university', 'favorite_genre']

    
    def get_userid(self, obj): 
        return obj.user.username

    def update(self, instance, validated_data):
        genres_data = validated_data.pop('favorite_genre', [])

        if genres_data:
            instance.favorite_genre.set(genres_data)

        # user_university 업데이트
        if 'user_university' in validated_data:
            university_name = validated_data.pop('user_university')
            university = UniversityTag.objects.filter(id=university_name.id).first()
            instance.user_university = university

        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)

        instance.save()
        return instance