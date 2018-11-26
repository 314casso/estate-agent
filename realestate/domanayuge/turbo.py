# -*- coding: utf-8 -*-

from lxml import etree
from django.template.loader import render_to_string
from django.template.context import RequestContext

class FeedGenerator(object):
    def create_rss(self, request):
        nsmap = dict()        
        
        nsmap.update({
            'yandex': 'http://news.yandex.ru',
            'media': 'http://search.yahoo.com/mrss/',
            'turbo': 'http://turbo.yandex.ru'
            })

        feed = etree.Element('rss', version='2.0', nsmap=nsmap)
        channel = etree.SubElement(feed, 'channel')

        item = etree.SubElement(channel, 'item', turbo='true')

        link = etree.SubElement(item, 'link')
        link.text = 'http://www.example.com/page1.html'

        content = etree.SubElement(item, '{%s}content' % nsmap['turbo'])

        context = {
            'contact_name': u"John!",        
        }
        
        cdata = render_to_string('turbo/content.html', context, 
                           context_instance=RequestContext(request))

        content.text = etree.CDATA(cdata)                   

        return etree.tostring(feed, pretty_print=True, encoding='UTF-8',
                              xml_declaration=False)

