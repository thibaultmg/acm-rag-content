import sys
from unittest.mock import patch

import pytest

from scripts.query_local import main


def test_query_local_missing_args(capsys):
    test_args = ["query_local.py"]
    with patch.object(sys, "argv", test_args):
        with pytest.raises(SystemExit):
            main()
        captured = capsys.readouterr()
        assert "arguments are required: -q/--query" in captured.err


def test_query_local_path_traversal(capsys):
    test_args = ["query_local.py", "-q", "test", "-p", "../../etc", "-v", "shadow"]
    with patch.object(sys, "argv", test_args):
        result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Invalid product or version path (path traversal detected)" in captured.err


def test_query_local_missing_dir(capsys):
    test_args = [
        "query_local.py",
        "-q",
        "test",
        "-p",
        "nonexistent_product",
        "-v",
        "0.0",
    ]
    with patch.object(sys, "argv", test_args):
        result = main()
        assert result == 1
        captured = capsys.readouterr()
        assert "Error: Vector DB directory not found at" in captured.err
