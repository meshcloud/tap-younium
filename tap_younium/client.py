"""REST client handling, including YouniumStream base class."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qsl, urlparse

import requests
from singer_sdk.streams import RESTStream

from tap_younium.auth import YouniumAuthenticator
from functools import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class YouniumStream(RESTStream):
    """Younium stream class."""

    records_jsonpath = "$.data[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.nextPage"

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        if self.config.get('playground'):
            endpoint = "https://apisandbox.younium.com"
        else:
            endpoint = "https://api.younium.com"
        return endpoint

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return YouniumAuthenticator.create_for_stream(self, playground=self.config.get('playground'))

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            'api-version': '2.1'
        }
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_url_params(
        self,
        context: dict | None,  # noqa: ARG002
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            nexturl = urlparse(next_page_token)
            # we already are in the middle of sync, fetch next page
            query = parse_qsl(nexturl.query)
            params.update(query)
        elif self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key

        return params

    def apply_custom_fields(self, schema: dict, patch: dict | None):
        # many targets don't deal well with empty tag schemas so we remove the customFields property if we have no schema
        if (patch is None) :
            del schema["properties"]["customFields"]
        else:
            schema["properties"]["customFields"] = patch