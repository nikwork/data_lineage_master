from dataclasses import dataclass, field
from enum import IntEnum
from datetime import datetime
import uuid


class DataLinageObjectType(IntEnum):
    """
    Data linage object type
    """

    # Base tape for all data linage objects.
    DATA_LINAGE_OBJECT = 0

    # Data element object type
    DATA_ELEMENT = 1

    # Business process
    BUSINESS_PROCESS = 2


@dataclass
class DataLinageObject:
    """
    Base class for components of data linage
    """

    # Name and tile of object
    name: str

    # Data linage object type
    data_linage_object_type: int = field(
        default=DataLinageObjectType.DATA_LINAGE_OBJECT
        )

    # All key text tags for object
    tags: set = field(default_factory=set)

    # Optional string
    description: str = field(default=None)

    # Create timestamp
    create_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Last modified timestamp
    last_modified_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Set of relations with other Data Linage Objects
    relations: set = field(default_factory=set)

    # 1 - object was changed in last commit
    changed_flg: bool = field(default=False)

    # True - object version is actual
    actual_flg: bool = field(default=False)

    # True - post init load actual state from data base
    # and save changes to external storage
    ext_storage_sync: bool = field(default=False)

    id: str = (field(default_factory=uuid.uuid4))

    version: int = field(default=0)

    def __post_init__(self):
        # self.id = str(uuid.uuid4())
        pass
