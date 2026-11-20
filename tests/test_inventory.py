import pytest

from src.inventory import (
    Inventory,
    Item,
    OutOfStockError,
    UnknownItemError,
)
@pytest.fixture
def empty_inventory() -> Inventory:
    return Inventory()


@pytest.fixture
def inventory():
    inv = Inventory()
    inv.add(Item("apple", 10.0), quantity=10)
    return inv


def test_create_valid_item_defaults():
        item = Item("bread", 45.0)
        assert item.name == "bread"
        assert item.price == 45.0
        assert item.quantity == 0  

def test_create_item_zero_price():
        item = Item("pelmen", 0.0, quantity=1)
        assert item.price == 0.0
        assert item.quantity == 1

@pytest.mark.parametrize(
        "name, price, quantity, error_msg",
        [
            ("", 10.0, 1, "name must not be empty"),
            ("item1", -0.01, 1, "price must be non-negative"),
            ("item2", 10.0, -1, "quantity must be non-negative"),
        ],
    )
def test_create_invalid_item( name, price, quantity, error_msg):
        with pytest.raises(ValueError, match=error_msg):
            Item(name, price, quantity)




def test_remove_unknown_item_raises(inventory):
    with pytest.raises(UnknownItemError):
        inventory.remove("banana")

def test_remove_Out_Of_Stock_raises(inventory):
    with pytest.raises(OutOfStockError):
        inventory.remove("apple",11)

def test_deleting_position_when_zero(inventory):
    inventory.remove("apple",10)
    with pytest.raises(UnknownItemError):
            inventory.find("apple")

def test_remove_partial_quantity(inventory):
    result = inventory.remove("apple", quantity=4)

    assert result is None
    assert inventory.find("apple").quantity == 6
    
@pytest.mark.parametrize("bad_quantity", [0, -5])
def test_remove_invalid_quantity(inventory, bad_quantity):
    with pytest.raises(ValueError, match="quantity must be positive"):
        inventory.remove("apple", quantity=bad_quantity)





@pytest.mark.parametrize("bad_quantity", [0, -1, -10])

def test_zero_quantity_raises(empty_inventory, bad_quantity):
    with pytest.raises(ValueError, match="quantity must be positive"):
        empty_inventory.add(Item("lemon", 12.0), quantity=bad_quantity)


def test_adding_one(empty_inventory):
    result = empty_inventory.add(Item("peach", 8.0), quantity=1) 

    assert result is None

    found = empty_inventory.find("peach")

    assert found.name == "peach"
    assert found.price == 8.0
    assert found.quantity == 1


def test_add_existing_item_increases_quantity(empty_inventory):
        
    empty_inventory.add(Item("milk", 90.0), quantity=2)
    empty_inventory.add(Item("milk", 90.0), quantity=3)

    assert empty_inventory.find("milk").quantity == 5

def test_total_value_empty( empty_inventory):
        assert empty_inventory.total_value() == 0


def test_total_value_multiple_items(inventory):
    inventory.add(Item("pelmen", 10.0), quantity=10)

    assert inventory.total_value() == 200

def test_total_value_rounding(empty_inventory):
    empty_inventory.add(Item("nail", 0.333), quantity=1)
    empty_inventory.add(Item("screw", 0.333), quantity=1)
    assert empty_inventory.total_value() == 0.67


def test_low_stock_default_threshold_and_sorting(inventory):
    inventory.add(Item("banana", 80.5), quantity=5)
    inventory.add(Item("orange", 120.0), quantity=2)
    assert inventory.low_stock() == ["banana", "orange"]

@pytest.mark.parametrize(
    "threshold, expected",
    [
        (0, []),  
        (1, []),  
        (2, ["orange"]),
        (10, ["apple", "banana", "orange"]),  
    ],
)
def test_low_stock_custom_threshold( inventory, threshold, expected ):
    inventory.add(Item("banana", 80.5), quantity=5)
    inventory.add(Item("orange", 120.0), quantity=2)
    assert inventory.low_stock(threshold=threshold) == expected

def test_low_stock_negative_threshold(empty_inventory):
    with pytest.raises(ValueError, match="threshold must be non-negative"):
        empty_inventory.low_stock(threshold=-1)

@pytest.mark.parametrize(
    "percent, expected",
    [
        (0, 100.0),
        (10, 90.0),
        (100, 0.0),
    ],
)
def test_apply_discount_valid_percent(inventory, percent, expected):
    assert inventory.apply_discount(percent) == pytest.approx(expected)


@pytest.mark.parametrize("bad_percent", [-0.1, -10, 100.1, 150])
def test_apply_discount_invalid(inventory, bad_percent):
    with pytest.raises(ValueError, match="percent must be in 0..100"):
        inventory.apply_discount(bad_percent)