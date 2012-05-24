from django import template

register = template.Library()

@register.inclusion_tag('close_btn.html')
def close_btn(url):
    return {'url': url}