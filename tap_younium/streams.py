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

    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "subscription.json"
        schema = json.loads(Path(schema_filepath).read_text())

        custom = self.config["custom_field_schemas"]
        
        self.apply_custom_fields(schema, custom.get("subscription"))
        self.apply_custom_fields(schema["properties"]["products"]["items"], custom.get("product"))
        self.apply_custom_fields(schema["properties"]["products"]["items"]["properties"]["charges"]["items"], custom.get("charge"))

        return schema
    

class InvoicesStream(YouniumStream):
    name = "invoices"
    path = "/Invoices"
    primary_keys = ["id"]
    replication_key = None

    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "invoice.json"
        schema = json.loads(Path(schema_filepath).read_text())

        custom = self.config["custom_field_schemas"]
        
        self.apply_custom_fields(schema, custom.get("invoice"))
        self.apply_custom_fields(schema["properties"]["invoiceLines"]["items"], custom.get("charge"))

        return schema

    
class ProductsStream(YouniumStream):
    name = "products"
    path = "/Products"
    primary_keys = ["id"]
    replication_key = None
    
    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "product.json"
        schema = json.loads(Path(schema_filepath).read_text())

        custom = self.config["custom_field_schemas"]
        
        self.apply_custom_fields(schema, custom.get("product"))
        self.apply_custom_fields(schema["properties"]["chargePlans"]["items"]["properties"]["charges"]["items"], custom.get("charge"))

        return schema
    
    
class BookingsStream(YouniumStream):
    name = "bookings"
    path = "/Bookings"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "booking.json" 

class AccountsStream(YouniumStream):
    name = "accounts"
    path = "/Accounts"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "account.json" 

    @property
    def schema(self) -> dict:
        """Get dynamic schema including the configured tag schema

        Returns:
            JSON Schema dictionary for this stream.
        """
    
        schema_filepath = SCHEMAS_DIR / "account.json"
        schema = json.loads(Path(schema_filepath).read_text())

        custom = self.config["custom_field_schemas"]
        
        self.apply_custom_fields(schema, custom.get("account"))
        
        return schema
    