import datetime
from api.entity.orderEntity import OrderEntity
from api.entity.cartEntity import CartEntity
from api.entity.productEntity import ProductEntity

def add_new_order(user_id, products, total):
    date = datetime.datetime.now()
    cart = CartEntity.get_user_cart(user_id)
    if cart:
        CartEntity.delete_cart(cart._id)
        for product in products:
            ProductEntity.update_quantity_product(product["product_id"], product["quantity"])
    else:
        return None
    order = OrderEntity(user_id, products, total, date)
    order.save()
    return order.to_dictionary()