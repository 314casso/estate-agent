def get_request_dict(request):
    if not request:
        return
    if request.method == 'GET':
        return request.GET 
    elif request.method == 'POST':
        return request.POST
    

def get_fields(self):
    request = get_request_dict(self)
    try:
        fields = request['sort'].split(',')
    except (KeyError, ValueError, TypeError):
        fields = []
    direction = self.direction == 'desc' and '-' or ''
    return ['%s%s' % (direction, field) for field in fields]


def get_direction(self):
    request = get_request_dict(self)
    try:
        return request['dir']
    except (KeyError, ValueError, TypeError):
        return 'desc'


class SortingMiddleware(object):
    """
    Inserts a variable representing the field (with direction of sorting)
    onto the request object if it exists in either **GET** or **POST**
    portions of the request.
    """
    def process_request(self, request):
        request.__class__.fields = property(get_fields)
        request.__class__.direction = property(get_direction)