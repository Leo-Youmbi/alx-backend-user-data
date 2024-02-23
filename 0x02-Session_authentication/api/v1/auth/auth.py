#!/usr/bin/env python3
"""Authentication module
"""
import os
from typing import List


class Auth:
    """Authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if url requires authentication
        """
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Returns authorization header
        """
        if request is not None and 'Authorization' in request.headers:
            return request.headers.get('Authorization')
        return None

    def current_user(self, request=None):
        """Returns current user
        """
        return None

    def session_cookie(self, request=None):
        """Gets the session id from cookie
        """
        if request is None:
            return None

        SESSION_NAME = os.getenv('SESSION_NAME', None)
        if SESSION_NAME is None:
            return None
        return request.cookies.get(SESSION_NAME)
