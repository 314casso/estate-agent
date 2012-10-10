# -*- coding: utf-8 -*-

from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


class OrderedModelAdmin(admin.ModelAdmin):
    ordering = ['order']
    exclude = ['order']

    def get_urls(self):
        my_urls = patterns('',
                (r'^(?P<pk>\d+)/move_up/$', self.admin_site.admin_view(self.move_up)),
                (r'^(?P<pk>\d+)/move_down/$', self.admin_site.admin_view(self.move_down)),
        )
        return my_urls + super(OrderedModelAdmin, self).get_urls()

    def reorder(self, item):
        DEFAULT_SORT_UP = getattr(settings, 'DEFAULT_SORT_UP' , u'&uarr; вверх')
        DEFAULT_SORT_DOWN = getattr(settings, 'DEFAULT_SORT_DOWN' , u'&darr; вниз')
        button = '<a href="{0}/move_{1}">{2}</a>'
        html = ''
        html += button.format(item.pk, 'down', DEFAULT_SORT_DOWN)
        html += '&nbsp;' + button.format(item.pk, 'up', DEFAULT_SORT_UP)
        return html    
    reorder.allow_tags = True
    reorder.short_description = _('Order')

    def move_down(self, request, pk):
        if self.has_change_permission(request):
            item = get_object_or_404(self.model, pk=pk)
            try:
                next_item = self.model.objects.filter(order__gt=item.order).order_by('order')[0]
            except IndexError: # Last item
                pass
            else:
                self.model.swap(item, next_item)
        return HttpResponseRedirect('../../')

    def move_up(self, request, pk):
        if self.has_change_permission(request):
            item = get_object_or_404(self.model, pk=pk)
            try:
                prev_item = self.model.objects.filter(order__lt=item.order).order_by('-order')[0]
            except IndexError: # First item
                pass
            else:
                self.model.swap(item, prev_item)
        return HttpResponseRedirect('../../')

