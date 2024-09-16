from django import template

register = template.Library()


@register.filter(name='is_current_category')
def is_current_category(page, category_slug=None):
    current_category = page.split('category/')[-1][:-1]
    if (category_slug is None and current_category == '') or current_category == category_slug:
        return 'active'
    return ''
