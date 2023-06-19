"""Younium tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_younium import streams


class TapYounium(Tap):
    """Younium tap class."""

    name = "tap-younium"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "username",
            th.StringType,
            required=True,
            secret=False,  # Flag config as protected.
            description="",
        ),
        th.Property(
            "password",
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
        )
    ).to_dict()

    def discover_streams(self) -> list[streams.YouniumStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.SubscriptionsStream(self),
            streams.InvoicesStream(self),
            streams.ProductsStream(self),
        ]


if __name__ == "__main__":
    TapYounium.cli()
