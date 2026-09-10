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
        line = OrderLine(RED_CHAIR_SKU, 99)
        batch = Batch(BATCH_REF, "RED_CHAIR", 1)
        batch.allocate(line)
        assert batch.available_quantity == 1

    def test_batch_can_not_allocate_orderline_twice(self):
        with pytest.raises(Exception) as excinfo:
            line = OrderLine(BLUE_VASE_SKU, 2)
            batch = Batch(BATCH_REF, "BLUE_VASE", 10)
            print(batch)
            batch.allocate(line)
            print(batch)
            batch.allocate(line)
        assert batch.available_quantity == 8

class TestBatchETA:
    def test_prefers_warehouse_batches_to_shipments(self):
        batch_eta = Batch(
            BATCH_REF,
            "RED_CHAIR",
            4,
            eta=datetime(2026, 8, 31, 15, 30, tzinfo=timezone.utc)
        )
        batch_warehouse = Batch(
            BATCH_REF,
            "RED_CHAIR",
            5
        )
        line = OrderLine(RED_CHAIR_SKU, 4)
        order = Order("refOrder", line)
        order.allocate(batch_eta, batch_warehouse)
        assert batch_eta.available_quantity == 4
        assert batch_warehouse.available_quantity == 1

    def test_prefers_earlier_batches(self):
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