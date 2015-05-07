from django.db.models.signals import post_save, pre_save
from estatebase.models import prepare_history
from devrep.models import Partner, DevProfile, WorkTypeProfile
from django.dispatch.dispatcher import receiver


def common_history(sender, instance, created, **kwargs):
    if created or not instance.history:
        post_save.disconnect(common_history, sender=sender)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(common_history, sender=sender)
    else:
        prepare_history(instance.history, instance._user_id)

@receiver(pre_save, sender=WorkTypeProfile)
def worktype_populate_handler(sender, instance, *args, **kwargs):
    if not instance.measure and instance.work_type.measure:
        instance.measure = instance.work_type.measure
    if not instance.quality and instance.dev_profile.quality: 
        instance.quality = instance.dev_profile.quality    
    if not instance.experience and instance.dev_profile.experience: 
        instance.experience = instance.dev_profile.experience

                        
def connect_signals():    
    post_save.connect(common_history, sender=Partner)
    post_save.connect(common_history, sender=DevProfile)