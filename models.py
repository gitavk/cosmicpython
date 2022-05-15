from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class OrderLine:
    title: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.ref: str = ref
        self.sku: str = sku
        self.available_quantity: int = qty
        self.qty: int = qty
        self.eta: Optional[date] = eta

    def allocate(self, line: OrderLine) -> None:
        if self.can_allocate(line):
            self.available_quantity -= line.qty

    def can_allocate(self, line: OrderLine) -> bool:
        is_right_sku: bool = self.sku == line.sku
        enough_qty: bool = self.available_quantity >= line.qty
        return is_right_sku and enough_qty

    def deallocate(self, line: OrderLine) -> None:
        if self.available_quantity + line.qty <= self.qty:
            self.available_quantity += line.qty
        
