from django import template

register = template.Library()


@register.filter
def review_user(value, arg):
    for review in value.review_set.all():
        if review.user == arg:
            return True
    return False