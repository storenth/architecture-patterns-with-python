import pytest
from model import OrderLine, Order, Batch, OutOfStock, SameOrderLineException
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


class TestOrderLine:
    def test_orderline_has_attributes(self):
        order_line = OrderLine(RED_CHAIR_SKU, 1)
        log.debug(order_line.sku)
        assert order_line.sku == RED_CHAIR_SKU
        assert order_line.quantity == 1

    def test_order_has_attributes(self):
        order_line = OrderLine(RED_CHAIR_SKU, 1)
        order = Order(ORDER_REF, order_line)
        print(order)
        print(order.ref)
        print(order.order_line)
        assert order.ref == ORDER_REF
        assert order.order_line.quantity == 1

class TestBatch:
    def test_batch_has_orderline(self):
        batch = Batch(BATCH_REF, "RED_CHAIR", 2)
        print(batch)
        print(batch.ref)
        assert batch.quantity == 2

    def test_batch_can_allocate(self):
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, "RED_CHAIR", 10)
        assert batch.can_allocate(line) is True

    def test_batch_can_not_allocate(self):
        order_line = OrderLine(RED_CHAIR_SKU, 11)
        batch = Batch(BATCH_REF, "RED_CHAIR", 10)
        # batch = Batch(BATCH_REF, RED_CHAIR=10, BLUE_SOFA=10)  # old approach
        assert batch.can_allocate(order_line) is False

    def test_batch_not_allocate_no_line(self):
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch = Batch(BATCH_REF, "BLUE_SOFA", 10)
        assert batch.can_allocate(line) is False

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        batch = Batch(BATCH_REF, "RED_CHAIR", 10)
        line = OrderLine(RED_CHAIR_SKU, 1)
        batch.allocate(line)
        assert batch.available_quantity == 9

    def test_can_only_deallocate_allocated_lines(self):
        batch = Batch(BATCH_REF, "RED_CHAIR", 20)
        unallocated_line = OrderLine(RED_CHAIR_SKU, 2)
        with pytest.raises(Exception) as excinfo:
            batch.deallocate(unallocated_line)
        print("excinfo: ", excinfo)
        assert batch.available_quantity == 20

    def test_can_deallocate_allocated_lines(self):
        batch = Batch(BATCH_REF, "RED_CHAIR", 20)
        line = OrderLine(RED_CHAIR_SKU, 2)
        batch.allocate(line)
        assert batch.available_quantity == 18
        batch.deallocate(line)
        assert batch.available_quantity == 20

    def test_cannot_allocate_if_available_smaller_than_required(self):
        batch = Batch(BATCH_REF, "RED_CHAIR", 1)
        line = OrderLine(RED_CHAIR_SKU, 99)
        assert batch.can_allocate(line) is False
        batch.allocate(line)
        assert batch.available_quantity == 1

    def test_batch_can_not_allocate_orderline_twice(self):
        batch = Batch(BATCH_REF, "BLUE_VASE", 10)
        line = OrderLine(BLUE_VASE_SKU, 2)
        batch.allocate(line)
        with pytest.raises(SameOrderLineException):
            batch.allocate(line)
            print(f"{batch=}")
        assert batch.available_quantity == 8


class TestOutOfStock:
    def test_outofstock(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch = Batch(BATCH_REF, "BLUE_VASE", 1)
        with pytest.raises(OutOfStock):
            order.allocate(batch)
        assert batch.available_quantity == 1

    def test_outofstock_same_batch_order(self):
        order_first = Order("refOrder1", OrderLine(BLUE_VASE_SKU, 7))
        order_second = Order("refOrder2", OrderLine(BLUE_VASE_SKU, 10))
        batch = Batch(BATCH_REF, "BLUE_VASE", 10)
        order_first.allocate(batch)
        with pytest.raises(OutOfStock):
            order_second.allocate(batch)
        assert batch.available_quantity == 3

    def test_outofstock_two_batches(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 1)
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 5)
        with pytest.raises(OutOfStock):
            order.allocate(batch_1, batch_2)
        assert batch_1.available_quantity == 1
        assert batch_2.available_quantity == 5


