"""http://www.ewsolutions.com/enterprise-data-modeling/"""

from data_lineage_object import DataLineageObject, DataLineageObjectType
from enum import IntEnum
from dataclasses import dataclass, field


class ElementAbstractionLevel(IntEnum):
    """
    Element levels of abstraction and details
    """

    # Not defined
    NOT_DEFINED = 0

    # Conceptual:
    # data elements are presented in the form of terms and related constraints.
    CONCEPTUAL = 1

    # Logical, application-related:
    # data entities & attributes of a specific database
    # and related data transformation rules.
    LOGICAL_APPLICATION_RELATED = 2

    # Logical, not application related:
    # data entities & attributes and related data transformation rules.
    LOGICAL_NOT_APPLICATION_RELATED = 3

    # Physical: tables & columns & related
    # ETLs(Extract, Transform, Load).
    PHYSICAL = 4


@dataclass
class DataElement(DataLineageObject):
    """
    Data elements themselves form the key components of data lineage.
    Data elements can be specified on different levels of abstraction
    and details
    """

    # System/server name
    system_name: str = field(default_factory=str)

    # Database/schema/folder etc
    storage_name: str = field(default_factory=str)

    # Business key. Business key, wich usually concatenate system, data base
    # and object name
    full_name: str = field(default_factory=str)

    # Element level of abstraction and details (ElementAbstractionLevel)
    abstraction_level: int = field(default=0)

    def __post_init__(self):

        # Set object type
        self.data_lineage_object_type = DataLineageObjectType.DATA_ELEMENT

        # Calculate business key
        self.full_name = f"{self.system_name}.{self.storage_name}.{self.name}"
