import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Union, List


@dataclass
class Design:
    name: str
    size: str
    total_quantity: int
    flowers: Dict[str, int]


class BouquetResourcePlanner:
    _pattern_flowers = re.compile(r'^[a-z][A-Z]$')
    _pattern_designs = re.compile(r'^([A-Z])([A-Z])((?:\d+[a-z])+)(\d+)$')

    _flowers: Dict[str, Dict[str, int]]
    _designs: List[Design]

    def __init__(self):
        self._flowers = {}
        self._designs = []

    def get_flower_amount(self, species: str, size: str) -> int:
        """
        Get the current amount of flowers in the inventory.

        :param species: The name of the flower species.
        :param size: The size of the flower.
        :return int: The amount of flowers.
        """
        try:
            return self._flowers[species][size]
        except KeyError:
            return 0

    def add_flowers(self, species: str, size: str, amount: int) -> None:
        """
        Add flower(s) to the inventory of the resource planner.

        :param species: The name of the flower species.
        :param size: The size of the flower.
        :param amount: The amount of flowers to add to the inventory.
        """
        if species not in self._flowers:
            self._flowers[species] = {}

        if size not in self._flowers[species]:
            self._flowers[species][size] = 0

        self._flowers[species][size] += amount

    def remove_flowers(self, species: str, size: str, amount: int) -> None:
        """
        Remove flower(s) from the inventory of the resource planner.

        :param species: The name of the flower species.
        :param size: The size of the flower.
        :param amount: The amount of flowers to remove from the inventory.
        """
        try:
            self._flowers[species][size] -= amount
            if self._flowers[species][size] < 0:
                self._flowers[species][size] = 0
        except KeyError:
            pass

    def add_design(self, name: str, size: str, total_quantity: int,
                   flowers: Dict[str, int]) -> None:
        """
        Add design to the resource planner.

        :param name: The name of the design.
        :param size: The required size of the flowers.
        :param total_quantity: The amount of flowers in total.
        :param flowers: The required type of flowers (species and size).
        """
        design = Design(
            name=name,
            size=size,
            total_quantity=total_quantity,
            flowers=flowers
        )
        self._designs.append(design)

    def import_from_file(self, path: Path) -> None:
        """
        Import flowers and designs from a text file.

        :param path: The path of the text file.
        """
        with open(path) as f:
            for line in list(f.read().splitlines()):
                if self._pattern_flowers.fullmatch(line):
                    self.add_flowers(species=line[0], size=line[1], amount=1)

                elif self._pattern_designs.fullmatch(line):
                    groups = self._pattern_designs.fullmatch(line).groups()
                    flowers = self._convert_flower_data_to_dict(groups[2])
                    self.add_design(
                        name=groups[0],
                        size=groups[1],
                        flowers=flowers,
                        total_quantity=int(groups[3])
                    )

    def create_bouquet_code(self, design: Design) -> Union[str, None]:
        """
        Create a bouquet from a design and the available flowers.

        :param design: The design data required to create a bouquet.
        :return str: The bouquet code when a bouquet can be created with the
            available flowers.
        """
        unused_space = design.total_quantity
        required_flowers = []
        bouquet_code = ''

        for species, max_quantity in design.flowers.items():
            amount = 0
            inventory_amount = self.get_flower_amount(species, design.size)

            if unused_space == 0:
                break

            elif inventory_amount <= 0:
                continue

            elif inventory_amount >= unused_space and \
                    max_quantity >= unused_space:
                amount = unused_space

            elif inventory_amount >= max_quantity:
                amount = max_quantity

            elif inventory_amount < max_quantity:
                amount = inventory_amount

            if amount > 0:
                required_flowers.append({
                    'species': species,
                    'size': design.size,
                    'amount': amount
                })
                unused_space -= amount
                bouquet_code = f'{bouquet_code}{amount}{species}'

        if unused_space > 0:
            return None

        for flower in required_flowers:
            self.remove_flowers(**flower)
        return f'{design.name}{design.size}{bouquet_code}'

    def build_bouquet_list(self) -> List[str]:
        """
        Build a list of all possible bouquets from the designs and the
        available flowers.

        :return list: The list of bouquet codes.
        """
        bouquet_codes = []
        bouquet_added = []

        for design in self._designs:
            bouquet_code = self.create_bouquet_code(design)
            bouquet_added.append(bouquet_code)

            if bouquet_code:
                bouquet_codes.append(bouquet_code)

        if any(bouquet_added):
            return bouquet_codes + self.build_bouquet_list()

        return bouquet_codes

    @staticmethod
    def _convert_flower_data_to_dict(data: str) -> Dict[str, int]:
        """
        Convert the data that represents the required flowers for a design to
        a dictionary.

        Example:
        The data `10a15b5c` converts to `{'a': 10, 'b': 15, 'c': 5}`.

        :param data: The data representing the required flowers.
        :return dict: The converted dict with the flower data.
        """
        flowers = {}
        for max_quantity, species in re.findall(r'(\d+)([a-z])', data):
            flowers[species] = int(max_quantity)
        return flowers
