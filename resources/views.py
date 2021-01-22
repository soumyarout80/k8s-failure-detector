from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import ResourceTypeSerializer
from .serializers import AlertSerializer
from .models import Resource
from .models import Alert
from .models import Account

from django.conf import settings
from django.core.mail import send_mail


class ResourceViewSet(viewsets.ViewSet):

    def list(self, request):
        resources = Resource.objects.all()
        serializer = ResourceTypeSerializer(resources, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ResourceTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class AlertViewSet(viewsets.ViewSet):
    def list(self, request):
        resources = Alert.objects.all()
        serializer = AlertSerializer(resources, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AlertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = 'Kubernetes alerts'
        user_name = serializer.data['email_id'].split("@")[0]
        message = f'Hi {user_name}, One of your kubernetes node is Down.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [serializer.data['email_id'] ]
        send_mail( subject, message, email_from, recipient_list )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


# Create your views here.
