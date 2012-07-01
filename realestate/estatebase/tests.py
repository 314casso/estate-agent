"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
'''

from estatebase.models import Driveway

filename = '/home/picasso/coding/temp/load.txt'
lines = tuple(open(filename, 'r'))
for line in lines:
    e = Driveway(name=line)
    e.save() 
'''
import sys
path = '/home/picasso/django_workspace/estate-agent'
if path not in sys.path: 
    sys.path.append(path)

from estatebase.models import Driveway
from django.core import serializers
data = serializers.serialize( "python", [Driveway.objects.get(pk=1)])
print data
