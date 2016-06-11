# Create your views here.

from SimpleXMLRPCServer import SimpleXMLRPCDispatcher
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from xmlrpc.services import SpiderStoreService

# Create a Dispatcher; this handles the calls and translates info to function maps
#dispatcher = SimpleXMLRPCDispatcher() # Python 2.4
dispatcher = SimpleXMLRPCDispatcher(allow_none=True, encoding=None) # Python 2.5
 
@csrf_exempt
def rpc_handler(request):
        """
        the actual handler:
        if you setup your urls.py properly, all calls to the xml-rpc service
        should be routed through here.
        If post data is defined, it assumes it's XML-RPC and tries to process as such
        Empty post assumes you're viewing from a browser and tells you about the service.
        """

        if len(request.POST):
                response = HttpResponse(mimetype="application/xml")
                response.write(dispatcher._marshaled_dispatch(request.raw_post_data))
        else:
                response = HttpResponse()
                response.write("<b>This is an XML-RPC Service.</b><br>")
                response.write("You need to invoke it using an XML-RPC Client!<br>")
                response.write("The following methods are available:<ul>")
                methods = dispatcher.system_listMethods()

                for method in methods:
                        # right now, my version of SimpleXMLRPCDispatcher always
                        # returns "signatures not supported"... :(
                        # but, in an ideal world it will tell users what args are expected
                        sig = dispatcher.system_methodSignature(method)

                        # this just reads your docblock, so fill it in!
                        help =  dispatcher.system_methodHelp(method)  # @ReservedAssignment

                        response.write("<li><b>%s</b>: [%s] %s" % (method, sig, help))

                response.write("</ul>")
                response.write('<a href="http://www.djangoproject.com/"> <img src="http://media.djangoproject.com/img/badges/djangomade124x25_grey.gif" border="0" alt="Made with Django." title="Made with Django."></a>')

        response['Content-length'] = str(len(response.content))
        return response

def add_lot(item_dict):
    store_service = SpiderStoreService()    
    return store_service.add_lot(item_dict)
    
        
dispatcher.register_function(add_lot, 'add_lot')    