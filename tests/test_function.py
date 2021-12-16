"""Unit tests  for main script."""

import os

import webhook
from . import helper

THIS_FOLDER = os.path.dirname(__file__)


class TestFunction:
    """Test Google Cloud Function."""

    @staticmethod
    def test_function():
        """Test function normal usage."""
        body = helper.read_json(os.path.join(THIS_FOLDER, "data", "request.json"))
        req = helper.MockRequest(body=body)
        res = webhook.main(req)
        assert res.status_code == 200


class TestFormatSquad:
    """Test function that format the squad message."""

    @classmethod
    def setup_class(cls):
        """Setup class."""
        res = helper.read_json(os.path.join(THIS_FOLDER, "data", "response.json"))
        cls.formatted = webhook.format_answer(res)

    def test_length(self):
        """Test function normal usage."""
        assert len(self.formatted) < 4096
