from rest_framework import serializers
from django.conf import settings
import os, json
from django.contrib.auth import get_user_model
import errno

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validate_data):
        user = UserModel.objects.create(username=validate_data['username'])
        user.set_password(validate_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = (
            'email',
            'username',
            'password', )


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    url = serializers.URLField(read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True)

    def create(self, validated_data):
        print validated_data
        request = self.context['request']
        image = validated_data['image']
        latestId = getLatestId(str(request.user.id))
        fileName = "{}|{}".format(latestId, image.name)
        folder_path = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
        make_sure_path_exists(folder_path)
        path_to_save = os.path.join(folder_path, fileName)
        with open(path_to_save, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        data = readFromJson()
        url = request.build_absolute_uri("{}{}/{}".format(
            settings.MEDIA_URL, str(request.user.id), fileName))
        data = updateDict(
            createImagePart(latestId, url), str(request.user.id), data)
        writeToJson(data)
        validated_data['id'] = latestId
        validated_data['url'] = url
        return validated_data

    def update(self, instance, validated_data):
        request = self.context['request']
        image = validated_data['image']
        latestId = int(instance)
        fileName = "{}|{}".format(latestId, image.name)
        folder_path = os.path.join(settings.MEDIA_ROOT, str(request.user.id))
        make_sure_path_exists(folder_path)
        path_to_save = os.path.join(folder_path, fileName)
        with open(path_to_save, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)
        data = readFromJson()
        url = request.build_absolute_uri("{}{}/{}".format(
            settings.MEDIA_URL, str(request.user.id), fileName))
        data = updateDict(
            createImagePart(latestId, url), str(request.user.id), data)
        writeToJson(data)
        validated_data['id'] = latestId
        validated_data['url'] = url
        return validated_data


def getLatestId(userid):
    ids = []
    data = readFromJson()
    if not data:
        return 1
    if userid in data and data[userid]:
        row = max(data[userid], key=lambda x: x['id'])
        return int(row['id']) + 1
    return 1


def updateDict(part, userid, data):
    if not data:
        data = {}
    if userid in data:
        data = deleteImage(part['id'], userid, data)
        data[userid].append(part)
    else:
        data[userid] = [part]
    return data


def deleteImage(id, userid, data):
    for i, row in enumerate(data[userid]):
        if str(row['id']) == str(id):
            data[userid].pop(i)
            break
    return data


def deleteItem(id, userid):
    data = deleteImage(id, str(userid), readFromJson())
    writeToJson(data)


def createImagePart(id, url):
    return {'id': id, 'url': url}


def writeToJson(data, file='data.json'):
    with open(file, 'w') as f:
        json.dump(data, f)


def readFromJson(file='data.json'):
    if os.path.isfile(file):
        with open(file) as f:
            data = json.load(f)
        return data
    return None


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
