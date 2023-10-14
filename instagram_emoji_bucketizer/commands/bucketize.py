"""
Bucket emojis

currently just looking at modifiable skin tone emojis and bucketing them
"""

# built-in
import argparse
from pathlib import Path

# third-party
from vcorelib.args import CommandFunction

# internal
from instagram_emoji_bucketizer.buckets.bucketizer import Bucketizer


def bucketize_cmd(args: argparse.Namespace):
    bucketizer = Bucketizer(args.bucket)
    bucketizer.load_comments(args.comments_file)
    bucketizer.write(args.output_file, args.post_id)


def add_bucketize_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add arbiter-command arguments to its parser."""
    parser.add_argument(
        "--comments_file",
        "-c",
        help="Path to comments file to bucket into a excel file",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "--output_file",
        "-o",
        type=Path,
        default=Path("output.xlsx"),
        help="Path to output comments loaded from a post, defaults output.xlsx",
    )
    parser.add_argument(
        "--post_id",
        "-p",
        help="Post id to prefix in table",
        type=str,
        default="",
    )
    parser.add_argument("--bucket", "-b", required=True, type=str)
    return bucketize_cmd
