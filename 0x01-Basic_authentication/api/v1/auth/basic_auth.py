#!/usr/bin/env python3
"""Basic Authentication module
"""


import base64
import binascii
from api.v1.auth import Auth


class BasicAuth(Auth):
    """Basic Authentication class
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """Extract base64 authorization header
        """
        auth_header = authorization_header
        if auth_header is not None \
           and isinstance(auth_header, str) \
           and auth_header.startswith("Basic "):
            return auth_header.split(" ")[1]
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
        """Decode base64 authorization header
        """
        auth_header = base64_authorization_header
        try:
            if auth_header is not None and isinstance(auth_header, str):
                decoded_header = base64.b64decode(
                    auth_header,
                    validate=True
                    )
                return decoded_header.decode('utf-8')
        except binascii.Error:
            # Error from non-base64 data trying to be b64decoded.
            return None
        return None
