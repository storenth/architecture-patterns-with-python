import pytest
from model import OrderLine, Order, Batch


ORDER_REF = "order-ref"
BATCH_REF = "batch-ref"
RED_CHAIR_SKU = "RED_CHAIR"
BLUE_VASE_SKU = "BLUE_VASE"


class TestOrder:

    def test_orderline_has_attributes(self):
        order_line = OrderLine()
        order_line.sku = RED_CHAIR_SKU
        order_line.quantity = 1
        print(order_line.sku)
        assert order_line.sku == RED_CHAIR_SKU
        assert order_line.quantity == 1


    def test_order_has_attributes(self):
        order = Order(ORDER_REF, RED_CHAIR=10, BLUE_SOFA=5)
        print(order)
        print(order.ref)
        print(order.order_lines)
        assert order.ref == ORDER_REF
        assert len(order.order_lines) == 2

class TestBatch:
    def generate_order_line(self, sku, quantity):
        order_line = OrderLine()
        order_line.sku = sku
        order_line.quantity = quantity
        return order_line

    def test_batch_has_orderline(self):
        batch = Batch(BATCH_REF, RED_CHAIR=50, BLUE_SOFA=10)
        print(batch)
        print(batch.ref)
        print(batch.order_lines)

        assert len(batch.order_lines) == 2

    def test_batch_can_allocate(self):
        order_line = self.generate_order_line(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(order_line) is True

    def test_batch_can_not_allocate(self):
        order_line = OrderLine()
        order_line.sku = RED_CHAIR_SKU
        order_line.quantity = 11
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(order_line) is False

    def test_batch_not_allocate_no_line(self):
        order_line = self.generate_order_line(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, BLUE_SOFA=10)
        assert batch.can_allocate(order_line) is False

    def test_batch_can_allocate(self):
        order_line = self.generate_order_line(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(order_line) is True

    def test_batch_allocate_orderline(self):
        order_line = self.generate_order_line(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        batch.allocate(order_line)
        assert batch.order_lines[order_line.sku] == 9

    def test_batch_can_not_allocate_orderline_twice(self):
        print("test_batch_can_not_allocate_orderline_twice")
        order_line = self.generate_order_line(BLUE_VASE_SKU, 2)
        batch = Batch(BATCH_REF, BLUE_VASE=10, BLUE_SOFA=10)
        print(batch)
        batch.allocate(order_line)
        print(batch)
        batch.allocate(order_line)
        print(batch)
        assert batch.order_lines[order_line.sku] == 8

