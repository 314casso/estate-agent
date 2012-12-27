# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from migrate_app.prop_map import PropMap
import os
from settings import MEDIA_ROOT
from django.db.models.aggregates import Count
from estatebase.models import Estate, Bid, Region, Contact
from estatebase.forms import BidPicleForm
from django.http import QueryDict
import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.contact_duplicates()
#        from django.utils import translation
#        translation.activate(settings.LANGUAGE_CODE)
#        
#        self.new_pickle()
#        self.test_func()        
    
    
    def contact_duplicates(self):
        contacts = Contact.objects.values('contact').annotate(dup=Count('contact')).filter(dup__gt=1).order_by('dup')
        for c in contacts:
            clist = Contact.objects.filter(contact=c['contact'])
            for contact in clist:
                print contact.client.pk,  contact.client
    
    def test_func(self):    
        #estates = Estate.objects.annotate(num_bidgs=Count('bidgs')).filter(num_bidgs__gt=1)        
        bids = Bid.objects.all()
        for e in bids:
            e.brokers.add(e.broker)            
            data = e.estate_filter
            if data:                  
                estate_filter_form = BidPicleForm(data)
                if estate_filter_form.is_valid():
                    if estate_filter_form['estate_category'].value():
                        e.estate_categories = estate_filter_form['estate_category'].value()                    
                        e.save() 
    
    def new_pickle(self):    
        #estates = Estate.objects.annotate(num_bidgs=Count('bidgs')).filter(num_bidgs__gt=1)        
        bids = Bid.objects.all()
        for e in bids:
            data = e.estate_filter
            if data:                  
                estate_filter_form = BidPicleForm(data)
                if estate_filter_form.is_valid():                   
                    e.cleaned_filter = estate_filter_form.cleaned_data                    
                    e.save()
                else:
                    print e.id
                    print estate_filter_form.errors


            
        
        
        
        
        
        
                      
        
          
            

        
