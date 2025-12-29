from dataclasses import dataclass, field

@dataclass
class ASRL:
    """Specific settings for RS-232/Serial."""
    baud_rate: int = 9600
    data_bits: int = 8
    stop_bits: float = 1.0
    parity: str = "none" # none, odd, even