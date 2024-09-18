# app1/templatetags/custom_filters.py
from django import template
from app1.models import CustomUser, Post

register = template.Library()

@register.filter(name='is_instance')
def is_instance(value, class_name):
    if class_name == 'CustomUser':
        return isinstance(value, CustomUser)
    elif class_name == 'Post':
        return isinstance(value, Post)
    return False
