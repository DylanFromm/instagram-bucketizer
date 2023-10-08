import argparse
from collections import OrderedDict
from datetime import datetime
import json
from pathlib import Path
from typing import Any, Dict, List, Union

import emoji
import instaloader

# third-party
from vcorelib.args import CommandFunction


def normalize_to_datestr(date: Union[str, int, datetime]) -> str:
    if isinstance(date, str):
        return date
    elif isinstance(date, int):
        return datetime.fromtimestamp(date)
    elif isinstance(date, datetime):
        return str(date)
    assert False, f"Given data {date} is invalid! {type(date)}"


def normalize_to_epoch(date: Union[str, int, datetime]) -> int:
    if isinstance(date, str):
        utc_time = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        return ((utc_time) - datetime(1970, 1, 1)).total_seconds()
    elif isinstance(date, int):
        return date
    elif isinstance(date, datetime):
        return date.timestamp()
    assert False, f"Given data {date} is invalid! {type(date)}"


def normalize_to_dict(args: argparse.ArgumentParser) -> List[Dict[str, Any]]:
    """
    If given a comment file, parse and return dictionary
    if given a post code, get data, load into dictionary and return
    """

    ret_data: List[Dict[str, Any]] = []
    if args.comments_file:
        if args.comments_file.is_file():
            with open(args.comments_file, "r") as com_file:
                ret_data = json.load(com_file)
    elif args.post_code:
        assert args.username, "No username provided!"
        loader = instaloader.Instaloader()
        loader.load_session_from_file(args.username)
        post = instaloader.Post.from_shortcode(loader.context, args.post_code)

        for comment in post.get_comments():
            ret_data.append(
                {
                    "id": comment.id,
                    "created_at": normalize_to_datestr(comment.created_at_utc),
                    "text": comment.text,
                    "username": comment.owner.username,
                    "likes_count": comment.likes_count,
                    "answers": sorted(
                        [
                            {
                                "id": answer.id,
                                "created_at": normalize_to_datestr(
                                    answer.created_at_utc
                                ),
                                "text": answer.text,
                                "username": answer.owner.username,
                                "likes_count": answer.likes_count,
                            }
                            for answer in comment.answers
                        ],
                        key=lambda x: normalize_to_epoch(x["created_at"]),
                    ),
                }
            )
    return ret_data


def to_emoji_str(emoji_str: str) -> str:
    return emoji_str.encode("utf-16-be", "surrogatepass").decode("utf-16-be")


def parse_post_cmd(args: argparse.Namespace):
    comments_data = normalize_to_dict(args)

    if not comments_data:
        assert False, "No data found with given arguments!"

    sorted_data = sorted(
        comments_data, key=lambda x: normalize_to_epoch(x["created_at"])
    )
    for i in range(0, len(sorted_data)):
        sorted_data[i]["text"] = emoji.demojize(
            to_emoji_str(sorted_data[i]["text"])
        )

    with open(args.output_comments, "w") as com_file:
        com_file.write(json.dumps(sorted_data, indent=4))


def add_parse_post_cmd(parser: argparse.ArgumentParser) -> CommandFunction:
    """Add arbiter-command arguments to its parser."""
    parser.add_argument(
        "-p", "--post_code", help="Post code to parse", type=str
    )
    parser.add_argument(
        "--comments_file",
        help="Path to comments file to load without querying instagram",
        type=Path,
        default=None,
    )
    parser.add_argument("-u", "--username", type=str)
    parser.add_argument(
        "--output_comments",
        type=Path,
        default=Path("comments.json"),
        help="Path to output comments loaded from a post, defaults comments.json",
    )
    return parse_post_cmd
