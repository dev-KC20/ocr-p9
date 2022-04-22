from django import template

register = template.Library()


@register.filter()
def range_star(default=5):
    return range(1, default + 1, 1)
