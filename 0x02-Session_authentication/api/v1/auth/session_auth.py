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
        if isNotNoneAndIsAString(user_id):
            session_id = uuid.uuid4()
            type(self).user_id_by_session_id.__setitem__(session_id, user_id)
            return session_id
        return None
