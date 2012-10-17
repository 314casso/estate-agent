#path = 'c://Users//picasso//My Documents//Aptana Studio 3 Workspace//estate-agent//realestate//'
path = '/home/picasso/django_workspace/estate-agent/realestate/'
f = open("%stemp1.json" % path, 'rb').read().decode("unicode_escape").encode("utf8")
open("%stemp1.json" % path, 'wb').write(f)