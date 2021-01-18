from pathlib import Path

import pytest

from resource_planners import Design, BouquetResourcePlanner


@pytest.fixture
def new_planner():
    """
    Returns a Bouquet Resource Planner with an empty flower inventory.
    """
    return BouquetResourcePlanner()


@pytest.fixture
def planner():
    """
    Returns a Bouquet Resource Planner with:
        - 1 small flowers of species A
        - 2 large flowers of species A
        - 5 small flowers of species B
        - 2 Designs
    """
    planner = BouquetResourcePlanner()
    planner.add_flowers(species="a", size="S", amount=1)
    planner.add_flowers(species="a", size="L", amount=2)
    planner.add_flowers(species="b", size="S", amount=5)
    planner.add_design(name="Y", size="L", total_quantity=2, flowers={"a": 2})
    planner.add_design(name="Z", size="S", total_quantity=3, flowers={"a": 2, "b": 2})
    return planner


def test_default_new_planner_inventory(new_planner):
    assert new_planner._flowers == {}


def test_default_planner_inventory(planner):
    expected_result = {
        "a": {"S": 1, "L": 2},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


def test_getting_flower_amount(planner):
    assert planner.get_flower_amount("a", "S") == 1
    assert planner.get_flower_amount("a", "L") == 2
    assert planner.get_flower_amount("b", "S") == 5


def test_adding_new_flower_species(new_planner):
    new_planner.add_flowers(species="a", size="L", amount=2)
    new_planner.add_flowers(species="b", size="S", amount=5)

    expected_result = {
        "a": {"L": 2},
        "b": {"S": 5},
    }
    assert new_planner._flowers == expected_result


def test_adding_new_flower_size_to_existing_species(planner):
    planner.add_flowers(species="b", size="L", amount=1)
    expected_result = {
        "a": {"S": 1, "L": 2},
        "b": {"S": 5, "L": 1},
    }
    assert planner._flowers == expected_result


def test_adding_flowers_to_existing_size(planner):
    planner.add_flowers(species="a", size="L", amount=2)
    expected_result = {
        "a": {"S": 1, "L": 4},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


def test_removing_flowers(planner):
    planner.remove_flowers(species="a", size="S", amount=1)
    expected_result = {
        "a": {"S": 0, "L": 2},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


def test_removing_flowers_with_too_high_amount(planner):
    planner.remove_flowers(species="a", size="S", amount=10)
    expected_result = {
        "a": {"S": 0, "L": 2},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


def test_removing_flowers_with_non_existent_size(planner):
    planner.remove_flowers(species="a", size="M", amount=10)
    expected_result = {
        "a": {"S": 1, "L": 2},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


def test_removing_flowers_with_non_existent_species(planner):
    planner.remove_flowers(species="c", size="S", amount=1)
    expected_result = {
        "a": {"S": 1, "L": 2},
        "b": {"S": 5},
    }
    assert planner._flowers == expected_result


@pytest.mark.parametrize(
    "flower_data,expected_result",
    [
        ("10a15b5c", {"a": 10, "b": 15, "c": 5}),
        ("2a2b", {"a": 2, "b": 2}),
        ("2a", {"a": 2}),
    ],
)
def test_converting_flower_data_to_dict(flower_data, expected_result):
    flowers = BouquetResourcePlanner._convert_flower_data_to_dict(flower_data)
    assert flowers == expected_result


def test_adding_a_design(new_planner):
    new_planner.add_design(
        name="A", size="L", total_quantity=3, flowers={"a": 2, "b": 3}
    )
    expected_result = [
        Design(name="A", size="L", total_quantity=3, flowers={"a": 2, "b": 3})
    ]
    assert new_planner._designs == expected_result


def test_importing_from_file(new_planner):
    path = Path(__file__).parent / "test_data" / "example01.txt"
    new_planner.import_from_file(path=path)
    expected_designs = [
        Design(name="A", size="S", total_quantity=3, flowers={"a": 2, "b": 2}),
        Design(name="B", size="L", total_quantity=2, flowers={"a": 2}),
    ]
    expected_flowers = {"a": {"S": 3, "L": 2}, "b": {"S": 3}}
    assert new_planner._designs == expected_designs
    assert new_planner._flowers == expected_flowers


def test_importing_from_file_with_existing_data(planner):
    path = Path(__file__).parent / "test_data" / "example01.txt"
    planner.import_from_file(path=path)
    expected_designs = [
        Design(name="Y", size="L", total_quantity=2, flowers={"a": 2}),
        Design(name="Z", size="S", total_quantity=3, flowers={"a": 2, "b": 2}),
        Design(name="A", size="S", total_quantity=3, flowers={"a": 2, "b": 2}),
        Design(name="B", size="L", total_quantity=2, flowers={"a": 2}),
    ]
    expected_flowers = {"a": {"S": 4, "L": 4}, "b": {"S": 8}}
    assert planner._designs == expected_designs
    assert planner._flowers == expected_flowers


@pytest.mark.parametrize(
    "flowers,amounts_left,expected",
    [
        ({"a": 6, "b": 4, "c": 6}, {"a": 2, "b": 3, "c": 2}, "AL4a"),
        ({"a": 1, "b": 4, "c": 6}, {"a": 5, "b": 0, "c": 2}, "AL1a3b"),
        ({"a": 1, "b": 2, "c": 6}, {"a": 5, "b": 1, "c": 1}, "AL1a2b1c"),
        ({"d": 1, "e": 1}, {"a": 6, "b": 3, "c": 2}, None),
    ],
)
def test_creating_bouquet_code(new_planner, flowers, amounts_left, expected):
    design = Design(name="A", size="L", total_quantity=4, flowers=flowers)
    new_planner.add_flowers(species="a", size="L", amount=6)
    new_planner.add_flowers(species="b", size="L", amount=3)
    new_planner.add_flowers(species="c", size="L", amount=2)
    bouquet_code = new_planner.create_bouquet_code(design)
    assert bouquet_code == expected
    assert new_planner.get_flower_amount("a", "L") == amounts_left["a"]
    assert new_planner.get_flower_amount("b", "L") == amounts_left["b"]
    assert new_planner.get_flower_amount("c", "L") == amounts_left["c"]


def test_building_bouquet_list(planner):
    codes = planner.build_bouquet_list()
    assert codes == ["YL2a", "ZS1a2b"]


def test_building_bouquet_list_with_no_flowers(new_planner):
    new_planner.add_design(
        name="A", size="L", total_quantity=4, flowers={"d": 1, "e": 1}
    )
    codes = new_planner.build_bouquet_list()
    assert codes == []
