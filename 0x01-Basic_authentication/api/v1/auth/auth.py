#!/usr/bin/env python3
"""Authentication module
"""
from typing import List, Mapping, TypeVar
from flask import request


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

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user
        """
        return None
