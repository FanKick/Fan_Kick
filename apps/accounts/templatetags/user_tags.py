from django import template

register = template.Library()

@register.filter
def user_is_role(user, role):
    return user.role == role
