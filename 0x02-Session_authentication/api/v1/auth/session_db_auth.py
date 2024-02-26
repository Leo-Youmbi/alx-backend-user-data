#!/usr/bin/env python3
"""Sessions in DB Authentication module
"""


from datetime import datetime, timedelta
from api.v1.auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Sessions in DB Authentication class
    """

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

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id associated with the given session"""
        if session_id is None:
            return None

        try:
            user_session_list = UserSession.search({'session_id': session_id})
        except KeyError:
            return None

        if len(user_session_list) == 0:
            return None

        user_session: UserSession = user_session_list[0]
        created_at = user_session.created_at
        session_duration = timedelta(seconds=self.session_duration)
        if created_at + session_duration < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Delete session"""
        session_id = self.session_cookie()
        if session_id is None:
            return False

        user_session_list = UserSession.search({'session_id': session_id})
        if len(user_session_list) == 0:
            return False

        user_session: UserSession = user_session_list[0]
        user_session.remove()
        return True
