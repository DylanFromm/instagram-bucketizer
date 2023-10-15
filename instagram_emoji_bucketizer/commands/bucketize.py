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
    bucketizer.load_comments(args.comment_files[0])
    data = bucketizer.get_data()

    for comment in args.comment_files[1:]:
        next_bucket = Bucketizer(args.bucket)
        next_bucket.load_comments(comment)
        next_bucket.extend(data)
        
    bucketizer.write(data, args.output_file)


def add_bucketize_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add arbiter-command arguments to its parser."""
    parser.add_argument(
        "comment_files", nargs="+", help="Comment files to parse", type=Path
    )
    parser.add_argument(
        "--output_file",
        "-o",
        type=Path,
        default=Path("output.xlsx"),
        help="Path to output comments loaded from a post, defaults output.xlsx",
    )
    parser.add_argument("--bucket", "-b", required=True, type=str)
    return bucketize_cmd
