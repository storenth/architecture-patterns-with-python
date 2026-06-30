from dataclasses import dataclass

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
    """
    def __init__(self, ref, **items):
        self.ref: str = ref
        self.order_lines = items

    def __repr__(self):
        return f"Batch(ref='{self.ref}', items={self.order_lines})"

    def can_allocate(self, order_line: OrderLine) -> bool:
        if order_line.quantity <= 0:
            return False
        if self.order_lines.get(order_line.sku, 0) >= order_line.quantity:
            return True
        return False

    def allocate(self, order_line: OrderLine):
        if not self.can_allocate(order_line): return None
        print(f"Allocating {order_line.sku}:{order_line.quantity} to batch {self.ref}: {self.order_lines}")
        self.order_lines[order_line.sku] = self.order_lines[order_line.sku] - order_line.quantity
        print(self.order_lines[order_line.sku])
