from dataclasses import dataclass, field

@dataclass
class TCPIP:
    """Specific settings for Ethernet/LAN."""
    port: int = 5025  # Standard SCPI port
    lan_device_name: str = "inst0"