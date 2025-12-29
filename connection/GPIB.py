from dataclasses import dataclass, field
from typing import Optional

@dataclass
class GPIB:
    """Specific settings for GPIB."""
    enable_eoi: bool = True
    secondary_address: Optional[int] = None
