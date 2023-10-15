"""
Bucketizer class
"""

# built-in
import json
from typing import List, Type

import pandas as pd

# third party
from vcorelib.paths import Pathlike, normalize

# internal
from instagram_bucketizer.buckets import (
    Bucket,
    Comment,
    Comments,
    DataColumns,
    TBucket,
)
from instagram_bucketizer.buckets.emoji_tone import SkinToneBucket


def get_available_buckets() -> List[str]:
    return [cls.__name__ for cls in Bucket.__subclasses__()]


def get_bucket(name: str) -> TBucket:
    for cls in Bucket.__subclasses__():
        if cls.__name__ == name:
            return cls


class Bucketizer:
    """
    Given a string, get corresponding bucket child name
    hand list of comment dicts, create buckets
    print to excel
    """

    def __init__(self, bucket: str) -> None:
        available = get_available_buckets()
        assert (
            bucket in available
        ), f"Bucket {bucket} not in availble bucket!\n available: {available}!"

        self.bucket: TBucket = get_bucket(bucket)
        self.comments: Comments = []
        self.post_code = ""

    def load_comments(self, comments_file: Pathlike) -> None:
        comments_file = normalize(comments_file)
        with open(comments_file, "r") as read_fd:
            data = json.load(read_fd)
            self.post_code = data["post_code"]
            for comment in data["comments"]:
                self.comments.append(self.bucket.from_comment(comment))

    def extend(self, data: DataColumns) -> None:
        for comment in self.comments:
            comment.to_excel(data, self.post_code)

    def get_data(self) -> DataColumns:
        data = self.bucket.get_columns()
        self.extend(data)
        return data

    def write(self, data: DataColumns, output_file: Pathlike) -> None:
        output_file = normalize(output_file)
        output_data = pd.DataFrame(data=data)
        output_data.to_excel(output_file)