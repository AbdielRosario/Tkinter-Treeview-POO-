"""Gestiona el almacenamiento en memoria de los productos."""

from uuid import UUID

from models.product import Product


class ProductRepository:
    def __init__(self) -> None:
        self._products: list[Product] = []

    def find_all(self) -> list[Product]:
        """Retorna todos los productos registrados."""
        return list(self._products)

    def create_one(self, product: Product) -> None:
        self._products.append(product)

    def update_one(
        self,
        product_id: UUID,
        name: str,
        price: float,
        available_quantity: int,
    ) -> bool:
        for product in self._products:
            if product.id == product_id:
                product.name = name
                product.price = price
                product.available_quantity = available_quantity
                return True
        return False

    def delete_one(self, product_id: UUID) -> bool:
        for index, product in enumerate(self._products):
            if product.id == product_id:
                del self._products[index]
                return True
        return False
