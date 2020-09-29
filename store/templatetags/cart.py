from django import template
register = template.Library()

@register.filter(name="Is_In_Cart")
def is_in_cart(product1, cart1):
    keys = cart1.keys()
    for id in keys:
        if int(id) == product1.id:
            return True
    return False

@register.filter(name="Cart_Quantity")
def cart_quantity(product1, cart1):
    keys = cart1.keys()
    for id in keys:
        if int(id) == product1.id:
            return cart1.get(id)             #return quantity
    return False

@register.filter(name="Price_Total")
def price_total(product1, cart1):
   return product1.product_sell_price * cart_quantity(product1, cart1)

@register.filter(name='Total_Cart_Price')
def total_cart_price(products_all, cart):
    sum = 0;
    for product1 in products_all:
        sum = sum + price_total(product1, cart)
    return sum
