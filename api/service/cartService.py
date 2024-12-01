from api.entity.cartEntity import CartEntity
from api.entity.productEntity import ProductEntity

def add_product_to_cart(user_id, product_id, quantity):
    product = ProductEntity.find_by_id(product_id)
    price = product.price
    cart = CartEntity.add_new_product_to_cart(user_id, product_id, quantity, price)
    return cart.to_dictionary()


def get_user_cart(user_id):
    cart = CartEntity.get_user_cart(user_id)
    if cart:
        return cart.to_dictionary()
    return None