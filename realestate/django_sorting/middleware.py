def get_fields(self):
    try:
        fields = self.REQUEST['sort'].split(',')
    except (KeyError, ValueError, TypeError):
        fields = []
    direction = self.direction == 'desc' and '-' or ''
    return ['%s%s' % (direction, field) for field in fields]

def get_direction(self):
    try:
        return self.REQUEST['dir']
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