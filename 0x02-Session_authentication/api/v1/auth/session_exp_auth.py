#!/usr/bin/env python3
"""Session Expiry Authentication module
"""


from datetime import datetime, timedelta
import os
from api.v1.auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Expiry Authentication class
    """

    def __init__(self):
        """Initialize the session"""
        session_duration = os.getenv('SESSION_DURATION', None)
        try:
            session_duration = int(session_duration)
            self.session_duration = session_duration
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a new session

        Args:
            user_id (str, optional): The id of a user. Defaults to None.

        Returns:
            str: the id of the newly created session
        """
        session_id = super().create_session(user_id=user_id)
        if session_id is None:
            return None

        self.user_id_by_session_id.__setitem__(session_id, {
            'user_id': user_id,
            'created_at': datetime.now(),
        })
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id associated with the given session
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id.keys():
            return None

        session_dictionary: dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary['user_id']

        if 'created_at' not in session_dictionary.keys():
            return None

        created_at: datetime = session_dictionary['created_at']
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.now():
            return None

        return session_dictionary.__getitem__('user_id')
