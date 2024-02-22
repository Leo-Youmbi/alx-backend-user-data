#!/usr/bin/env python3
"""Basic Authentication module
"""


import base64
import binascii
from typing import Any, Tuple, TypeVar
from api.v1.auth import Auth
from models.user import User


def isNotNoneAndIsAString(variable: Any) -> bool:
    """Check if variable is not None and is a string
    """
    return variable is not None \
        and isinstance(variable, str)


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
        if isNotNoneAndIsAString(auth_header) \
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
            if isNotNoneAndIsAString(auth_header):
                decoded_header = base64.b64decode(
                    auth_header,
                    validate=True
                    )
                return decoded_header.decode('utf-8')
        except binascii.Error:
            # Error from non-base64 data trying to be b64decoded.
            return None
        return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> Tuple[str, str]:
        """Extract user credentials
        """
        auth_header = decoded_base64_authorization_header
        if isNotNoneAndIsAString(auth_header) \
           and ':' in auth_header:
            creds = auth_header.split(':', 1)
            return creds[0], creds[1]
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
            ) -> TypeVar('User'):
        if isNotNoneAndIsAString(user_email) \
           and isNotNoneAndIsAString(user_pwd):

            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None
