# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.response import Response
from api_manager import serializers
import os
from django.conf import settings

# Create your views here.


def getImage(pk):
    image = None
    for fileName in os.listdir(settings.MEDIA_ROOT):
        if int(fileName.split('|')[0]) == int(pk):
            image = fileName
    return image


class ImageViewSet(viewsets.ViewSet):
    serializer_class = serializers.ImageSerializer

    def list(self, request):
        resp = []
        for fileName in os.listdir(settings.MEDIA_ROOT):
            resp.append({
                "id":
                fileName.split('|')[0],
                "url":
                request.build_absolute_uri(
                    "{}{}".format(settings.MEDIA_URL, fileName))
            })
        return Response(resp)

    def create(self, request):
        serializer = serializers.ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            image = getImage(pk)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "id":
            pk,
            "url":
            request.build_absolute_uri(
                "{}{}".format(settings.MEDIA_URL, image))
        }, )

    def destroy(self, request, pk=None):
        try:
            image = getImage(pk)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        os.remove(os.path.join(settings.MEDIA_ROOT, image))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk=None):
        try:
            image = getImage(pk)
            if not image:
                raise KeyError
        except KeyError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        os.remove(os.path.join(settings.MEDIA_ROOT, image))
        serializer = serializers.ImageSerializer(pk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
