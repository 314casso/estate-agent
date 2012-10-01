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
    template = \
'''{
    "pk": %(pk)s,
    "model": "%(model)s",
    "fields": {
        "name": "%(name)s",
        "region": "%(fk)s"        
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
        name, fk = ('', '')
        for line in lines:
            try:
                name, fk = line.split(';')
            except:
                pass    
            if len(name):            
                result.append(self.template % {'model':self.model_name,'pk':pk,'name':capfirst(name.strip()),'fk':fk})
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
Абрау-Дюрсо;3
Адербиевка;2
Анапа;1
Анапская;1
Артющенко;4
Архипо-Осиповка;2
Афонка;2
Ахтанизовская;4
Батарейка;4
Белый;4
Береговое;2
Береговой;4
Бетта;2
Благовещенская;1
Большие Хутора;3
Борисовка;3
Бужор;1
Варваровка;1
Васильевка;3
Верхнебаканский;3
Верхнее Джемете;1
Верхний Ханчакрак;1
Верхний Чекон;1
Веселая горка;1
Веселовка (Янтарь);4
Вестник;1
Виноградное;2
Виноградный;1
Виноградный;4
Витязево;1
Владимировка;3
Возрождение;2
Волна;4
Волна Революции;4
Воскресенский;1
Вышестеблиевская;4
Гайдук;3
Гайкодзор;1
Гаркуша;4
Геленджик;2
Глебовское;3
Голубицкая;4
Горный;3
Гостагаевская;1
Джанхот;2
Джемете;1
Джигинка;1
Дивноморское;2
Дюрсо;3
За Родину;4
Запорожская;4
Заря;1
Иваново;1
Ильич;4
Кабардинка;2
Капустино;1
Киблерово;1
Кирилловка;3
Красная Горка;1
Красная Скала;1
Красноармейский;4
Красный;1
Красный Курган;1
Красный Октябрь;4
Криница;2
Куматырь;1
Курбацкий;1
Курчанская;4
Кучугуры;4
Ленинский Путь;3
Лесничество Абрау-Дюрсо;3
Лиманный;1
Малый Разнокол;1
Малый Чекон;1
Марьина Роща;2
Михайловский Перевал;2
Мысхако;3
Натухаевская;3
Нижняя Гостагайка;1
Новороссийск;3
Павловка;1
Пересыпь;4
Песчаный;1
Победа;3
Прасковеевка;2
Приазовский;4
Приморский;4
Прогресс;4
Просторный;1
Пшада;2
Пятихатки;1
Раевская;3
Разнокол;1
Рассвет;1
Светлый;2
Светлый Путь;4
Северная Озереевка;3
Семигорский;3
Сенной;4
Соленый;4
Старотитаровская;4
Стрелка;4
Суворово-Черкесский;1
Сукко;1
Супсех;1
Таманский;4
Тамань;4
Тарусино;1
Текос;2
Темрюк;4
Тешебс;2
Убых;3
Усатова Балка;1
Уташ;1
Утриш;1
Фадеево;1
Федотовка;3
Фонталовская;4
Цемдолина;3
Цыбанобалка;1
Чекон;1
Чембурка;1
Черный;1
Широкая Балка;3
Широкая Пшадская Щель;2
Широкая Щель;2
Юбилейный;4
Южная Озереевка;3
Юровка;1
'''


MODEL = 'Locality'

import settings
import os

FIXTURE_ROOT = os.path.join(settings.SITE_ROOT, 'estatebase', 'fixtures')

fm = FixtureSimpleMaker('estatebase',MODEL,options)
fixfile = os.path.join(FIXTURE_ROOT, fm.fixfile)
if not os.path.isfile(fixfile):
    open(fixfile, 'wb').write('[\n%s\n]' % ','.join(fm.get_json()))
    print './manage.py loaddata %s' % fm.fixfile 
else:
    print 'Fixture already exists!'     



mm = ModelMaker('SimpleDict', 'estate_client_status')
print mm.get_model_code()