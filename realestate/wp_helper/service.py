# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies, media
from wordpress_xmlrpc.wordpress import WordPressTerm, WordPressPost
import difflib
from wordpress_xmlrpc import AnonymousMethod
from wp_helper.models import WordpressTaxonomyTree, EstateWordpressMeta
from django.core.exceptions import ObjectDoesNotExist
from django.template.base import Template
from django.template.context import Context
from estatebase.models import Locality
import pymorphy2
from django.template import loader
import re
import os
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.media import GetMediaItem, GetMediaLibrary
from urlparse import urljoin
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, GetPost

        
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
    
    def get_normal_form_parser(self, parses):
        none_animacy = None        
        for item in parses:                      
            if item.tag.POS not in 'PREP':                
                if (item.normal_form == item.word and item.tag.animacy == 'inan') or item.tag.number == 'plur':                         
                    return item
                if item.tag.animacy is None:
                    none_animacy = item
        return none_animacy
            
    def inflect(self, name, case):
        cases = {
            1 : 'nomn', #    именительный    Кто? Что?    хомяк ест
            2 : 'gent', #    родительный    Кого? Чего?    у нас нет хомяка
            3 : 'datv', #    дательный    Кому? Чему?    сказать хомяку спасибо
            4 : 'accs', #    винительный    Кого? Что?    хомяк читает книгу
            5 : 'ablt', #    творительный    Кем? Чем?    зерно съедено хомяком
            6 : 'loct', #    предложный    О ком? О чём? и т.п.    хомяка несут в корзинке
        }
        parts = name.split()
        result = []
        for part in parts:                
            p = self.get_normal_form_parser(self.morph.parse(part))
            if p:
                item = p.inflect({cases[case]})
                word = item.word if item else part                     
                result.append(pymorphy2.shapes.restore_word_case(word, part))
            else:
                result.append(part)
        if result:
            return ' '.join(result)
        
    def get_taxonomies(self, name='category'):
        if not name in self._taxonomies:            
            self._taxonomies[name] = self.client.call(taxonomies.GetTerms(name))
        return self._taxonomies[name]
    def get_or_create_category(self, estate):
        locality_id = estate.locality_id
        estate_type_name = estate.basic_estate_type.name 
        wp_cat = WordpressTaxonomyTree.objects.filter(parent__localities__id=locality_id, name__iexact=estate_type_name)[:1]    
        if wp_cat:
            return wp_cat.get()
        else:
            wp_cats = WordpressTaxonomyTree.objects.filter(localities__id=locality_id)
            len_cats = len(wp_cats)
            if len_cats != 1:
                raise ObjectDoesNotExist(u'Населенный пункт с id %s, связан с %s категорией wordperss!'  % (locality_id, len_cats))
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
    
    def render_post_category(self, estate):
        result = []        
        taxonomy_tree = self.get_or_create_category(estate)
        category = self.client.call(taxonomies.GetTerm('category', taxonomy_tree.wp_id))
        if category:
            result.append(category)
        return result
    
    def delete_taxonomy(self, term_id):
        self.client.call(taxonomies.DeleteTerm('category', term_id))
            
    def find_term(self, term, queryset):        
        result = {}
        for item in queryset:
            ratio = difflib.SequenceMatcher(None, term.lower(), item.name.lower().replace('_', '')).ratio()
            if ratio > self._ratio:
                result[ratio] = item        
        return result[sorted(result, key=result.get)[0]] if result else None
    
    def get_post_by_estate(self, estate):                         
        post_id = int(self.client.call(GetPostID(self.META_KEY,estate.id)))
        if post_id:
            return self.client.call(GetPost(post_id))
    
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
        return u'%s' % template.render(Context(context))
    
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
    
    def render_post_body(self, estate, description, images):        
        t = loader.get_template('reports/wp_post.html')
        c = Context({'estate_item':estate, 'description': description, 'images': images})
        rendered = t.render(c)
        return re.sub(r"\s+"," ", rendered)
    
    def get_estate_images(self, estate):
        from sorl.thumbnail import get_thumbnail        
        images = estate.images.all()[:4]
        if images:
            result = {}
            for img in images:               
                im = get_thumbnail(img.image.file, '800x600')
                head, tail = os.path.split(im.name)  # @UnusedVariable                                
                result[os.path.join(im.storage.location,im.name)] = tail                  
            return result
        
    def get_filtered_post_images(self, estate, post_id):
        estate_images = self.get_estate_images(estate)
        if not estate_images:
            return {}
        if not post_id:
            return {'estate_images' : estate_images}
        fltr = {'parent_id' : post_id}                
        media_items = self.client.call(GetMediaLibrary(fltr))
        keys = set()
        same_items = set()
        for key, image in estate_images.items():
            for item in media_items:
                if item.metadata['file'].find(os.path.splitext(image)[0]) != -1:
                    keys.add(key)
                    same_items.add(item)
        for key in keys:
            del estate_images[key]
        return {'estate_images' : estate_images, 'same_items': same_items}     

    def get_media_items(self, estate, post_id):
        data = {'type':'image/jpg', 'overwrite':False}
        filtered_post_images = self.get_filtered_post_images(estate, post_id)        
        estate_images = filtered_post_images.get('estate_images')
        result = []
        if estate_images:
            for filepath, name in estate_images.items(): 
                data['name'] = name        
                result.append(self.upload_image(filepath, data))
        same_items = filtered_post_images.get('same_items')
        if same_items:                 
            result.extend(same_items)
        return result
        
    def render_post_images(self, estate, post_id):        
        context = {'class' : 'face-post-image'}
        template = '<a class="%(class)s" href="%(link)s"><img src="%(src)s"></a>'
        media_items = self.get_media_items(estate, post_id)
        post_images = []
        for item in media_items:
            context['link'] = item.link
            context['src'] = urljoin(item.link, item.metadata['sizes']['thumbnail']['file'])
            post_images.append(template % context)
        return post_images
    
    def render_custom_fields(self, estate):
        fields = {}
        taxonomy_tree_item = estate.locality.wp_taxons.all()[:1].get()        
        fields['locality'] = taxonomy_tree_item.wp_meta_locality.wp_id
        fields['Nomer'] = estate.pk
        estate_type = estate.basic_estate_type  
        fields['object_type'] = estate_type.wp_taxons.all()[:1].get().wp_id
        fields['price'] = estate.agency_price
        fields['region'] = estate.locality.region.wp_taxons.all()[:1].get().wp_id
        fields['rooms'] = estate.basic_bidg.room_count if estate.basic_bidg else None
        fields['status'] = estate.estate_status.wp_taxons.all()[:1].get().wp_id  
        result = []
        for key, value in fields.items():        
            result.append({'key': key, 'value': value})
        return result
        
    def upload_image(self, filename, data):               
        """
        Upload a file to the blog.

        Note: the file is not attached to or inserted into any blog posts.
    
        Parameters:
            `filename`: `string` full file name
            `data`: `dict` with three items:
                * `name`: filename
                * `type`: MIME-type of the file               
        Returns: `MediaItem`       
        """
        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())

        response = self.client.call(media.UploadFile(data))
        return self.client.call(GetMediaItem(response['id']))
    def render_post_description(self, estate):
        region = u'Краснодарского края' if estate.locality.locality_type_id == Locality.CITY else self.inflect(estate.locality.region.regular_name,2)
        location = u'%s %s' % (self.inflect(estate.locality.name,6), region)
        result = u'Продается %s в %s' % (estate.estate_type.lower(), location)             
        return result
    
    def get_custom_field_id(self, old_custom_fields, key):
        for field in old_custom_fields:
            if field.get('key') == key:
                return field.get('id')
    
    def assemble_post(self, estate, old_post, published=True):
        post = WordPressPost()
        post_id = None
        description = self.render_post_description(estate)
        if old_post:
            post_id = old_post.id
        
        post.custom_fields = [
                              {'key': '_aioseop_description', 'value': description}, 
                              {'key': '_aioseop_title', 'value': self.render_seo_post_title(estate)},
                              {'key': '_aioseop_keywords', 'value': u','.join(self.render_post_tags(estate))},
                             ]
        post.custom_fields.extend(self.render_custom_fields(estate))
        if post_id:
            for custom_field in post.custom_fields:
                custom_field['id'] = self.get_custom_field_id(old_post.custom_fields, custom_field.get('key'))
            
        post.title = self.render_post_title(estate)
        post_images = self.render_post_images(estate, post_id)
        images = u''.join(post_images)
        post.content = self.render_post_body(estate, description, images)
        post.terms_names = {'post_tag': self.render_post_tags(estate)}
        post.terms = self.render_post_category(estate)
        if published:
            post.post_status = 'publish'
        return post
    def sync_post(self, estate):
        wp_meta = estate.wp_meta
        old_post = self.get_post_by_estate(estate)
        wp_meta.post_id = old_post.id if old_post else None 
        if wp_meta.post_id == -1:
            wp_meta.status = EstateWordpressMeta.MULTIKEYS
            wp_meta.save()
            return False        
        post = self.assemble_post(estate, old_post, True)
        if not wp_meta.post_id:
            wp_meta.post_id = self.client.call(NewPost(post))        
        else:
            self.client.call(EditPost(wp_meta.post_id, post))
        wp_meta.status = EstateWordpressMeta.UPTODATE
        wp_meta.save()
        return True