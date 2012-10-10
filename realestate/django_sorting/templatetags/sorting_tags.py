# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from django.utils.translation import ugettext as _

register = template.Library()

DEFAULT_SORT_UP = getattr(settings, 'DEFAULT_SORT_UP' , '&uarr;')
DEFAULT_SORT_DOWN = getattr(settings, 'DEFAULT_SORT_DOWN' , '&darr;')
INVALID_FIELD_RAISES_404 = getattr(settings,
        'SORTING_INVALID_FIELD_RAISES_404' , True)

sort_directions = {
    'asc': {'icon':DEFAULT_SORT_UP, 'inverse': 'desc'},
    'desc': {'icon':DEFAULT_SORT_DOWN, 'inverse': 'asc'},
    '': {'icon':DEFAULT_SORT_DOWN, 'inverse': 'asc'},
}

MESSAGE_404 = """Invalid field sorting. If DEBUG were set to 
                 False, an HTTP 404 page would have been shown instead."""

def anchor(parser, token):
    """
    Parses a tag that's supposed to be in this format: {% anchor fields title %}
    Title may be a "string", _("trans string"), or variable
    """
    bits = [b for b in token.split_contents()]
    if len(bits) < 2:
        raise template.TemplateSyntaxError("anchor tag takes at least 1 argument")

    title_is_var = False
    try:
        title = bits[2]
        if title[0] in ('"', "'"):
            if title[0] == title[-1]:
                title = title[1:-1]
            else:
                raise template.TemplateSyntaxError(
                    'anchor tag title must be a "string", _("trans string"), or variable')
        elif title.startswith('_("') or title.startswith("_('"):
            title = _(title[3:-2])
        else:
            title_is_var = True
    except IndexError:
        title = bits[1].capitalize()

    return SortAnchorNode(bits[1].strip(), title.strip(), title_is_var)


class SortAnchorNode(template.Node):
    """
    Renders an <a> HTML tag with a link which href attribute 
    includes the fields on which we sort and the direction.
    and adds an up or down arrow if the fields is the one 
    currently being sorted on.

    Eg.
        {% anchor name Name %} generates
        <a href="/the/current/path/?sort=name" title="Name">Name</a>

        {% anchor name,title Name %} generates
        <a href="/the/current/path/?sort=name,title" title="Name">Name</a>
    """
    def __init__(self, fields, title, title_is_var):
        self.fields = fields
        self.title = title
        self.title_is_var = title_is_var

    def render(self, context):
        if self.title_is_var:
            self.title = context[self.title]
        request = context['request']
        getvars = request.GET.copy()

        if 'sort' in getvars:
            sortby = getvars['sort']
            del getvars['sort']
        else:
            sortby = ''

        if 'dir' in getvars:
            sortdir = getvars['dir']
            del getvars['dir']
        else:
            sortdir = ''

        if sortby == self.fields:
            getvars['dir'] = sort_directions[sortdir]['inverse']
            icon = sort_directions[sortdir]['icon']
        else:
            icon = ''

        if len(getvars.keys()) > 0:
            urlappend = "&%s" % getvars.urlencode()
        else:
            urlappend = ''

        if icon:
            title = "%s %s" % (self.title, icon)
        else:
            title = self.title

        url = '%s?sort=%s%s' % (request.path, self.fields, urlappend)
        return '<a href="%s" title="%s">%s</a>' % (url, self.title, title)


anchor = register.tag(anchor)