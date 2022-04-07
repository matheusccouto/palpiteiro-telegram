"""Testing helper functions."""

import json
from typing import Optional, Dict, Any

from werkzeug.datastructures import MultiDict


def read_json(path):
    """Read JSON file."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


class MockRequest:
    """A mock Flask request."""

    def __init__(
        self,
        query: Optional[dict] = None,
        body: Optional[dict] = None,
    ) -> None:
        self.query = query
        self.body = body

    @property
    def params(self) -> MultiDict:
        """Mock params."""
        return MultiDict(self.query)

    def get_json(self) -> Dict[str, Any]:
        """Mock get_json method."""
        if self.body is None:
            raise ValueError("No body defined.")
        return self.body
