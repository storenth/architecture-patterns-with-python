from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# custom exceptions
class SameOrderLineException(Exception):
   def __init__(self, order_line: "OrderLine"):
       self.order_line = order_line
   def __str__(self):
        return 'We can not allocate the same line twice: {}'.format(self.order_line.sku)
class NotAllocatedLineException(Exception):
   def __init__(self, order_line: "OrderLine"):
       self.order_line = order_line
   def __str__(self):
        return 'We can not deallocate not allocated line: {}'.format(self.order_line.sku)

class OutOfStock(Exception):
    pass


class Product:
    sku: str

@dataclass(frozen=True)
# the hash based on all the value attributes
class OrderLine:
    sku: str
    quantity: int

class Order:
    """Client create order
    Order contains multiple product lines (OrderLine)
    """
    def __init__(self, ref, line:OrderLine):
        """
        ref: уникальный идентификатор заказа (строка или число)
        *items: dict вида {"название-товара": количество}
        """
        self.ref = ref
        self.order_line = line
        print(f"{self.order_line=}")

    def __repr__(self):
        return f"Order(ref='{self.ref}', items={self.order_line})"

    def allocate(self, *batches: "Batch"):
        """Сначала сортируематем, далее 
        для каждого батча проверяем есть ли нужный quantity, и
        выделяем из партии под конкретный заказ
        """
        logger.debug(f"{batches=}")
        logger.debug(f"{sorted(batches)=}")

        try:
            preferred_batch = next(b for b in sorted(batches) if b.can_allocate(self.order_line))
            preferred_batch.allocate(self.order_line)
            return preferred_batch.ref
        except StopIteration:
            raise OutOfStock(f"OutOfStock: can't allocate {self.order_line=} because no Product found in batches {batches=}")


class Batch:
    """The Purchasing Department orders Batches of product
    To sell (to client) need to allocate from Batch to OrderLine
    So, OrderLine is the Client's but Batch is the Company's orders
    
    Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We
    allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches
    in order of which has the earliest ETA.

    lines: соберет готовые объекты OrderLine
    items: соберет именованные параметры типа RED_CHAIR=10
    """
    def __init__(self, ref:str, sku:str, quantity:int, eta:datetime|None=None):
        self.ref: str = ref
        self.eta = eta
        logger.debug(f"Batch {quantity=}")

        self.sku = sku
        self.quantity = quantity        

        self._customer_order_lines_map:set[OrderLine] = set()

    def __repr__(self):
        return f"Batch(ref='{self.ref}', items={self.sku},{self.quantity}, ets={self.eta})"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.ref == other.ref

    def __hash__(self):
        return hash(self.ref)

    def __lt__(self, batch:"Batch"):
        logger.debug(f"{self.eta=}")
        if self.eta is None and batch.eta is None:
            return False
        if self.eta is None:
            return True
        if batch.eta is None:
            return False
        return self.eta < batch.eta
    
    @property
    def allocated_quantity(self) -> int:
        return sum(line.quantity for line in self._customer_order_lines_map)

    @property
    def available_quantity(self) -> int:
        _available_quantity = self.quantity  - self.allocated_quantity
        logger.debug(f"{_available_quantity=}")
        return _available_quantity

    def can_allocate(self, order_line: OrderLine) -> bool:
        logger.debug(f"{order_line.quantity=}")
        logger.debug(f"{self.available_quantity=}")
        if order_line.quantity <= 0:
            return False
        return self.sku == order_line.sku and self.available_quantity >= order_line.quantity

    def can_deallocate(self, order_line: OrderLine) -> bool:
        if order_line.quantity <= 0: return False
        else: return True

    def is_same_orderline(self, order_line: OrderLine) -> bool:
        if order_line in self._customer_order_lines_map:
            return True
        self._customer_order_lines_map.add(order_line)
        print("self._customer_order_lines_map: ", self._customer_order_lines_map)
        return False

    def allocate(self, order_line: OrderLine):
        logger.debug("allocate...")
        if self.can_allocate(order_line):
            if self.is_same_orderline(order_line):
                raise SameOrderLineException(order_line)

        print(f"Allocating {order_line.sku}:{order_line.quantity} to batch {self.ref}: {self.quantity}")
        print(self._customer_order_lines_map)

    def deallocate(self, order_line: OrderLine):
        logger.debug("deallocate...")
        if not order_line in self._customer_order_lines_map:
            raise NotAllocatedLineException(order_line)
        if not self.can_deallocate(order_line): return None
        print(f"Deallocating {order_line.sku}:{order_line.quantity} to batch {self.ref}: {self.quantity}")
        self._customer_order_lines_map.remove(order_line)
        print(self._customer_order_lines_map)
