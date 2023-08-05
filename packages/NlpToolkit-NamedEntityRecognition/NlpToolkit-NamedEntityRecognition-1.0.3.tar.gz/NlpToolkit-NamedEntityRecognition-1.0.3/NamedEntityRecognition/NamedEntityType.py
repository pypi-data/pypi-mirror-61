from __future__ import annotations
from enum import Enum, auto

"""
Enumerator class for Named Entity types.
"""


class NamedEntityType(Enum):
    NONE = auto()
    PERSON = auto()
    ORGANIZATION = auto()
    LOCATION = auto()
    TIME = auto()
    MONEY = auto()

    """
    Static function to convert a string entity type to NamedEntityType type.

    PARAMETERS
    ----------
    entityType : str
        Entity type in string form
    
    RETURNS
    -------
    NamedEntityType
        Entity type in NamedEntityType form
    """

    @staticmethod
    def getNamedEntityType(entityType: str) -> NamedEntityType:
        for _type in NamedEntityType:
            if entityType == _type.name:
                return _type
        return NamedEntityType.NONE

    """
    Static function to convert a NamedEntityType to string form.
    
    PARAMETERS
    ----------
    entityType : NamedEntityType
        Entity type in NamedEntityType form
        
    RETURNS
    -------
    str
        Entity type in string form
    """

    @staticmethod
    def getNamedEntityString(namedEntityType: NamedEntityType) -> str:
        if namedEntityType is None:
            return "NONE"
        return namedEntityType.name
