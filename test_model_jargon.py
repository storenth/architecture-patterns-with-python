import pytest
from model import OrderLine, Order, Batch
from datetime import datetime, timezone
import logging


log = logging.getLogger(__name__)
formatter = logging.Formatter(
    "%(asctime)s.%(msecs)03d %(levelname)s "
    "%(filename)s:%(lineno)s: %(message)s",
    "%Y-%m-%d %H:%M:%S",
)
# Console output default: sys.stderr
handler = logging.StreamHandler()
handler.setFormatter(formatter)
log.addHandler(handler)

ORDER_REF = "order-ref"
BATCH_REF = "batch-ref"
RED_CHAIR_SKU = "RED_CHAIR"
BLUE_VASE_SKU = "BLUE_VASE"


class TestOrder:
    def test_orderline_has_attributes(self):
        order_line = OrderLine(RED_CHAIR_SKU, 1)
        log.debug(order_line.sku)
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
    def test_batch_has_orderline(self):
        batch = Batch(BATCH_REF, RED_CHAIR=50, BLUE_SOFA=10)
        print(batch)
        print(batch.ref)
        print(batch.purchased_lines)
        assert len(batch.purchased_lines) == 2

    def test_batch_can_allocate(self):
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(line) is True

    def test_batch_can_not_allocate(self):
        order_line = OrderLine(RED_CHAIR_SKU, 11)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(order_line) is False

    def test_batch_not_allocate_no_line(self):
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, BLUE_SOFA=10)
        assert batch.can_allocate(line) is False

    def test_batch_can_allocate(self):
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        assert batch.can_allocate(line) is True

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch.allocate(line)
        assert batch.purchased_lines[line.sku] == 9

    def test_can_only_deallocate_allocated_lines(self):
        batch = Batch(BATCH_REF, RED_CHAIR=20, BLUE_SOFA=5)
        unallocated_line = OrderLine(RED_CHAIR_SKU, 2)
        with pytest.raises(Exception) as excinfo:
            batch.deallocate(unallocated_line)
        print("excinfo: ", excinfo)
        assert batch.purchased_lines["RED_CHAIR"] == 20

    def test_can_deallocate_allocated_lines(self):
        batch = Batch(BATCH_REF, RED_CHAIR=20, BLUE_SOFA=5)
        line = OrderLine(RED_CHAIR_SKU, 2)
        batch.allocate(line)
        assert batch.purchased_lines["RED_CHAIR"] == 18
        batch.deallocate(line)
        assert batch.purchased_lines["RED_CHAIR"] == 20

    def test_cannot_allocate_if_available_smaller_than_required(self):
        line = OrderLine(RED_CHAIR_SKU, 99)
        batch = Batch(BATCH_REF, RED_CHAIR=1, BLUE_SOFA=10)
        batch.allocate(line)
        assert batch.purchased_lines[line.sku] == 1

    def test_batch_can_not_allocate_orderline_twice(self):
        with pytest.raises(Exception) as excinfo:
            line = OrderLine(BLUE_VASE_SKU, 2)
            batch = Batch(BATCH_REF, BLUE_VASE=10, BLUE_SOFA=10)
            print(batch)
            batch.allocate(line)
            print(batch)
            batch.allocate(line)
        assert batch.purchased_lines[line.sku] == 8
