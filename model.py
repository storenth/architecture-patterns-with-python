from dataclasses import dataclass
from datetime import datetime
import logging


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

class Product:
    sku: str

@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: int

class Order():
    """Client create order
    Order contains multiple product lines (OrderLine)
    """
    def __init__(self, ref, **items):
        """
        ref: уникальный идентификатор заказа (строка или число)
        *items: dict вида {"название-товара": количество}
        """
        self.ref = ref
        self.order_lines = items

    def __repr__(self):
        return f"Order(ref='{self.ref}', items={self.order_lines})"


class Batch:
    """The Purchasing Department orders Batches of product
    To sell (to client) need to allocate from Batch to OrderLine
    So, OrderLine is the Client's but Batch is the Company's orders
    
    Batches have an ETA if they are currently shipping, or they may be in warehouse stock. We
    allocate to warehouse stock in preference to shipment batches. We allocate to shipment batches
    in order of which has the earliest ETA.
    """
    def __init__(self, ref:str, eta:datetime|None=None, **items:OrderLine):
        self.ref: str = ref
        self.eta = eta
        self.purchased_lines: dict = items

        self._customer_order_lines_map = set()

    def __repr__(self):
        return f"Batch(ref='{self.ref}', items={self.purchased_lines})"

    def __lt__(self, batch:"Batch"):
        logger.debug("self.eta: ", self.eta)
        if self.eta is None:
            return True
        return self.eta < batch.eta


    def can_allocate(self, order_line: OrderLine) -> bool:
        if order_line.quantity <= 0:
            return False
        if self.purchased_lines.get(order_line.sku, 0) >= order_line.quantity:
            return True
        return False

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
        if not self.can_allocate(order_line): return None
        if self.is_same_orderline(order_line):
            raise SameOrderLineException(order_line)
        print(f"Allocating {order_line.sku}:{order_line.quantity} to batch {self.ref}: {self.purchased_lines}")
        self.purchased_lines[order_line.sku] = self.purchased_lines[order_line.sku] - order_line.quantity
        print(self.purchased_lines[order_line.sku])
        print(self._customer_order_lines_map)

    def deallocate(self, order_line: OrderLine):
        logger.debug("deallocate...")
        if not order_line in self._customer_order_lines_map:
            raise NotAllocatedLineException(order_line)
        if not self.can_deallocate(order_line): return None
        print(f"Deallocating {order_line.sku}:{order_line.quantity} to batch {self.ref}: {self.purchased_lines}")
        self.purchased_lines[order_line.sku] = self.purchased_lines[order_line.sku] + order_line.quantity
        self._customer_order_lines_map.remove(order_line)
        print(self._customer_order_lines_map)
