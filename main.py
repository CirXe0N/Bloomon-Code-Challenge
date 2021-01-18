from pathlib import Path

from resource_planners import BouquetResourcePlanner


def run(input_dir: Path, output_dir: Path) -> None:
    for path in input_dir.rglob("*.txt"):
        planner = BouquetResourcePlanner()
        planner.import_from_file(path)
        bouquet_codes = planner.build_bouquet_list()
        with open(output_dir / f"out.{path.name}", mode="w") as f:
            bouquet_codes.reverse()
            f.writelines(f"{bouquet_code}\n" for bouquet_code in bouquet_codes)


if __name__ == "__main__":
    dir_in = Path(__file__).parent.parent / "inputs"
    dir_out = Path(__file__).parent.parent / "outputs"
    run(dir_in, dir_out)
    print(f"Bouquets created! The results can be found in the `outputs` directory.")
