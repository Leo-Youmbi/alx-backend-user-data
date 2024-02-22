#!/usr/bin/env python3
"""Basic Authentication module
"""


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
