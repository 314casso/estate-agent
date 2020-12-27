# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from wp_helper.service import WPService
from settings import WP_PARAMS
from estatebase.models import Estate, EstateStatus
from django.utils import translation
from wp_helper.models import EstateWordpressMeta, WordpressTaxonomyTree
import time
from wordpress_xmlrpc import AnonymousMethod, AuthenticatedMethod
from wordpress_xmlrpc.methods import taxonomies


class GetPostID(AnonymousMethod):
        method_name = 'picassometa.getPostID'
        method_args = ('meta_key','meta_value')

class Command(BaseCommand):
    def handle(self, *args, **options):
        translation.activate('ru')        
        wp_service = WPService(WP_PARAMS['site'])
        self.sync_terms(wp_service)      
                
    def sync_terms(self, wp_service):
#         estate = Estate.objects.get(pk='107602')           
#         print(estate.pk)                     
#         wp_service.sync_post(estate)

        terms = WordpressTaxonomyTree.objects.filter(localities__isnull=False)
        
        for term in terms:
            l = wp_service.client.call(taxonomies.GetTerms('category', {'search': term.name }))
            if len(l) == 1:
                if l[0].id != term.wp_id:
                    if l[0].parent == term.parent.wp_id and term.name == l[0].name:
                        term.wp_id = l[0].id
                        term.save()                   
#                         print u"%s %s %s" % (term.name, l[0].id, term.wp_id)
                    else:
                        print u'Error %s %s %s' % (term.name, l[0].parent, l[0].name)
                else:
                    print u'Success %s %s %s' % (term.name, l[0].parent, l[0].name)
            elif len(l) == 0: 
                wp_service.create_taxonomy(term.parent.wp_id, term.name)       
            else:
                print u"%s %s!!!" % (term.name, len(l))
