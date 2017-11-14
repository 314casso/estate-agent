from django.db.models.signals import post_save, pre_save, post_delete,\
    m2m_changed
from estatebase.models import Bidg, Stead, YES, EstateType, Estate,\
    prepare_history, Bid, Contact, EstateClient, Client, BidEvent, EstateParam,\
    Layout, EntranceEstate, EstatePhoto
from datetime import datetime    

def save_estate(sender, instance, created, **kwargs):    
    if hasattr(instance.level, 'bidg'):
        instance.level.bidg.estate.save()

def prepare_estate_childs(sender, instance, created, **kwargs):
    if created:
        estate_type = getattr(instance,'_estate_type_id', None) and EstateType.objects.get(pk=instance._estate_type_id) or None                
        if estate_type:             
            if estate_type.estate_type_category.has_bidg == YES:
                Bidg.objects.create(estate=instance, estate_type=estate_type, basic=True)
            if estate_type.estate_type_category.has_stead == YES:
                stead_type_id = instance.estate_category.is_stead and estate_type.pk or Stead.DEFAULT_TYPE_ID 
                Stead.objects.create(estate=instance, estate_type_id=stead_type_id)          

def set_validity(sender, instance, created, **kwargs):
    estate = getattr(instance,'estate',instance) 
    post_save.disconnect(set_validity, sender=Estate)
    estate.set_validity(estate.check_validity())
    estate.save()
    post_save.connect(set_validity, sender=Estate)

def estate_client_handler(sender, instance, **kwargs):
    try:     
        instance.estate.set_contact()
        instance.estate.save()
    except Estate.DoesNotExist:
        pass

def update_deleted(sender, instance, created, **kwargs):
    if instance.deleted:                     
        for estate in instance.estates.all():
            estate.set_contact()
            estate.save()            
            prepare_history(estate.history, instance._user_id)                                
       
def update_estate(sender, instance, created, **kwargs):
    if instance.client.history:
        prepare_history(instance.client.history, instance.user_id)
    if instance.client.pk:    
        for estate in instance.client.estates.all():
            estate.set_contact()
            estate.save()            
            prepare_history(estate.history, instance.user_id)                                

def update_estate_m2m(sender, instance, created, **kwargs):
    user = instance.user if hasattr(instance, 'user') else instance.estate.history.updated_by 
    prepare_history(instance.estate.history, user)
    estate_wp_meta_base(instance.estate) 

def bid_event_history(sender, instance, created, **kwargs):
    if created:
        post_save.disconnect(bid_event_history, sender=BidEvent)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(bid_event_history, sender=BidEvent)
    else:
        prepare_history(instance.history, instance._user_id)
    prepare_history(instance.bid.history, instance._user_id)

def update_from_pickle(sender, instance, **kwargs):
    cleaned_data = instance.cleaned_filter    
    if cleaned_data:
        if 'estates' in cleaned_data:
            instance.estates = cleaned_data['estates']
        if 'estate_type' in cleaned_data:    
            instance.estate_types = cleaned_data['estate_type']
         
        if 'estate_category' in cleaned_data:     
            instance.estate_categories = cleaned_data['estate_category']
        if 'region' in cleaned_data:
            instance.regions = cleaned_data['region']
        if 'locality' in cleaned_data:                  
            instance.localities = cleaned_data['locality']
        if 'agency_price' in cleaned_data:
            instance.agency_price_min = cleaned_data['agency_price'][0]                        
            instance.agency_price_max = cleaned_data['agency_price'][1]

def estate_wp_meta_base(estate):
    from wp_helper.models import EstateWordpressMeta
    post_on_site = len(estate.estate_params.filter(pk=EstateParam.POSTONSITE)) > 0
    if estate.correct and post_on_site:   
        wp_meta, created = EstateWordpressMeta.objects.get_or_create(estate=estate)  # @UnusedVariable
        wp_meta.status = EstateWordpressMeta.XMLRPC
        wp_meta.save()
    else:
        try:
            wp_meta = EstateWordpressMeta.objects.get(estate=estate)
        except EstateWordpressMeta.DoesNotExist:
            return
        wp_meta.status = EstateWordpressMeta.UNKNOWN
        wp_meta.save()

def estate_wp_meta(sender, instance, **kwargs):
    estate_wp_meta_base(instance)

def estate_param_wp_meta(sender, instance, **kwargs):
    estate_wp_meta_base(instance)

def update_geo(sender, instance, **kwargs):
    geo_groups = set()    
    for r in instance.regions.all():        
        geo_groups.add(r.geo_group_id)    
    for l in instance.localities.all():        
        geo_groups.add(l.region.geo_group_id)            
    instance.geo_groups = geo_groups


def update_status(sender, instance, **kwargs):    
    instance.update_state()
    
#     BID_EXPIRED = datetime(2015, 12, 1)
#     if instance.history.modificated < BID_EXPIRED:
#         instance.state = Bid.PENDING
#         return
    

def connect_signals():
    post_save.connect(prepare_estate_childs, sender=Estate)
    post_save.connect(set_validity, sender=Estate)
    post_save.connect(set_validity, sender=Bidg)
    post_save.connect(set_validity, sender=Stead)
    post_save.connect(update_deleted, sender=Client)
    post_save.connect(update_estate, sender=Contact)
    post_save.connect(estate_client_handler, sender=EstateClient)
    post_delete.connect(estate_client_handler, sender=EstateClient)
    post_save.connect(update_geo, sender=Bid) # @UndefinedVariable
    pre_save.connect(update_from_pickle, sender=Bid)
    post_save.connect(update_status, sender=Bid)
    post_save.connect(bid_event_history, sender=BidEvent)
    post_save.connect(estate_wp_meta, sender=Estate)
    m2m_changed.connect(estate_param_wp_meta, sender=Estate.estate_params.through)  # @UndefinedVariable
    post_save.connect(update_estate_m2m, sender=EntranceEstate)  # @UndefinedVariable    
    post_save.connect(update_estate_m2m, sender=EstatePhoto)  # @UndefinedVariable
    post_save.connect(save_estate, sender=Layout)
    
    

    
