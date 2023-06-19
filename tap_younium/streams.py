"""Stream type classes for tap-younium."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_younium.client import YouniumStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SubscriptionsStream(YouniumStream):
    name = "subscriptions"
    path = "/Subscriptions"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "subscription.json"  # noqa: ERA001
    