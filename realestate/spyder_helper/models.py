# -*- coding: utf-8 -*-
from django.db import models

class SpiderMeta(models.Model):
    NEW = 0
    PROCESSED = 1    
    ERROR = 2
    NOPHONE = 3
    EXISTSPHONE = 4
    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (PROCESSED, u'Обработанный'),
        (ERROR, u'Ошибка'),
        (NOPHONE, u'Нет телефона'),
        (EXISTSPHONE, u'Телефон в базе'),
    )
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    spider = models.CharField(db_index=True, max_length=100)
    url = models.URLField(db_index=True, max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, db_index=True, default=NEW)
    class Meta:
        unique_together = ('spider', 'url')
    
    
