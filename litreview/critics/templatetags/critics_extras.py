from django import template

register = template.Library()


@register.filter
def is_review_user(value, arg):
    """ Vérifier si un utilisateur a publié une critique """
    for review in value.review_set.all():
        if review.user == arg:
            return True
    return False


@register.filter
def model_type(value):
    """ Retourner le nom de l'objet """
    return type(value).__name__
