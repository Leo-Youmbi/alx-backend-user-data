#!/usr/bin/env python3
"""Session Authentication module
"""


import uuid
from api.v1.auth import Auth
from api.v1.utils import isNotNoneAndIsAString
from models.user import User


class SessionAuth(Auth):
    """Session Authentication class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a new session

        Args:
            user_id (str, optional): The id of a user. Defaults to None.

        Returns:
            str: the id of the newly created id
        """
        if isNotNoneAndIsAString(user_id):
            session_id = uuid.uuid4()
            type(self).user_id_by_session_id.__setitem__(session_id, user_id)
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns the user id associated with the given session
        """
        if isNotNoneAndIsAString(session_id):
            return type(self).user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """Returns the current user"""
        session_id = self.session_cookie(request)
        if session_id is not None:
            user_id = self.user_id_for_session_id(session_id)

            if user_id is not None:
                return User.get(user_id)

        return None
