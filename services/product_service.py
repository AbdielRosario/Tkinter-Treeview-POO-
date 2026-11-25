"""Contiene la lógica de negocio de los productos."""

from uuid import UUID

from models.product import Product
from repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, repository: ProductRepository) -> None:
        self.repository = repository

    def find_all(self) -> list[Product]:
        return self.repository.find_all()

    def create_one(
        self, name: str, price: float, available_quantity: int
    ) -> Product:
        product = Product(
            name=name,
            price=price,
            available_quantity=available_quantity,
        )
        self.repository.create_one(product)
        return product

    def update_one(
        self,
        product_id: UUID,
        name: str,
        price: float,
        available_quantity: int,
    ) -> bool:
        return self.repository.update_one(
            product_id, name, price, available_quantity
        )

    def delete_one(self, product_id: UUID) -> bool:
        return self.repository.delete_one(product_id)
