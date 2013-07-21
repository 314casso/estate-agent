# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from estatebase.models import Locality, Region
from django.db.models.signals import pre_save, post_save, m2m_changed
from wp_helper.service import WPService
from django.dispatch.dispatcher import receiver
from django.db.utils import IntegrityError

class WordpressTaxonomyTree(MPTTModel):
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10, unique=True)  
    wp_parent_id = models.CharField('WP parent Id', max_length=10, null=True, blank=True,) 
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    up_to_date = models.BooleanField()
    regions = models.ManyToManyField(Region, verbose_name=_('Region'), blank=True, null=True, related_name='wp_taxons')    
    localities = models.ManyToManyField(Locality, verbose_name=_('Locality'), blank=True, null=True, related_name='wp_taxons')
    wp_meta_key = models.CharField('WP meta key', max_length=10, blank=True, null=True)   
    def __unicode__(self):
        return u'%s' % (self.name,)
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:        
        verbose_name = u'Рубрика'
        verbose_name_plural = u'Рубрики'    

class WordpressMeta(models.Model):    
    LOCALITY = 1    
    METATYPE_CHOICES = (
        (LOCALITY, u'Населенные пункты'),        
    )
    name = models.CharField('Name', max_length=150)
    wp_id = models.CharField('WP Id', max_length=10, unique=True)
    wordpress_meta_type = models.IntegerField(choices=METATYPE_CHOICES)
    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
        verbose_name = u'Жесткое поле'
        verbose_name_plural = u'Жесткие поля'

def load_data(data, wordpress_meta_type_id):   
    list_r = data.split(',')
    for item in list_r:
        key,value = item.split(':')
        WordpressMeta.objects.create(wp_id=key.strip(), name=value.strip(), wordpress_meta_type_id=wordpress_meta_type_id)

def check_localities():
    ar = [x.lower() for x in WordpressTaxonomyTree.objects.values_list('name',flat=True)]
    #ar = [x.lower() for x in WordpressMeta.objects.filter(wordpress_meta_type=WordpressMeta.LOCALITY).values_list('name',flat=True)]
    locs = Locality.objects.values_list('name',flat=True)
    import difflib     
    print '+++++++++++++++++++++++++++++++++++++++++++++++++++++'
    for l in locs:         
        d = difflib.get_close_matches(l.lower(), ar)
        if d:            
            print '%s=%s' % (l,d[0])
            pass
        else:
            print '%s=%s' % (l,'*' * 20)


@receiver(m2m_changed, sender=WordpressTaxonomyTree.localities.through)
def unique_locality(sender, instance, **kwargs):    
    action = kwargs.get('action', None)
    localities = kwargs.get('pk_set', None)
    if action == 'pre_add':
        for locality in localities:
            same_taxonomy = list(WordpressTaxonomyTree.objects.filter(localities=locality))
            if same_taxonomy:                
                raise IntegrityError(u'Населенный пункт c кодом [%s] уже привязан к рубрике "%s" с кодом [%s]' % (locality, same_taxonomy[0].name, same_taxonomy[0].id))
            
def sync_wp_taxonomy(sender, instance, **kwargs):
    pre_save.disconnect(sync_wp_taxonomy, sender=WordpressTaxonomyTree, dispatch_uid='sync_wp_taxonomy')        
    wp_service = WPService()
    if not instance.id:
        print u'Creating... %s' %  instance
        try:
            wp_id = wp_service.create_taxonomy(instance.parent.wp_id if instance.parent else None, instance.name)
        except:
            pass
        if wp_id:
            instance.up_to_date = True
            instance.wp_id = wp_id
            instance.wp_parent_id = instance.parent.wp_id
            instance.save()                 
    else:
        print u'Updating... %s' % instance.parent.wp_id       
    pre_save.connect(sync_wp_taxonomy, sender=WordpressTaxonomyTree, dispatch_uid='sync_wp_taxonomy')    

#pre_save.connect(sync_wp_taxonomy, sender=WordpressTaxonomyTree, dispatch_uid='sync_wp_taxonomy')

#check_localities()

#reg = u":Все, 1:___Анапа___, 2:Анапская, 8:Благовещенская, 9:Бужор, 10:Варваровка, 12:Веселая горка, 14:Вестник, 15:Виноградный, 16:Витязево, 19:Воскресенский, 21:Гайкодзор, 24:Гостагаевская, 44:Нижняя Гостагайка, 25:Джемете, 11:Верхнее Джемете, 26:Джигинка, 29:Заря, 30:Иваново, 32:Капустино, 33:Киблерово, 34:Красная Горка, 36:Красный, 37:Красный Курган, 39:Куматырь, 40:Курбацкий, 43:Лиманный, 45:Павловка, 47:Песчаный, 51:Просторный, 52:Пятихатки, 54:Рассвет, 53:Разнокол, 60:Суворово-Черкесский, 61:Сукко, 62:Супсех, 65:Тарусино, 67:Усатова Балка, 68:Уташ, 69:Утриш, 71:Цыбанобалка, 72:Чекон, 73:Чембурка, 74:Черный, 76:Юровка, 66:___Темрюк___, 3:Артющенко, 4:Ахтанизовская, 5:Батарейка, 6:Белый, 7:Береговой, 13:Веселовка (Янтарь), 123:Виноградный, 17:Волна, 18:Волна Революции, 20:Вышестеблиевская, 22:Гаркуша, 23:Голубицкая, 27:За Родину, 28:Запорожская, 31:Ильич, 35:Красноармейский, 38:Красный Октябрь, 41:Курчанская, 42:Кучугуры, 46:Пересыпь, 48:Приазовский, 49:Приморский, 50:Прогресс, 55:Светлый Путь, 56:Сенной, 57:Соленый, 58:Старотитаровская, 59:Стрелка, 63:Таманский, 64:Тамань, 70:Фонталовская, 75:Юбилейный, 77:___Новороссийск___, 93:Абрау-Дюрсо, 94:Большие Хутора, 78:Борисовка, 79:Васильевка, 99:Верхнебаканский, 80:Владимировка, 101:Гайдук, 81:Глебовское, 100:Горный, 95:Дюрсо, 96:Камчатка, 82:Кирилловка, 86:Ленинский Путь, 97:Лесничество Абрау-Дюрсо, 90:Мысхако, 85:Натухаевская, 89:Победа, 88:Раевская, 98:Северная Озереевка, 87:Семигорский, 83:Убых, 91:Федотовка, 92:Широкая Балка, 84:Южная Озереевка, 102:___Геленджик___,  103:Адербиевка, 104:Архипо-Осиповка, 105:Афонка, 106:Береговое, 107:Бетта, 108:Виноградное, 109:Возрожение, 110:Джанхот, 111:Дивноморское, 112:Кабардинка, 113:Криница, 114:Марьина Роща, 115:Михайловский Перевал, 116:Прасковеевка, 117:Пшада, 118:Светлый, 119:Текос, 120:Тешебс, 121:Широкая Пшадская Щель, 122:Широкая Щель"
#load_data(reg, 1)