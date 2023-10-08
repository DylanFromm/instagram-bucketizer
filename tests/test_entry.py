"""
instagram_emoji_bucketizer - Test the program's entry-point.
"""

# built-in
from subprocess import check_output
from sys import executable
from unittest.mock import patch

# module under test
from instagram_emoji_bucketizer import PKG_NAME
from instagram_emoji_bucketizer.entry import (
    main as instagram_emoji_bucketizer_main,
)


def test_entry_basic():
    """Test basic argument parsing."""

    args = [PKG_NAME, "noop"]
    assert instagram_emoji_bucketizer_main(args) == 0

    with patch(
        "instagram_emoji_bucketizer.entry.entry", side_effect=SystemExit(1)
    ):
        assert instagram_emoji_bucketizer_main(args) != 0


def test_package_entry():
    """Test the command-line entry through the 'python -m' invocation."""

    check_output([executable, "-m", "instagram_emoji_bucketizer", "-h"])
