# -*- coding: utf-8 -*-
from django.db import models
from estatebase.models import Estate

class SpiderMeta(models.Model):
    NEW = 0
    PROCESSED = 1    
    ERROR = 2
    NOPHONE = 3
    EXISTSPHONE = 4
    DO_NOT_PROCESS = 5
    STATUS_CHOICES = (
        (NEW, u'Новый'),
        (PROCESSED, u'Обработанный'),
        (ERROR, u'Ошибка'),
        (NOPHONE, u'Нет телефона'),
        (EXISTSPHONE, u'Телефон в базе'),
        (DO_NOT_PROCESS, u'Не обрабатывать'),
    )
    created = models.DateTimeField(db_index=True, auto_now_add=True)
    spider = models.CharField(db_index=True, max_length=100)
    url = models.URLField(db_index=True, max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, db_index=True, default=NEW)
    phone_filename = models.CharField(max_length=250, blank=True, null=True)
    estate = models.ForeignKey(Estate, related_name='spider_meta', blank=True, null=True)
    class Meta:
        unique_together = ('spider', 'url')
    
    
