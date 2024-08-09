"""Stream type classes for tap-younium."""

from __future__ import annotations
import json

from pathlib import Path

from tap_younium.client import YouniumStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

# base class for order based streams
class OrderStream(YouniumStream):
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

class SubscriptionsStream(OrderStream):
    name = "subscriptions"
    path = "/Subscriptions"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "orderNumber": record["orderNumber"],
        }

class SubscriptionVersionsStream(OrderStream):
    name = "subscription_versions"
    path = "/Subscriptions/{orderNumber}/versions"
    
    parent_stream_type = SubscriptionsStream
    ignore_parent_replication_keys = True
    state_partitioning_keys = []

    records_jsonpath = "$[*]"  # the versions resource returns plain arrays

class SalesOrdersStream(OrderStream):
    name = "sales_orders"
    path = "/SalesOrders"

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "orderNumber": record["orderNumber"],
        }

class SalesOrderVersionsStream(OrderStream):
    name = "sales_order_versions"
    path = "/SalesOrders/{orderNumber}/versions"
    
    parent_stream_type = SalesOrdersStream
    ignore_parent_replication_keys = True
    state_partitioning_keys = []

    records_jsonpath = "$[*]"  # the versions resource returns plain arrays

    
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
    