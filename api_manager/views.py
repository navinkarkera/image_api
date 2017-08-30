# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from api_manager import serializers
import os
from django.conf import settings
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from .serializers import readFromJson, deleteItem
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

# Create your views here.

User = get_user_model()


def getImage(pk, userid):
    image = None
    folder_path = os.path.join(settings.MEDIA_ROOT, str(userid))
    for fileName in os.listdir(folder_path):
        if int(fileName.split('|')[0]) == int(pk):
            image = fileName
    return image, folder_path


class ImageViewSet(viewsets.ViewSet):
    serializer_class = serializers.ImageSerializer

    def list(self, request):
        resp = readFromJson()
        if resp:
            if str(request.user.id) in resp and resp[str(request.user.id)]:
                return Response(resp[str(request.user.id)])
            return Response("No images uploaded.")
        return Response("No images uploaded.")

    def create(self, request):
        serializer = serializers.ImageSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            image, folder_path = getImage(pk, request.user.id)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        url = request.build_absolute_uri(
            "{}{}/{}".format(settings.MEDIA_URL, str(request.user.id), image))
        return Response({"id": pk, "url": url}, )

    def destroy(self, request, pk=None):
        try:
            image, folder_path = getImage(pk, request.user.id)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)

        os.remove(os.path.join(folder_path, image))
        deleteItem(pk, request.user.id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        try:
            image, folder_path = getImage(pk, request.user.id)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(status=status.HTTP_404_NOT_FOUND)
        os.remove(os.path.join(folder_path, image))
        serializer = serializers.ImageSerializer(
            pk, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class CreateUserView(CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response(
            {
                'token': token.key
            },
            status=status.HTTP_201_CREATED,
            headers=headers)


@api_view()
def regenerateToken(request):
    Token.objects.filter(user=request.user).delete()
    token, created = Token.objects.get_or_create(user=request.user)
    return Response({'token': token.key})
