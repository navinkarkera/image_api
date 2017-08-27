from rest_framework import serializers
from api_manager.models import Images
from django.conf import settings
import os


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False, max_length=250)
    image = serializers.ImageField(max_length=None, use_url=True)

    def create(self, validated_data):
        print validated_data
        image = validated_data['image']
        path_to_save = os.path.join(settings.MEDIA_ROOT, "{}|{}".format(
            getLatestId(), image.name))
        with open(path_to_save, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        return validated_data

    def update(self, instance, validated_data):
        image = validated_data['image']
        path_to_save = os.path.join(settings.MEDIA_ROOT, "{}|{}".format(
            instance, image.name))
        with open(path_to_save, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        return validated_data


def getLatestId():
    ids = []
    for fileName in os.listdir(settings.MEDIA_ROOT):
        ids.append(int(fileName.split('|')[0]))
    return max(ids) + 1 if ids else 1
