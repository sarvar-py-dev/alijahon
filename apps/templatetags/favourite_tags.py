from django import template

register = template.Library()


@register.filter()
def is_liked(user, product):
    return user.is_authenticated and user.favourites.all().filter(product=product).exists()
