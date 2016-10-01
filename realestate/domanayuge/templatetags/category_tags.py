# -*- coding: utf-8 -*-
from django import template
from domanayuge.models import Category, ContentEntry

register = template.Library()

@register.assignment_tag
def category(slug):
    try:
        return Category.objects.get(slug=slug)
    except Category.DoesNotExist:  # @UndefinedVariable
        return None 
    
@register.assignment_tag
def article(slug):
    try:
        return ContentEntry.objects.get(slug=slug)
    except ContentEntry.DoesNotExist:
        return None