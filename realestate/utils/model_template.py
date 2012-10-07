# -*- coding: utf-8 -*-
from django.utils.encoding import force_unicode

capfirst = lambda x: x and force_unicode(x)[0].upper() + force_unicode(x)[1:]

class ModelMaker(object):
    
    template = \
"""
class %(cname)s(SimpleDict):
    '''
    %(cname)s
    %(corig)s = models.ForeignKey(%(cname)s,verbose_name=_('%(cname)s'),%(cblank)s)
    '''
    class Meta(%(cmeta)s):
        verbose_name = _('%(cverb)s')
        verbose_name_plural = _('%(cverb_p)s')
"""
    
    def __init__(self,base_model,model_name,base_model_meta='parent'):
        self.base_model = base_model
        self.base_model_meta = base_model_meta
        self.model_name = model_name           
    def get_meta(self):
        if self.base_model_meta == 'parent':
            return '%s.Meta' % self.base_model
        else:
            return self.base_model_meta
    @property    
    def model_name_parts(self):
        return self.model_name.split('_')
    
    def get_params(self):
        cparam = {'cname':''}  
        for name in self.model_name_parts:
            cparam['cname'] += capfirst(name)            
        cparam['cmeta'] = self.get_meta()
        cparam['cverb'] = capfirst(' '.join(self.model_name_parts))    
        cparam['cverb_p'] = '%ss' % cparam['cverb']
        cparam['corig'] = self.model_name
        cparam['cblank'] = 'blank=True,null=True'
        return cparam    
    
    def get_model_code(self):
        return self.template % self.get_params()


class FixtureSimpleMaker(object):
    c_template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(name)s",
        "order": "%(pk)s"                
    }
}'''
    template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(0)s",
        "estate_type_category": "%(1)s",
        "has_bidg": "%(2)s",
        "has_stead": "%(3)s",
        "template": "%(4)s",
        "placeable": "%(5)s",        
        "order": "%(pk)s"
    }
}'''    
    
    def __init__(self,app_name,model_name,name_list):
        self.model_name = '%s.%s' % (app_name.lower(), model_name.lower())        
        self.name_list = name_list
        self.fixfile = '%s.json' % model_name.lower()    
    def get_json(self):
        pk = 1
        result = []
        lines = self.name_list.splitlines()
        lines = sorted(lines)
        fields = None
        json_fields ={}        
        for line in lines:            
            try:                
                if line: 
                    fields = line.split(';')                    
                    for ind, val in enumerate(fields):
                        json_fields['%s' % ind] = ind == 0 and capfirst(val.strip()) or val.strip()                  
            except:                
                pass    
            if len(json_fields):                
                template_dict = {'model':self.model_name,'pk':pk}
                template_dict.update(json_fields)                             
                result.append(self.template % template_dict)
                pk += 1   
        return result


'''
Загрузить все файлы
find . -name "*.json" -exec manage.py loaddata {} \;

Регулярка для вытаскивания опций их списка select
^.*>(.*)<\/.*$
\1
'''

options = \
'''
дом;2;1;1;2;1
полдома;2;1;1;2;1
дача;2;1;1;2;0
сельскохозяйственного назначения;8;0;1;3;0
дачный;8;0;1;3;0
коммерческого назначения;8;0;1;3;0
для строительства жилого дома;8;0;1;3;0
комната;4;2;0;0;0
малосемейка;4;2;0;0;0
новостройка;4;2;0;1;0
вторичка;4;2;0;0;0
квартира с участком;5;1;1;0;1
коттедж;5;1;1;0;1
таунхаус;5;1;1;0;1
гостевой дом;6;1;2;2;1
минигостиница;6;1;2;2;1
гостиница;6;1;2;2;1
строение для отдыхающих;6;1;2;2;1
магазин;6;1;2;2;1
торговый павильон;6;1;2;2;1
пансионат;6;1;2;2;1
база отдыха;6;1;2;2;1
производственная база;6;1;2;2;1
офис;6;1;2;2;1
нежилое помещение;6;1;2;0;1
гостевые комнаты;6;1;2;2;1
винзавод;6;1;2;2;1
хозяйственные постройки;7;1;1;4;1
баня;7;1;1;4;1
летняя кухня;7;1;1;4;1
гараж ;7;1;1;4;1
летний дом;7;1;1;4;1
времянка;7;1;1;4;1
мастерская;7;1;1;4;1
хозблок;7;1;1;4;1
летняя кухня;7;1;1;4;1
фундамент;7;1;1;4;1
подвал;7;1;1;4;1
погреб;7;1;1;4;1
ветхий дом;7;1;1;4;1
недострой;7;1;1;4;1
забор;7;1;1;4;1
навес;7;1;1;4;1
стоянка;7;1;1;4;1
летний душ;7;1;1;4;1
уборная;7;1;1;4;1
колодец;7;1;1;4;1
сад;7;1;1;4;1
гараж;1;1;2;4;1
гараж лодочный;1;1;2;4;1
'''


MODEL = 'EstateType'

import settings
import os

FIXTURE_ROOT = os.path.join(settings.SITE_ROOT, 'estatebase', 'fixtures')

fm = FixtureSimpleMaker('estatebase',MODEL,options)
fixfile = os.path.join(FIXTURE_ROOT, fm.fixfile)
if not os.path.isfile(fixfile):
    open(fixfile, 'wb').write('[\n%s\n]' % ','.join(fm.get_json()))
    print './manage.py loaddata %s' % fm.fixfile 
else:
    print ','.join(fm.get_json())
    print 'Fixture already exists!'     



mm = ModelMaker('SimpleDict', 'estate_client_status')
print mm.get_model_code()