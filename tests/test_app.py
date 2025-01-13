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
    return test_dir


def test_create_index(setup_test_data, tmp_path):
    index_file = tmp_path / "index.json"
    create_index(setup_test_data, output_file=index_file)
    assert os.path.exists(index_file)
    with open(index_file) as f:
        index = json.load(f)
        assert len(index) == 2
        assert any(entry["name"] == "file1.txt" for entry in index)


def test_search_index_by_name(setup_test_data, tmp_path, capsys):
    index_file = tmp_path / "index.json"
    create_index(setup_test_data, output_file=index_file)

    search_index(index_file, query="file1.txt")

    captured = capsys.readouterr()
    assert "file1.txt" in captured.out
    assert "Hello, world!" not in captured.out


def test_search_index_by_type(setup_test_data, tmp_path, capsys):
    index_file = tmp_path / "index.json"
    create_index(setup_test_data, output_file=index_file)

    search_index(index_file, file_type="application/json")

    captured = capsys.readouterr()
    assert "file2.json" in captured.out
    assert "file1.txt" not in captured.out
