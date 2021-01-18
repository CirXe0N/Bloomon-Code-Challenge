from pathlib import Path

import pytest

from main import run


@pytest.fixture
def test_dir_in():
    directory = Path(__file__).parent / 'test_data'
    yield directory


@pytest.fixture
def test_dir_out():
    directory = Path(__file__).parent / 'test_data_out'
    yield directory

    for file in directory.rglob('*.txt'):
        file.unlink()


def test_running_main(test_dir_in, test_dir_out):
    run(test_dir_in, test_dir_out)

    expected_file = test_dir_out / 'out.example01.txt'

    assert expected_file.exists() is True

    with open(expected_file) as f:
        assert list(f.read().splitlines()) == ['AS1a2b', 'BL2a', 'AS2a1b']
