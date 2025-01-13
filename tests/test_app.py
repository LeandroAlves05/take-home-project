import os
import json
import pytest
from app import create_index, search_index


@pytest.fixture
def setup_test_data(tmp_path):
    test_dir = tmp_path / "test_data"
    test_dir.mkdir()
    (test_dir / "file1.txt").write_text("Hello, world!")
    (test_dir / "file2.json").write_text('{"key": "value"}')
    (test_dir / "large_file.txt").write_text("A" * 10000)
    return test_dir


def test_create_index(setup_test_data, tmp_path):
    index_file = tmp_path / "index.json"
    create_index(setup_test_data, output_file=index_file)
    assert os.path.exists(index_file)

    with open(index_file) as f:
        index = json.load(f)
        assert len(index) == 3
        file_names = [entry["name"] for entry in index]

        assert "file1.txt" in file_names
        assert "file2.json" in file_names
        assert "large_file.txt" in file_names


def test_search_index_by_size_range(setup_test_data, tmp_path, capsys):
    index_file = tmp_path / "index.json"
    create_index(setup_test_data, output_file=index_file)

    search_index(index_file, size_min=10, size_max=500)

    captured = capsys.readouterr()
    assert "file1.txt" in captured.out
    assert "file2.json" in captured.out
    assert "large_file.txt" not in captured.out
