from api.entity.productEntity import ProductEntity

def create_product(product_data):
    new_product = ProductEntity(
        name=product_data["name"],
        price=product_data["price"],
        quantity=product_data["quantity"],
        image=product_data["image"]
    )
    new_product.save()
    return {
        "id": str(new_product._id),
        "name": new_product.name,
        "price": new_product.price,
        "quantity": new_product.quantity,
        "image": new_product.image
    }

def get_product_by_id(id):
    product = ProductEntity.find_by_id(id)
    if product:
        return product.to_dictionary()
    return None

def get_all_products():
    return ProductEntity.get_all_products()

def update_product_quantity(product_id, quantity):
    return ProductEntity.update_quantity_product(product_id, quantity)

def get_product_price(product_id):
    product = ProductEntity.find_by_id(product_id)
    if product:
        return product.price
    return None