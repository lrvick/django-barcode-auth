from django import template
from django.template.defaultfilters import stringfilter
from utils import gen_passhash

register = template.Library()

@register.filter
@stringfilter
def barcode_hash(value):
    passhash = gen_passhash(value)
    return passhash
barcode_hash.is_safe = True
