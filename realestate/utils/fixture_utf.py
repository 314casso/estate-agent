#path = 'c://Users//picasso//My Documents//Aptana Studio 3 Workspace//estate-agent//realestate//'
import os
path = "/home/picasso/Documents/Aptana Studio 3 Workspace/estate-agent/realestate/"
os.system("./../manage.py dumpdata exportdata.feedlocality > temp.json")
#path = '/home/picasso/django_workspace/estate-agent/realestate/'
f = open("temp.json", 'rb').read().decode("unicode_escape").encode("utf8")
open("temp.json", 'wb').write(f)