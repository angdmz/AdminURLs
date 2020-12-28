import uuid

from django.contrib.auth.models import User as UserModel
from rest_framework import serializers

from logic.models import Manager as ManagerModel
from logic.models import Project as ProjectModel
from urls.models import Project as DetailsModel
from logic.querysets import all_user_queryset, all_managers_queryset


class User(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('username', 'email', 'id')


class Project(serializers.ModelSerializer):
    public_id = serializers.SerializerMethodField()
    max_requests_per_second = serializers.SerializerMethodField()
    max_requests_per_month = serializers.SerializerMethodField()

    def get_public_id(self, obj):
        return obj.details.public_id

    def get_max_requests_per_second(self, obj):
        return obj.details.max_requests_per_second

    def get_max_requests_per_month(self, obj):
        return obj.details.max_requests_per_month

    class Meta:
        model = ProjectModel
        fields = ('name', 'public_id', 'max_requests_per_second', 'max_requests_per_month')


class ManagerCreation(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=all_user_queryset)

    class Meta:
        model = ManagerModel
        fields = ('id', 'user_id', 'registration_on', 'modification_on')


class ManagerListing(serializers.ModelSerializer):
    user = User()

    class Meta:
        model = ManagerModel
        fields = ('id', 'user', 'registration_on', 'modification_on')


class ManagerRetrieval(serializers.ModelSerializer):
    user = User()
    projects = Project(many=True)

    class Meta:
        model = ManagerModel
        fields = ('id', 'user', 'projects', 'registration_on', 'modification_on')


class ProjectCreation(serializers.Serializer):

    manager_id = serializers.PrimaryKeyRelatedField(queryset=all_managers_queryset)
    project_id = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField()
    id_generator = uuid

    def get_project_id(self, obj):
        return obj.details.public_id

    def create(self, validated_data):
        project = ProjectModel.objects.create(manager=validated_data['manager_id'], name=validated_data['name'])
        details = DetailsModel.objects.create(project=project, public_id=self.id_generator.uuid4())
        return details

    def update(self, instance, validated_data):
        pass


