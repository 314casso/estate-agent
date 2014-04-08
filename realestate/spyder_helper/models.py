# -*- coding: utf-8 -*-
from django.db import models

class SpyderMeta(models.Model):
    NEW = 0
    PROCESSED = 1    
    ERROR = 2
    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (PROCESSED, u'Обработанный'),
        (ERROR, u'Ошибка'),
    )
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    spyder = models.CharField(unique=True, max_length=100)
    url = models.URLField(unique=True, db_index=True, max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES)
    
