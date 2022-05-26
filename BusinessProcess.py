"""https://appian.com/bpm/business-process-definition.html"""
from data_linage_object import DataLinageObject, DataLinageObjectType
from dataclasses import dataclass, field


@dataclass
class BisnessProcess(DataLinageObject):
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

        DataLinageObject.__post_init__(self)

        # Set object type
        self.data_linage_object_type = DataLinageObjectType.BUSINESS_PROCESS

        # Calculate business key
        self.process_natural_key = \
            f"{str(self.process_group_id)}_{str(self.process_id)}"
