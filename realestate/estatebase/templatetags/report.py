# -*- coding: utf-8 -*-
from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

def distance_helper(value):
    if value:
        return u' - %s м' % intcomma(value) 
    return ''

@register.inclusion_tag('inclusion/communication.html')
def communication(estate):
    comms = []
    if estate.electricity:
        comms.append('%s: %s %s' %  (u'свет', estate.electricity.name.lower(), distance_helper(estate.electricity_distance)))            
    if estate.watersupply:
        comms.append('%s: %s %s' %  (u'вода', estate.watersupply.name.lower(), distance_helper(estate.watersupply_distance)))
    if estate.gassupply:
        comms.append('%s: %s %s' %  (u'газ', estate.gassupply.name.lower(), distance_helper(estate.gassupply_distance)))    
    if estate.sewerage:
        comms.append('%s: %s %s' %  (u'канализация', estate.sewerage.name.lower(), distance_helper(estate.sewerage_distance)))        
    if estate.telephony:
        comms.append('%s: %s' %  (u'тел.', estate.telephony.name.lower()))    
    if estate.internet:
        comms.append('%s: %s' %  (u'интернет', estate.internet.name.lower()))    
    if estate.driveway:
        comms.append('%s: %s %s' %  (u'подъезд', estate.driveway.name.lower(), distance_helper(estate.driveway_distance)))    
    return {'comms': comms}
