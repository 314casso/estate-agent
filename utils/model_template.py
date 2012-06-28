# -*- coding: utf-8 -*-
from django.utils.encoding import smart_str, force_unicode
base_model = 'SimpleDict'
base_model_meta = 'parent'
model_name = 'ceiling'


def get_meta():
    if base_model_meta == 'parent':
        return '%s.Meta' % base_model
    else:
        return base_model_meta

model_name_parts = model_name.split('_')
capfirst = lambda x: x and force_unicode(x)[0].upper() + force_unicode(x)[1:]
cparam = {'cname':''}  
for name in model_name_parts:
    cparam['cname'] += capfirst(name)
    
cparam['cmeta'] = get_meta()
cparam['cverb'] = capfirst(' '.join(model_name_parts))    
cparam['cverb_p'] = '%ss' % cparam['cverb']
    

class_template = """
class %(cname)s(SimpleDict):
    '''
    %(cname)s
    '''
    class Meta(%(cmeta)s):
        verbose_name = _('%(cverb)s')
        verbose_name_plural = _('%(cverb_p)s')
"""

print class_template % cparam