"""Tests standard tap features using the built-in SDK tests library."""

import datetime
import json

from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_younium.tap import TapYounium

# Specify the relative path to your JSON file
config_path = '.secrets/config.json'

# Read the JSON file into a dictionary
with open(config_path, 'r') as file:
    SAMPLE_CONFIG = json.load(file)


# aggressively limit the number of records to limit the number of child stream fetches and reduce 
# overall number of API requests for a test run
TEST_SUITE_CONFIG = SuiteConfig(
    max_records_limit=2 
)

# Run standard built-in tap tests from the SDK:
TestTapYounium = get_tap_test_class(
    tap_class=TapYounium,
    config=SAMPLE_CONFIG,
    suite_config = TEST_SUITE_CONFIG
)
