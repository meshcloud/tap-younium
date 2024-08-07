"""Younium tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_younium import streams


class TapYounium(Tap):
    """Younium tap class."""

    name = "tap-younium"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=False,  # Flag config as protected.
            description="",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="",
        ),
        th.Property(
            "sandbox",
            th.ArrayType(th.BooleanType),
            required=False,
            description="Target sandbox or production API",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "custom_field_schemas",
            th.ObjectType(
                th.Property("account", th.ObjectType(), required=False),
                th.Property("subscription", th.ObjectType(), required=False),
                th.Property("product", th.ObjectType(), required=False),
                th.Property("charge", th.ObjectType(), required=False),
                th.Property("invoice", th.ObjectType(), required=False)
            ),
            required=False,
        )

    ).to_dict()

    def discover_streams(self) -> list[streams.YouniumStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.SubscriptionsStream(self),
            streams.SubscriptionVersionsStream(self),
            streams.InvoicesStream(self),
            streams.ProductsStream(self),
            streams.BookingsStream(self),
            streams.AccountsStream(self)
        ]


if __name__ == "__main__":
    TapYounium.cli()
