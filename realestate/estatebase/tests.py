"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import sys
sys.path.append('/home/picasso/django_workspace/estate-agent')

from estatebase.models import Watersupply, Gassupply, Sewerage, Telephony,\
    Internet, Driveway

filename = '/home/picasso/coding/temp/load.txt'
lines = tuple(open(filename, 'r'))
for line in lines:
    e = Driveway(name=line)
    e.save() 
