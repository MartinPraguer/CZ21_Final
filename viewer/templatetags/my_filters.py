from django import template

register = template.Library()

@register.filter
def price_format(value):
    try:
        # Nejprve zkuste hodnotu převést na float
        value = float(value)
        return f"{value:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        # Pokud převod na číslo selže, vraťte původní hodnotu
        return value