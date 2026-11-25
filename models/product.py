from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Product:
    name: str
    price: float
    available_quantity: int
    id: UUID = field(default_factory=uuid4)
