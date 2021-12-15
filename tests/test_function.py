"""Unit tests  for main script."""

import json
import os

import pytest

import webhook
from . import helper

THIS_FOLDER = os.path.dirname(__file__)


class TestFunction:
    """Test Google Cloud Function."""

    @staticmethod
    def test_function():
        """Test function normal usage."""
        with open(os.path.join(THIS_FOLDER, "data", "request.json")) as file:
            body = json.load(file)
        req = helper.MockRequest(body=body)
        res = webhook.main(req)
        assert res.status_code == 200

    # @staticmethod
    # def test_invalid_args():
    #     """Test passing invalid arguments."""
    #     args_list = []

    #     for args in args_list:
    #         req = helper.MockRequest(args)
    #         with pytest.raises(ValueError):
    #             function.main(req)
