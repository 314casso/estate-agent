from django.db.models.signals import post_save, pre_save, post_delete
from django.db import transaction
from estatebase.models import Bidg, Stead, YES, EstateType, Estate,\
    prepare_history, Bid, Contact, EstateClient, Client, BidEvent

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

@transaction.commit_on_success        
def update_estate(sender, instance, created, **kwargs):
    if instance.client.history:
        prepare_history(instance.client.history, instance.user_id)
    if instance.client.pk:    
        for estate in instance.client.estates.all():
            estate.set_contact()
            estate.save()            
            prepare_history(estate.history, instance.user_id)                                

def update_localities(sender, instance, **kwargs):
    if instance.pk:
        if instance.regions.all().count() > 0 and not instance.localities.all().count() > 0:
            for region in instance.regions.all():
                localities = list(region.locality_set.values_list('id',flat=True))
                instance.localities = localities                 
                instance.cleaned_filter.update({'locality' : localities})                    

def bid_event_history(sender, instance, created, **kwargs):
    if created:
        post_save.disconnect(bid_event_history, sender=BidEvent)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(bid_event_history, sender=BidEvent)
    else:
        prepare_history(instance.history, instance._user_id)

def update_from_pickle(sender, instance, **kwargs):
    cleaned_data = instance.cleaned_filter
    if cleaned_data:
        instance.estates = cleaned_data['estates']
        instance.estate_types = cleaned_data['estate_type']
        instance.estate_categories = cleaned_data['estate_category']
        instance.regions = cleaned_data['region']            
        instance.localities = cleaned_data['locality']
        instance.agency_price_min = cleaned_data['agency_price'][0]                        
        instance.agency_price_max = cleaned_data['agency_price'][1]

def connect_signals():
    post_save.connect(prepare_estate_childs, sender=Estate)
    post_save.connect(set_validity, sender=Estate)
    post_save.connect(set_validity, sender=Bidg)
    post_save.connect(set_validity, sender=Stead)
    post_save.connect(update_deleted, sender=Client)
    post_save.connect(update_estate, sender=Contact)
    post_save.connect(estate_client_handler, sender=EstateClient)
    post_delete.connect(estate_client_handler, sender=EstateClient)
    pre_save.connect(update_localities, sender=Bid)
    pre_save.connect(update_from_pickle, sender=Bid)
    post_save.connect(bid_event_history, sender=BidEvent)
    
