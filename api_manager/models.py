# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#from django.db import models


# Create your models here.
class Images(object):
    def __init__(self, **kwargs):
        for field in ('id', 'name', 'files'):
            setattr(self, field, kwargs.get(field, None))


images = {
    1: Images(id=1, name='Demo', files="aaa"),
}
