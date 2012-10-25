#path = 'c://Users//picasso//My Documents//Aptana Studio 3 Workspace//estate-agent//realestate//'
#import os
#os.system("./manage.py dampdata estatebase.office > temp.json")
path = '/home/picasso/django_workspace/estate-agent/realestate/'
f = open("%stemp.json" % path, 'rb').read().decode("unicode_escape").encode("utf8")
open("%stemp.json" % path, 'wb').write(f)