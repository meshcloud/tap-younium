"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import json

from singer_sdk.testing import get_tap_test_class

from tap_younium.tap import TapYounium

# Specify the relative path to your JSON file
config_path = '.secrets/config.json'

# Read the JSON file into a dictionary
with open(config_path, 'r') as file:
    SAMPLE_CONFIG = json.load(file)

# Run standard built-in tap tests from the SDK:
TestTapYounium = get_tap_test_class(
    tap_class=TapYounium,
    config=SAMPLE_CONFIG,
)


# TODO: Create additional tests as appropriate for your tap.
