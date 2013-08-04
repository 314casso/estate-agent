# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.wordpress import WordPressTerm
import difflib
from wordpress_xmlrpc import AnonymousMethod
from wp_helper.models import WordpressTaxonomyTree
from django.core.exceptions import ObjectDoesNotExist
from django.template.base import Template
from django.template.context import Context
from estatebase.models import Locality
import pymorphy2
        
class GetPostID(AnonymousMethod):
        method_name = 'picassometa.getPostID'
        method_args = ('meta_key','meta_value')

class WPService(object):
    META_KEY = 'Nomer'
    _ratio = 0.85
    _taxonomies = {}   
    def __init__(self, params):
        self.params = params        
        self.client = Client(**self.params)
        self.morph = pymorphy2.MorphAnalyzer()
    
    def get_normal_form(self, parses):        
        for item in parses:            
            if item.normal_form == item.word:    
                return item
        return parses[0]
    
    def inflect(self, name, case, number='sing'):
        cases = {
            1 : 'nomn', #    именительный    Кто? Что?    хомяк ест
            2 : 'gent', #    родительный    Кого? Чего?    у нас нет хомяка
            3 : 'datv', #    дательный    Кому? Чему?    сказать хомяку спасибо
            4 : 'accs', #    винительный    Кого? Что?    хомяк читает книгу
            5 : 'ablt', #    творительный    Кем? Чем?    зерно съедено хомяком
            6 : 'loct', #    предложный    О ком? О чём? и т.п.    хомяка несут в корзинке
        }
        parts = name.split()
        if len(parts) == 1:               
            p = self.get_normal_form(self.morph.parse(parts[0]))
            word = p.inflect({number, cases[case]}).word
            return pymorphy2.shapes.restore_word_case(word, parts[0])
        
    def get_taxonomies(self, name='category'):
        if not name in self._taxonomies:            
            self._taxonomies[name] = self.client.call(taxonomies.GetTerms(name))
        return self._taxonomies[name]
    def get_or_create_category(self, locality_id, estate_type_name):
        wp_cats = WordpressTaxonomyTree.objects.filter(parent__localities__id=locality_id, name__iexact=estate_type_name)    
        if len(wp_cats):
            return wp_cats[0]
        else:
            wp_cats = WordpressTaxonomyTree.objects.filter(localities__id=locality_id)
            len_cats = len(wp_cats)
            if len_cats != 1:
                raise ObjectDoesNotExist(u'Населенный пункт с id %s, связанн с %s категорией wordperss!'  % (locality_id, len_cats))
            else:
                taxonomy_item = list(wp_cats)[0]
                remote_taxonomy = None
                try:                                        
                    remote_taxonomy = self.create_taxonomy(taxonomy_item.wp_id, estate_type_name)
                except:
                    raise Exception(u'Не удалось создать категорию на стороне wordpress! Если категория существует на сайте, запустите синхронизацию...')
                if remote_taxonomy:
                    return WordpressTaxonomyTree.objects.create(
                                                         name=remote_taxonomy.name,
                                                         wp_parent_id=taxonomy_item.wp_id,
                                                         wp_id=remote_taxonomy.id,                                                         
                                                         parent=taxonomy_item,
                                                         up_to_date=True,
                                                         )                   
            
    def create_taxonomy(self, parent_cat_id, name, taxonomy='category'):
        child_cat = WordPressTerm()
        child_cat.taxonomy = taxonomy
        if parent_cat_id:
            child_cat.parent = parent_cat_id
        child_cat.name = name
        child_cat.id = self.client.call(taxonomies.NewTerm(child_cat))
        return child_cat
    def delete_taxonomy(self, term_id):
        self.client.call(taxonomies.DeleteTerm('category', term_id))
            
    def find_term(self, term, queryset):        
        result = {}
        for item in queryset:
            ratio = difflib.SequenceMatcher(None, term.lower(), item.name.lower().replace('_', '')).ratio()
            if ratio > self._ratio:
                result[ratio] = item        
        return result[sorted(result, key=result.get)[0]] if result else None
    def get_post_id_by_meta_key(self, estate_id):        
        return int(self.client.call(GetPostID(self.META_KEY,estate_id)))
    def render_post_title(self, estate):
        context = {}
        template = Template(u'{{ estate_type }}{{ stead }} {{ locality }} {{ region }}{{ microdistrict }}')              
        context['estate_type'] = estate.estate_type_total_area
        context['locality'] = u'в %s' % self.inflect(estate.locality.name,6)
        if estate.locality.locality_type_id != Locality.CITY:
            context['region'] = self.inflect(estate.locality.region.regular_name,2)
        basic_stead = estate.basic_stead
        if not estate.estate_category.is_stead and basic_stead and basic_stead.total_area_sotka:
            context['stead'] = u' на участке %g сот.' % basic_stead.total_area_sotka
        if estate.microdistrict:
            context['microdistrict'] = u', %s' % estate.microdistrict.name
        template = template.render(Context(context))
        return template
    def render_seo_post_title(self, estate):
        result = u'Недвижимость %s'
        if estate.locality.locality_type_id == Locality.CITY:            
            result = result % self.inflect(estate.locality.name,2)            
        else:
            result = result % u'Краснодарского края'
        result = u'%s | %s в %s' % (result, estate.estate_type, self.inflect(estate.locality.name,6))
        return result
    def render_post_tags(self, estate):
        estate_type = estate.estate_type.lower()
        locality = estate.locality.name
        place = estate.beside.name if estate.beside else None  
        region = estate.locality.region.regular_name
        result = []
        result.append(u'купить %s в %s' % (self.inflect(estate_type ,4), self.inflect(locality,6)))
        result.append(u'%s в %s' % (estate_type, self.inflect(locality,6)))
        if place:
            result.append(u'%s у %s' % (estate_type, self.inflect(place,2)))
            result.append(u'недвижимость на %s' % self.inflect(place,6))
            result.append(place)
        result.append(u'%s в Краснодарском крае' % estate_type)
        result.append(u'%s %s' % (estate_type, self.inflect(locality,2)))
        result.append(u'недвижимость %s' % self.inflect(locality,2))
        result.append(u'купить недвижимость в %s' % self.inflect(locality,6))
        result.append(u'недвижимость Краснодарского края')
        result.append(u'купить недвижимость в Краснодарском крае')
        result.append(u'купить %s в Краснодарском крае' % self.inflect(estate_type,4))
        result.append(locality)
        result.append(region)
        result.append(u'недвижимость %s' % self.inflect(region,2))
        result.append(u'Краснодарский край')
        return result
        
    
        
            
        
        


        
    

