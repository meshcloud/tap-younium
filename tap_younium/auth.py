"""Younium Authentication."""

from __future__ import annotations
from xmlrpc.client import Boolean
from singer_sdk.authenticators import OAuthAuthenticator

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
            url = "https://younium-identity-server-sandbox.azurewebsites.net/connect/token"
        else:
            url = "https://younium-identity-server.azurewebsites.net/connect/token"
  
        return YouniumAuthenticator(stream, url)
        
    @property
    def oauth_request_body(self) -> dict:
        return {
            'grant_type': 'password',
            'client_id': 'apiclient',
            'username': self.config.get('username'),
            'password': self.config.get('password'),
            'scope':   'openid youniumapi profile'
        }