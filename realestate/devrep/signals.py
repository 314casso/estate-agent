from django.db.models.signals import post_save
from estatebase.models import prepare_history
from devrep.models import Partner

def partner_history(sender, instance, created, **kwargs):
    if created or not instance.history:
        post_save.disconnect(partner_history, sender=Partner)
        instance.history = prepare_history(None, instance._user_id)
        instance.save()
        post_save.connect(partner_history, sender=Partner)
    else:
        prepare_history(instance.history, instance._user_id)
        
        
def connect_signals():    
    post_save.connect(partner_history, sender=Partner)