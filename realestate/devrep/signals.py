from django.db.models.signals import post_save
from estatebase.models import prepare_history
from devrep.models import Partner, DevProfile

def common_history(sender, instance, created, **kwargs):
    if created or not instance.history:
        post_save.disconnect(common_history, sender=sender)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(common_history, sender=sender)
    else:
        prepare_history(instance.history, instance._user_id)
                        
def connect_signals():    
    post_save.connect(common_history, sender=Partner)
    post_save.connect(common_history, sender=DevProfile)