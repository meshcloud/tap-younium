"""Stream type classes for tap-younium."""

from __future__ import annotations
import json

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers
from singer_sdk._singerlib.schema import Schema, resolve_schema_references
from tap_younium.client import YouniumStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SubscriptionsStream(YouniumStream):
    name = "subscriptions"
    path = "/Subscriptions"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "subscription.json"  # noqa: ERA001
    

class InvoicesStream(YouniumStream):
    name = "invoices"
    path = "/Invoices"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "invoice.json"  # noqa: ERA001
    
class ProductsStream(YouniumStream):
    name = "products"
    path = "/Products"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "product.json"  # noqa: ERA001
    

class BookingsStream(YouniumStream):
    name = "bookings"
    path = "/Bookings"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "booking.json"  # noqa: ERA001
    