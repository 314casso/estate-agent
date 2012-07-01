from django import http
from django.db import connection
from django.template import Template, Context
from django.contrib.auth.decorators import login_required
import re
import settings


class FilterPersistMiddleware(object):
    def process_request(self, request):
        
        if '/admin/' not in request.path:
            return None        
        if not request.META.has_key('HTTP_REFERER'):
            return None
                
        popup = 'pop=1' in request.META['QUERY_STRING']
        path = request.path
        query_string = request.META['QUERY_STRING']
        session = request.session
        
        if session.get('redirected', False):#so that we dont loop once redirected
            del session['redirected']
            return None

        referrer = request.META['HTTP_REFERER'].split('?')[0]
        referrer = referrer[referrer.find('/admin'):len(referrer)]
        key = 'key' + path.replace('/', '_')
        if popup:
            key = 'popup' + path.replace('/', '_')

        if path == referrer: #We are in same page as before
            if query_string == '': #Filter is empty, delete it
                if session.get(key, False):
                    del session[key]
                return None
            request.session[key] = query_string
        else: #We are are coming from another page, restore filter if available
            if session.get(key, False):
                query_string = request.session.get(key)
                redirect_to = path + '?' + query_string
                request.session['redirected'] = True
                return http.HttpResponseRedirect(redirect_to)
        return None

class RequireLoginMiddleware(object):
    def __init__(self):
        self.required = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.exceptions = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS_EXCEPTIONS])

    def process_view(self,request,view_func,view_args,view_kwargs):
        # No need to process URLs if user already logged in
        if request.user.is_authenticated(): return None
        # An exception match should immediately return None
        for url in self.exceptions:
            if url.match(request.path): return None
        # Requests matching a restricted URL pattern are returned 
        # wrapped with the login_required decorator
        for url in self.required:
            if url.match(request.path): return login_required(view_func)(request,*view_args,**view_kwargs)
        # Explicitly return None for all non-matching requests
        return None


    
class SQLLogMiddleware:
    def process_response (self, request, response): 
        time = 0.0
        for q in connection.queries: #@UndefinedVariable
            time += float(q['time'])
        
        t = Template('''
            <p><em>Total query count:</em> {{ count }}<br/>
            <em>Total execution time:</em> {{ time }}</p>
            <ul class="sqllog">
                {% for sql in sqllog %}
                    <li>{{ sql.time }}: {{ sql.sql }}</li>
                {% endfor %}
            </ul>
        ''')

        response.content = "%s%s" % (response.content, t.render(Context({'sqllog':connection.queries, 'count':len(connection.queries), 'time':time}))) #@UndefinedVariable
        return response
