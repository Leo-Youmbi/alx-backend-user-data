#!/usr/bin/env python3
"""Session Authentication module
"""


import uuid
from api.v1.auth import Auth
from api.v1.utils import isNotNoneAndIsAString


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
