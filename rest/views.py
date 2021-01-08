from django.shortcuts import render

# Create your views here.
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from logic.models import Manager as ManagerModel
from rest.serializers import ManagerCreation as ManagerCreationSerializer, ProjectListing as ProjectListingSerializer, ProjectCreation as ProjectCreationSerializer
from rest.serializers import ManagerListing as ManagerListingSerializer
from rest.serializers import ManagerRetrieval as ManagerRetrievalSerializer
from urls.models import Project as ProjectModel


class GetSerializerClassMixin(object):

    serializer_action_classes = dict()

    def get_serializer_class(self):
        """
        A class which inherits this mixins should have variable
        `serializer_action_classes`.
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class SampleViewSet(viewsets.ViewSet):
            serializer_class = DocumentSerializer
            serializer_action_classes = {
               'upload': UploadDocumentSerializer,
               'download': DownloadDocumentSerializer,
            }
            @action
            def upload:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class Manager(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = ManagerModel.objects.select_related('user').all()
    filter_backends = [DjangoFilterBackend]
    serializer_action_classes = {
        'list': ManagerListingSerializer,
        'retrieve': ManagerRetrievalSerializer,
        'create': ManagerCreationSerializer
    }


class Project(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = ProjectModel.objects.select_related('project', 'project__manager', 'project__manager__user').all()
    filter_backends = [DjangoFilterBackend]
    serializer_action_classes = {
        'list': ProjectListingSerializer,
        'create': ProjectCreationSerializer,
        'retrieve': ProjectListingSerializer
    }
    lookup_field = 'public_id'

