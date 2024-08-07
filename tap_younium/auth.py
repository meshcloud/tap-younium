"""Younium Authentication."""

from __future__ import annotations
from xmlrpc.client import Boolean
from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.helpers._util import utc_now

import requests


class YouniumAuthenticator(OAuthAuthenticator):
    """Authenticator class for Younium."""

        
    @classmethod
    def create_for_stream(
        cls,
        stream,
        playground: Boolean
    ) -> YouniumAuthenticator:
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        if playground:
            url = "https://api.sandbox.younium.com/auth/token"
        else:
            url = "https://api.younium.com/auth/token"
  
        return YouniumAuthenticator(stream, url)
        
    @property
    def oauth_request_body(self) -> dict:
        return {
            'clientId': self.client_id,
            'secret': self.client_secret
        }

    # unfortunately Younium API uses non-standard json response properties like accessToken instead of access_token
    # so we have to override the base class implementation here, using a bit of copy/paste/replace
    def update_access_token(self) -> None:
        """Update `access_token` along with: `last_refreshed` and `expires_in`.

        Raises:
            RuntimeError: When OAuth login fails.
        """
        request_time = utc_now()
        auth_request_payload = self.oauth_request_payload
        token_response = requests.post(
            self.auth_endpoint,
            headers= {
                'Content-Type': 'application/json'
            },
            json=auth_request_payload,
            timeout=60,
        )
        try:
            token_response.raise_for_status()
        except requests.HTTPError as ex:
            msg = f"Failed OAuth login, response was '{token_response.json()}' for '{auth_request_payload}'. {ex}"
            raise RuntimeError(msg) from ex

        self.logger.info("OAuth authorization attempt was successful.")

        token_json = token_response.json()
        self.access_token = token_json["accessToken"]
        expiration = token_json.get("expiresIn", self._default_expiration)
        self.expires_in = int(expiration) if expiration else None
        if self.expires_in is None:
            self.logger.debug(
                "No expires_in received in OAuth response and no "
                "default_expiration set. Token will be treated as if it never "
                "expires.",
            )
        self.last_refreshed = request_time
