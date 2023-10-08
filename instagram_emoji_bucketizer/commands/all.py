# =====================================
# generator=datazen
# version=3.1.4
# hash=870e816c74edaa3a3e36618a677027d4
# =====================================

"""
A module aggregating package commands.
"""

# built-in
from typing import List as _List
from typing import Tuple as _Tuple

# third-party
from vcorelib.args import CommandRegister as _CommandRegister

# internal
from instagram_emoji_bucketizer.commands.parse_post import add_parse_post_cmd


def commands() -> _List[_Tuple[str, str, _CommandRegister]]:
    """Get this package's commands."""

    return [
        (
            "parse_post",
            "parse a given post short code",
            add_parse_post_cmd,
        ),
        ("noop", "command stub (does nothing)", lambda _: lambda _: 0),
    ]
