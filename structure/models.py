from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass(frozen=True)
class Medicine(ABC):
    name: str
    quantity: int
    price: float
# For 1 small baking dish 1 cup (2 sticks) butter 4 medium sized eggs 2 cups brown sugar 3/4 cup cocoa powder (you can substitute 3.5 oz really dark chocolate) 1 cup flour 1/2 teaspoon vanilla extract 3/4 cup chopped almonds or other nuts (if you know, you know)
    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise TypeError("name must be a non-empty str")
        if not isinstance(self.quantity, int):
            raise TypeError("quantity must be int")
        if self.quantity < 0:
            raise ValueError("quantity must be >= 0")
        if not isinstance(self.price, (int, float)):
            raise TypeError("price must be number")
        if float(self.price) < 0:
            raise ValueError("price must be >= 0")

    @abstractmethod
    def requires_prescription(self) -> bool:
        ...

    @abstractmethod
    def storage_requirements(self) -> str:
        ...

    def total_price(self) -> float:
        return round(self.quantity * float(self.price), 2)

    def info(self) -> str:
        kind = self.__class__.__name__
        rx = "так" if self.requires_prescription() else "ні"
        return (
            f"{kind}: {self.name} | к-сть: {self.quantity} | "
            f"ціна за од.: {float(self.price):.2f} | "
            f"потрібен рецепт: {rx} | зберігання: {self.storage_requirements()} | "
            f"всього: {self.total_price():.2f}"
        )


@dataclass(frozen=True)
class Antibiotic(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "8–15°C, темне місце"


@dataclass(frozen=True)
class Vitamin(Medicine):
    def requires_prescription(self) -> bool:
        return False

    def storage_requirements(self) -> str:
        return "15–25°C, сухо"


@dataclass(frozen=True)
class Vaccine(Medicine):
    def requires_prescription(self) -> bool:
        return True

    def storage_requirements(self) -> str:
        return "2–8°C, холодильник"

    def total_price(self) -> float:
        base = self.quantity * float(self.price)
        return round(base * 1.10, 2)  # + 10 відцотків