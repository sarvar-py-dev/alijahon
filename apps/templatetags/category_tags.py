from django import template

register = template.Library()


@register.filter(name='is_current_category')
def is_current_category(page, category=None):
    current_category = page.split('category/')[-1][:-1]
    if category is None:
        return current_category == ''
    return current_category == category.slug
