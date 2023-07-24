from django import template

register = template.Library()

@register.filter
def leading_zero(value):
    # Проверяем, является ли значение числом и однозначным
    if isinstance(value, int) and value < 10 and value > 0:
        return f'0{value}'
    return value