import pytest

from service_body_test import Order


def test_total_with_multiple_items():
    """total() для звичайного набору товарів"""
    items = [
        {"name": "A", "price": 10.0, "quantity": 2},
        {"name": "B", "price": 5.5, "quantity": 3},
    ]
    order = Order(id=1, items=items)
    assert order.total() == pytest.approx(10.0 * 2 + 5.5 * 3)


def test_total_with_empty_items():
    """total() для порожнього списку — має бути 0"""
    order = Order(id=2, items=[])
    assert order.total() == 0


def test_total_with_zero_price_and_quantity():
    """total() коли або price=0, або quantity=0"""
    items = [
        {"name": "Free", "price": 0.0, "quantity": 10},
        {"name": "None", "price": 99.0, "quantity": 0},
    ]
    order = Order(id=3, items=items)
    assert order.total() == 0


def test_most_expensive_basic():
    """most_expensive() повертає товар з найбільшою ціною"""
    items = [
        {"name": "Cheap", "price": 1.0, "quantity": 10},
        {"name": "Mid", "price": 5.0, "quantity": 1},
        {"name": "Expensive", "price": 9.99, "quantity": 1},
    ]
    order = Order(id=4, items=items)
    most = order.most_expensive()
    assert most["name"] == "Expensive"
    assert most["price"] == 9.99


def test_most_expensive_raises_on_empty_items():
    """most_expensive() на порожньому списку має кинути ValueError"""
    order = Order(id=5, items=[])
    with pytest.raises(ValueError):
        order.most_expensive()


def test_apply_discount_valid_percent_changes_all_items():
    """apply_discount() змінює ціну КОЖНОГО товару на відсоток"""
    items = [
        {"name": "A", "price": 100.0, "quantity": 1},
        {"name": "B", "price": 50.0, "quantity": 2},
    ]
    order = Order(id=6, items=items)
    original_prices = [item["price"] for item in items]

    order.apply_discount(10)  # -10%

    for idx, item in enumerate(order.items):
        expected_price = original_prices[idx] * 0.9
        assert item["price"] == pytest.approx(expected_price)


def test_apply_discount_zero_percent_keeps_prices():
    """apply_discount(0) не змінює ціни"""
    items = [
        {"name": "A", "price": 100.0, "quantity": 1},
        {"name": "B", "price": 50.0, "quantity": 2},
    ]
    order = Order(id=7, items=items)
    original_prices = [item["price"] for item in items]

    order.apply_discount(0)

    assert [item["price"] for item in order.items] == original_prices


def test_apply_discount_hundred_percent_sets_prices_to_zero():
    """apply_discount(100) обнуляє ціни"""
    items = [
        {"name": "A", "price": 100.0, "quantity": 1},
        {"name": "B", "price": 50.0, "quantity": 2},
    ]
    order = Order(id=8, items=items)

    order.apply_discount(100)

    for item in order.items:
        assert item["price"] == pytest.approx(0.0)


def test_apply_discount_fractional_percent():
    """apply_discount() з дробовим відсотком (наприклад 12.5%)"""
    items = [{"name": "A", "price": 80.0, "quantity": 1}]
    order = Order(id=9, items=items)

    order.apply_discount(12.5)

    assert order.items[0]["price"] == pytest.approx(80.0 * (1 - 0.125))


def test_apply_discount_on_empty_items_does_not_fail():
    """apply_discount() на порожньому списку не повинен падати"""
    order = Order(id=10, items=[])
    order.apply_discount(50)
    assert order.items == []


@pytest.mark.parametrize("percent", [-1, -0.01, 100.01, 150])
def test_apply_discount_invalid_percent_raises(percent):
    """apply_discount() з некоректними відсотками кидає ValueError"""
    items = [{"name": "A", "price": 100.0, "quantity": 1}]
    order = Order(id=11, items=items)

    with pytest.raises(ValueError):
        order.apply_discount(percent)


def test_repr_format():
    """__repr__ містить id та кількість items"""
    items = [
        {"name": "A", "price": 10.0, "quantity": 1},
        {"name": "B", "price": 20.0, "quantity": 2},
    ]
    order = Order(id="ORD-123", items=items)
    assert repr(order) == "<Order ORD-123: 2 items>"


def test_repr_with_zero_items():
    """__repr__ для пустого замовлення"""
    order = Order(id="EMPTY", items=[])
    assert repr(order) == "<Order EMPTY: 0 items>"
