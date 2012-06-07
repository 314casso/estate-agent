from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def reverse_link(name, *args):
    return reverse(name, args=args)

@register.inclusion_tag('close_btn.html')
def close_btn(url):        
    return {'url': url or ''}

@register.inclusion_tag('contact_list_tag.html')
def contact_list(client, next_url):        
    return {'client': client, 'next_url': next_url}
