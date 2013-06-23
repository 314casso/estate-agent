from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import taxonomies

class WPService(object):
    _taxonomies = {}
    params = {
              'url':'http://www.domnatamani.ru/xmlrpc.php',
              'username':'xmlrpc_user',
              'password': '}^wA%d;py,)7{-K'
              }
    def __init__(self):
        self.client = Client(**self.params)
        
    def get_taxonomies(self, name='category'):
        if not name in self._taxonomies:            
            self._taxonomies[name] = self.client.call(taxonomies.GetTerms(name))
        return self._taxonomies[name]
    

