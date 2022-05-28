from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


@dataclass(frozen=True)
class OrderLine:
    title: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]) -> None:
        self.reference: str = ref
        self.sku: str = sku
        self.eta: Optional[date] = eta
        self._allocations: Set[OrderLine] = set()
        self._purchased_quantity: int = qty


    def __repr__(self):
        return f"<Batch {self.reference}>"

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        is_right_sku: bool = self.sku == line.sku
        enough_qty: bool = self.available_quantity >= line.qty
        return is_right_sku and enough_qty

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    batch: Batch = next(b for b in sorted(batches) if b.can_allocate(line))
    batch.allocate(line)
    return batch.reference
