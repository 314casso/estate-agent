import xmlrpclib
import urllib2
from datetime import date
import time

def get_url_content(url):
        try:
            content = urllib2.urlopen(url)
            return content.read()
        except:
            print 'error! NOOOOOO!!!'
file_url = 'http://the path to your picture'
extension = file_url.split(".")
leng = extension.__len__()
extension = extension[leng-1]
if (extension=='jpg'):
    xfileType = 'image/jpeg'
elif(extension=='png'):
    xfileType='image/png'
elif(extension=='bmp'):
    xfileType = 'image/bmp'

file = get_url_content(file_url)
file = xmlrpclib.Binary(file)
server = xmlrpclib.Server('http://website.com/xmlrpc.php')
filename = str(date.today())+str(time.strftime('%H:%M:%S'))
mediarray = {'name':filename+'.'+extension, 
             'type':xfileType, 
             'bits':file, 
             'overwrite':'false'}
xarr = ['1', 'USERHERE', 'PASSWORDHERE', mediarray]
result = server.wp.uploadFile(xarr)
print result