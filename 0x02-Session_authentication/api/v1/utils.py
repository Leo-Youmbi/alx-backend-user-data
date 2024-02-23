#!/usr/bin/env python3
"""Utility functions module
"""


from typing import Any, TypeVar
from uuid import UUID


user_type = TypeVar('user_type')

def isNotNoneAndIsAString(variable: Any) -> bool:
    """Check if variable is not None and is a string
    """
    return variable is not None \
        and isinstance(variable, (str, UUID))
