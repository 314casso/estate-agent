# -*- coding: utf-8 -*-
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies, media
from wordpress_xmlrpc.wordpress import WordPressTerm, WordPressPost
import difflib
from wordpress_xmlrpc import AnonymousMethod, AuthenticatedMethod
from wp_helper.models import WordpressTaxonomyTree, EstateWordpressMeta
from django.core.exceptions import ObjectDoesNotExist
from django.template.base import Template
from django.template.context import Context
from estatebase.models import Locality, EntranceEstate
from django.template import loader
import re
import os
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.media import GetMediaItem, GetMediaLibrary
from urlparse import urljoin
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, GetPost
import datetime
import xmlrpclib
from collections import OrderedDict
        
class GetPostID(AnonymousMethod):
        method_name = 'picassometa.getPostID'
        method_args = ('meta_key','meta_value')

class SetPostMeta(AuthenticatedMethod):
        method_name = 'picassometa.setPostMeta'
        method_args = ('post_id', 'meta_struct')

class WPService(object):
    META_KEY = 'Nomer'
    _ratio = 0.85
    _taxonomies = {}   
    def __init__(self, params):
        self.params = params        
        self.client = Client(**self.params)
        #self.morph = pymorphy2.MorphAnalyzer()
    
    def get_normal_form_parser(self, parses):
        none_animacy = None        
        for item in parses:                      
            if item.tag.POS and item.tag.POS not in 'PREP':                
                if (item.normal_form == item.word and item.tag.animacy == 'inan') or item.tag.number == 'plur':                         
                    return item
                if item.tag.animacy is None:
                    none_animacy = item
        return none_animacy
            
    def inflect_depricated(self, name, case):
        import pymorphy2
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
        wp_cat = WordpressTaxonomyTree.objects.filter(parent__localities__id=locality_id, name__iexact=estate_type_name)[:1]    # @UndefinedVariable
        if wp_cat:
            return wp_cat.get()
        else:
            wp_cats = WordpressTaxonomyTree.objects.filter(localities__id=locality_id)  # @UndefinedVariable
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
                    return WordpressTaxonomyTree.objects.create(  # @UndefinedVariable
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
    
    def wrap_to_wp_category(self, taxonomy_tree):        
        cat = WordPressTerm()
        cat.taxonomy = 'category'
        cat.parent = taxonomy_tree.parent.wp_id if taxonomy_tree.parent else None
        cat.id = taxonomy_tree.wp_id
        return cat
    
    def render_post_category(self, estate):
        result = []        
        taxonomy_tree = self.get_or_create_category(estate)
        ancestors = taxonomy_tree.get_ancestors(ascending=True, include_self=True)
        for ancestor in ancestors:
            result.append(self.wrap_to_wp_category(ancestor))
        wp_cats = estate.estate_params.exclude(wp_taxons=None).values_list('wp_taxons__taxonomy_tree', flat=True)
        for wp_cat_id in wp_cats:
            if wp_cat_id:             
                params_taxonomy_tree = WordpressTaxonomyTree.objects.get(pk=wp_cat_id)            # @UndefinedVariable
                result.append(self.wrap_to_wp_category(params_taxonomy_tree))
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
        context['locality'] = u'в %s' % estate.locality.name_loct
        if estate.locality.locality_type_id != Locality.CITY:
            context['region'] = estate.locality.region.regular_name_gent
        basic_stead = estate.basic_stead
        if not estate.estate_category.is_stead and basic_stead and basic_stead.total_area_sotka:
            context['stead'] = u' на участке %g сот.' % basic_stead.total_area_sotka
        if estate.microdistrict:
            context['microdistrict'] = u', %s' % estate.microdistrict.name
        return u'%s' % template.render(Context(context))
    
    def render_seo_post_title(self, estate):
        result = u'Недвижимость %s'
        if estate.locality.locality_type_id == Locality.CITY:            
            result = result % estate.locality.name_gent            
        else:
            result = result % u'Краснодарского края'
        result = u'%s | %s в %s' % (result, estate.estate_type, estate.locality.name_loct)
        return result
    
    def render_post_tags(self, estate):
        locality = estate.locality  
        region = estate.locality.region
        result = set()
        result.add(u'купить %s в %s' % (estate.estate_type_accs, locality.name_loct))
        result.add(u'%s в %s' % (estate.estate_type, locality.name_loct))
        for beside in estate.entranceestate_set.filter(type=EntranceEstate.DISTANCE):
            result.add(u'%s у %s' % (estate.estate_type, beside.beside.name_gent))
            result.add(u'недвижимость на %s' % beside.beside.name_loct)
            result.add(beside.beside.name)
        result.add(u'%s в Краснодарском крае' % estate.estate_type)
        #result.add(u'%s %s' % (estate.estate_type, locality.name_gent))
        result.add(u'недвижимость %s' % locality.name_gent)
        result.add(u'купить недвижимость в %s' % locality.name_loct)
        result.add(u'недвижимость Краснодарского края')
        result.add(u'купить недвижимость в Краснодарском крае')
        result.add(u'купить %s в Краснодарском крае' % estate.estate_type_accs)
        result.add(locality.name)
        result.add(region.regular_name)
        result.add(u'недвижимость %s' % region.regular_name_gent)
        result.add(u'Краснодарский край')
        return list(result)
    
    def render_post_body(self, estate, description, images):        
        t = loader.get_template('reports/wp_post.html')
        c = Context({'estate_item':estate, 'description': description, 'images': images})
        rendered = t.render(c)
        return re.sub(r"\s+"," ", rendered)
    
    def get_estate_images(self, estate):
        from sorl.thumbnail import get_thumbnail        
        images = estate.images.all()[:4]
        if images:
            result = OrderedDict()
            for img in images:               
                im = get_thumbnail(img.image.file, '800x600')
                head, tail = os.path.split(im.name)  # @UnusedVariable                                
                result[os.path.join(im.storage.location,im.name)] = {'name': tail}                  
            return result
        
    def get_filtered_post_images(self, estate, post_id):
        estate_images = self.get_estate_images(estate)
        if not estate_images:
            return {}
        if not post_id:
            return {'estate_images' : estate_images}
        fltr = {'parent_id' : post_id}                
        media_items = self.client.call(GetMediaLibrary(fltr))       
        for key, image_data in estate_images.items():  # @UnusedVariable
            image_name = image_data['name']
            for item in media_items:                
                if type(item.metadata) == 'dict' and item.metadata.get('file'):
                    wp_image_name_no_ext = item.metadata.get['file']
                    estate_image_no_ext = os.path.splitext(image_name)[0][:-1]
                    if wp_image_name_no_ext.find(estate_image_no_ext) != -1:
                        image_data['wp_image'] = item                         
                        break                       
        ######
        #import logging
        #log = logging.getLogger('estate')
        #log.debug({'estate_images' : estate_images, 'same_items': same_items})
        ######
        return estate_images     

    def get_media_items(self, estate, post_id):
        data = {'type':'image/jpg', 'overwrite':False}
        estate_images = self.get_filtered_post_images(estate, post_id)       
        result = []
        if estate_images:
            for filepath, image_data in estate_images.items():
                if 'wp_image' in image_data:
                    result.append(image_data['wp_image'])
                else:
                    data['name'] = image_data["name"]                        
                    result.append(self.upload_image(filepath, data))
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
        wp_taxons = estate.estate_params.exclude(wp_taxons=None).values_list('wp_taxons__wp_postmeta_key', 'wp_taxons__wp_postmeta_value')
        for taxon in wp_taxons:             
            if taxon[0]:
                fields[taxon[0]] = taxon[1]  
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
            data['bits'] = xmlrpc_client.Binary(img.read())  # @UndefinedVariable

        response = self.client.call(media.UploadFile(data))
        return self.client.call(GetMediaItem(response['id']))
    def render_post_description(self, estate):
        region = u'Краснодарского края' if estate.locality.locality_type_id == Locality.CITY else estate.locality.region.regular_name_gent
        location = u'%s %s' % (estate.locality.name_loct, region)
        result = u'Продается %s в %s' % (estate.estate_type.lower(), location)             
        return result
    
    def get_custom_field_id(self, old_custom_fields, key):
        for field in old_custom_fields:
            if field.get('key') == key:
                return field.get('id')
    
    def assemble_post(self, estate, old_post, published=True):
        post = WordPressPost()
        post_id = None
        post.comment_status = 'open'
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
        post.date = estate.history.modificated - datetime.timedelta(hours=4)
        if published:
            post.post_status = 'publish'
        return post
    def sync_post(self, estate):
        try:
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
        except xmlrpclib.ProtocolError as err:
            wp_meta.error_message = prepare_err_msg(err)
            wp_meta.save()            
        except Exception, err:                       
            wp_meta.error_message = prepare_err_msg(err)
            wp_meta.status = EstateWordpressMeta.ERROR
            wp_meta.save()
        return False
        
    def sync_status(self, estate):        
        print('Processing %s' % estate)
        wp_meta, created = EstateWordpressMeta.objects.get_or_create(estate=estate)  # @UnusedVariable
        post_id = int(self.client.call(GetPostID(self.META_KEY,estate.id)))        
        print('Wordpress id %s' % post_id)        
        if post_id:                  
            wp_meta.post_id = post_id       
            try:            
                meta_struct = {'status' : estate.estate_status.wp_taxons.all()[:1].get().wp_id}            
                self.client.call(SetPostMeta(post_id, meta_struct))
                wp_meta.status = EstateWordpressMeta.UPTODATE
                wp_meta.save()                
            except xmlrpclib.ProtocolError as err:            
                wp_meta.error_message = prepare_err_msg(err)                
                wp_meta.save()                
            except Exception, err:            
                wp_meta.error_message = prepare_err_msg(err.errmsg)
                wp_meta.status = EstateWordpressMeta.STATUS_ERROR
                wp_meta.save()
        else:
            wp_meta.status = EstateWordpressMeta.OUT
            wp_meta.save()           
        
def prepare_err_msg(err):    
    s =  u"%s" % err
    print s
    return s[:255]