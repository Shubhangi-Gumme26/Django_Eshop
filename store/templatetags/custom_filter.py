from django import template
register = template.Library()

@register.filter(name="Currency")
def currency(amount):
    return "Rs. " + str(amount)

@register.filter(name="Multiply")
def multiply(amount, number):
    return amount * number