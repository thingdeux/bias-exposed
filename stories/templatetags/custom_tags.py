from django import template
from django.template.defaultfilters import stringfilter
import json

register = template.Library()


@register.filter
def get_item_json(dictionary, key):
    data = dictionary.get(key)
    return json.dumps(data)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
