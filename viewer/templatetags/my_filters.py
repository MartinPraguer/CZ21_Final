from django import template

register = template.Library()

@register.filter
def price_format(value):
    # Zformátuje číslo s tečkou jako oddělovačem tisíců
    return f"{value:,.0f}".replace(",", ".")