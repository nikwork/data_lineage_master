from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class DataLineageObjectAttribure:
    """
    Store attribute state.
    """

    # Name and tile of attribute
    name: str

    # Attribute value
    value: str

    # Attrubute meta data. Helps to interpret value
    metadata_vlue: str

    id: str = (field(default_factory=uuid.uuid4))

    # Create timestamp
    create_timestamp: datetime = field(default_factory=datetime.utcnow)