class TestSortOrder:
    def test_available_stock_in_first_batch(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 1))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 50)
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 7)
        order.allocate(batch_1, batch_2)
        assert batch_1.available_quantity == 49
        assert batch_2.available_quantity == 7

    def test_available_stock_in_second_batch(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 1)
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 70)
        batch_3 = Batch(BATCH_REF, "BLUE_VASE", 100)
        order.allocate(batch_1, batch_2, batch_3)
        assert batch_2.available_quantity == 60
        assert batch_1.available_quantity == 1
        assert batch_3.available_quantity == 100

    def test_prefered_eta_in_first_batch(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 50, eta=datetime(2026, 8, 31, 15, 30, tzinfo=timezone.utc))
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 7)
        order.allocate(batch_1, batch_2)
        assert batch_1.available_quantity == 40
        assert batch_2.available_quantity == 7

    def test_prefered_eta_in_second_batch(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 40, eta=datetime(2026, 8, 31, 15, 30, tzinfo=timezone.utc))
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 40)
        batch_3 = Batch(BATCH_REF, "BLUE_VASE", 100)
        order.allocate(batch_1, batch_2, batch_3)
        assert batch_1.available_quantity == 40
        assert batch_2.available_quantity == 30
        assert batch_3.available_quantity == 100

    def test_prefered_eta_third_batch(self):
        order = Order("refOrder", OrderLine(BLUE_VASE_SKU, 10))
        batch_1 = Batch(BATCH_REF, "BLUE_VASE", 40, eta=datetime(2026, 9, 29, 15, 30, tzinfo=timezone.utc))
        batch_2 = Batch(BATCH_REF, "BLUE_VASE", 4)
        batch_3 = Batch(BATCH_REF, "BLUE_VASE", 100, eta=datetime(2026, 9, 29, 15, 00, tzinfo=timezone.utc))
        order.allocate(batch_3, batch_1, batch_2)
        assert batch_1.available_quantity == 40
        assert batch_2.available_quantity == 4
        assert batch_3.available_quantity == 90

class TestBatchETA:
    def test_prefers_warehouse_batches_to_shipments(self):
        batch_eta = Batch(
            BATCH_REF,
            "RED_CHAIR",
            3,
            eta=datetime(2026, 8, 31, 15, 30, tzinfo=timezone.utc)
        )
        batch_warehouse = Batch(
            BATCH_REF,
            "RED_CHAIR",
            3
        )
        line = OrderLine(RED_CHAIR_SKU, 2)
        order = Order("refOrder", line)
        order.allocate(batch_eta, batch_warehouse)
        assert batch_eta.available_quantity == 3
        assert batch_warehouse.available_quantity == 1

    def test_prefers_earllest_batches(self):
        batch_eta = Batch(
            BATCH_REF,
            "RED_CHAIR",
            5,
            eta=datetime(2026, 10, 29, 15, 30, tzinfo=timezone.utc)
        )
        batch_eta_earler = Batch(
            BATCH_REF,
            "RED_CHAIR",
            2,
            eta=datetime(2026, 10, 20, 11, 00, tzinfo=timezone.utc)
        )
        batch_eta_earllest = Batch(
            BATCH_REF,
            "RED_CHAIR",
            2,
            eta=datetime(2026, 9, 11, 13, 45, tzinfo=timezone.utc)
        )
        line = OrderLine(RED_CHAIR_SKU, 1)
        order = Order("refOrder", line)
        
        order.allocate(batch_eta, batch_eta_earllest, batch_eta_earler)
        assert batch_eta.available_quantity == 5
        assert batch_eta_earler.available_quantity == 2
        assert batch_eta_earllest.available_quantity == 1