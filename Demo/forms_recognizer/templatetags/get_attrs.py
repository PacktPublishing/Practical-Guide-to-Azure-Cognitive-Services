from django import template

register = template.Library()


@register.filter
def get_obj_attr(obj, attr):
    return obj[attr]
