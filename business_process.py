"""https://appian.com/bpm/business-process-definition.html"""
from data_lineage_object import DataLineageObject, DataLineageObjectType
from dataclasses import dataclass, field


@dataclass
class BisnessProcess(DataLineageObject):
    """
    Business processes ensure a set of activities related to data processing.
    Business processes usually include references to related applications.
    """
    # Process group id
    process_group_id: int = field(default=0)

    # Process group name
    process_group_name: str = field(default_factory=str)

    # Process id
    process_id: int = field(default=0)

    # Owner (in product oriented organisations - product owner)
    owner: str = field(default_factory=str)

    # Process natural key. Calculated field
    process_natural_key: str = field(default_factory=str)

    def __post_init__(self):

        DataLineageObject.__post_init__(self)

        # Set object type
        self.data_lineage_object_type = DataLineageObjectType.BUSINESS_PROCESS

        # Calculate business key
        self.process_natural_key = \
            f"{str(self.process_group_id)}_{str(self.process_id)}"
