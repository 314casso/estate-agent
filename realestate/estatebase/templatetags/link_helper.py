from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def reverse_link(name, *args):
    return reverse(name, args=args)

