from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc.wordpress import WordPressTerm
import difflib
from wordpress_xmlrpc import AnonymousMethod

class GetPostID(AnonymousMethod):
        method_name = 'picassometa.getPostID'
        method_args = ('meta_key','meta_value')

class WPService(object):
    META_KEY = 'Nomer'
    _ratio = 0.85
    _taxonomies = {}
    params = {
              'url':'http://www.domnatamani.ru/xmlrpc.php',
              'username':'xmlrpc_user',
              'password': '}^wA%d;py,)7{-K'
              }
    
#     params = {
#               'url':'http://localhost/wordpress/xmlrpc.php',
#               'username':'admin',
#               'password': '123'
#               }
    
    def __init__(self):
        self.client = Client(**self.params)
        
    def get_taxonomies(self, name='category'):
        if not name in self._taxonomies:            
            self._taxonomies[name] = self.client.call(taxonomies.GetTerms(name))
        return self._taxonomies[name]
    def create_taxonomy(self, parent_cat_id, name, taxonomy='category'):
        child_cat = WordPressTerm()
        child_cat.taxonomy = taxonomy
        if parent_cat_id:
            child_cat.parent = parent_cat_id
        child_cat.name = name
        child_cat.id = self.client.call(taxonomies.NewTerm(child_cat))
        return child_cat.id
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
    
        
            
        
        


        
    

