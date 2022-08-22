from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class VersionedRelation:
    """
    Relation with hist timestamps
    """

    # Type of relation
    relation_type: str

    effective_from: field(default_factory=datetime.utcnow)

    effective_to: Optional[datetime]

    # Attribute value
    value: str

    id: str = (field(default_factory=uuid.uuid4))

    # Create timestamp
    create_timestamp: datetime = field(default_factory=datetime.utcnow)
