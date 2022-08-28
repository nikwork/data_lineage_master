from dataclasses import dataclass, field, asdict
from enum import IntEnum
from datetime import datetime
import uuid


class DataLineageObjectType(IntEnum):
    """
    Data Lineage object type
    """

    # Base tape for all data Lineage objects.
    DATA_LINEAGE_OBJECT = 0

    # Data element object type
    DATA_ELEMENT = 1

    # Business process
    BUSINESS_PROCESS = 2


@dataclass
class DataLineageObject:
    """
    Base class for components of data Lineage
    """

    # Name and tile of object
    name: str

    # Data Lineage object type
    data_lineage_object_type: int = field(
        default=DataLineageObjectType.DATA_LINEAGE_OBJECT
        )

    # All key text tags for object
    tags: set = field(default_factory=set)

    # Optional string
    description: str = field(default=None)

    # Create timestamp
    create_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Last modified timestamp
    last_modified_timestamp: datetime = field(default_factory=datetime.utcnow)

    # Set of relations with other Data Lineage Objects
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


class DataLineageObjectUtils:

    MANDATORY_DLO_PROPERTIES = {
                                'name',
                                'data_lineage_object_type',
                                'create_timestamp',
                                'last_modified_timestamp',
                                'id',
                                'natural_key'
                            }

    def decompose_data_object(self, obj: DataLineageObject) -> dict:
        """Decompose data lineage object in to object and attributes nodes

        Args:
            obj (DataLineageObject): data lineage object

        Returns:
            dict: object('dlo_node') and attributes('dlo_attribute_nodes')
        """

        dlo_as_dict = asdict(obj)

        dlo_attribute_keys = dlo_as_dict.keys() - self.MANDATORY_DLO_PROPERTIES

        dlo_node = {
            k: dlo_as_dict.get(k, None) for k in self.MANDATORY_DLO_PROPERTIES
            }

        dlo_attribute_nodes = {
            k: dlo_as_dict.get(k, None) for k in dlo_attribute_keys
        }

        return {
                'dlo_node': dlo_node,
                'dlo_attribute_nodes': dlo_attribute_nodes
            }
