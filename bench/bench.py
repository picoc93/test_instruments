#!/usr/bin/env python3
"""
Simplified Bench class for managing multiple instruments from JSON configuration.
"""
import json
from typing import Dict, Optional
from instrument_base import Instrument


class Bench:
    """
    Simple bench manager - loads instruments from JSON and provides access.
    
    Usage:
        bench = Bench('config.json')
        bench.load()
        bench.connect_all()
        psu = bench['psu_1']
        psu.write('VOLT 5.0')
        bench.disconnect_all()
    """
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.instruments: Dict[str, Instrument] = {}
    
    def load(self):
        """Load instruments from JSON configuration."""
        with open(self.config_path, 'r') as f:
            data = json.load(f)
        
        for item in data['instruments']:
            # Get timeout in seconds (convert from ms if needed)
            timeout = item.get('timeout', 1.0)
            if timeout > 100:  # Assume milliseconds if > 100
                timeout = timeout / 1000.0
            
            # Create instrument using your custom class or a generic one
            instrument_class = item.get('class', Instrument)
            if isinstance(instrument_class, str):
                # If class is specified as string, you would import it
                # For now, just use base Instrument
                instrument_class = Instrument
            
            # Store metadata for later use
            instrument = instrument_class(
                resource_id=item['resource_id'],
                timeout=timeout
            )
            instrument._connect_kwargs = item.get('connection_kwargs', {})
            instrument._config = item
            
            self.instruments[item['id']] = instrument
    
    def save(self, output_path: Optional[str] = None):
        """Save current configuration to JSON."""
        if output_path is None:
            output_path = self.config_path
        
        config = {
            'instruments': [
                inst._config for inst in self.instruments.values()
            ]
        }
        
        with open(output_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def add_instrument(self, instrument_id: str, resource_id: str, 
                      timeout: float = 1.0, connection_kwargs: dict = None):
        """
        Add a new instrument.
        
        Args:
            instrument_id: Unique ID for the instrument
            resource_id: Connection string (GPIB, ASRL, TCPIP, USB)
            timeout: Timeout in seconds
            connection_kwargs: Parameters for connect() method
        """
        if connection_kwargs is None:
            connection_kwargs = {}
        
        instrument = Instrument(resource_id, timeout)
        instrument._connect_kwargs = connection_kwargs
        instrument._config = {
            'id': instrument_id,
            'resource_id': resource_id,
            'timeout': timeout,
            'connection_kwargs': connection_kwargs
        }
        
        self.instruments[instrument_id] = instrument
        print(f"Added instrument: {instrument_id}")
    
    def remove_instrument(self, instrument_id: str):
        """
        Remove an instrument.
        
        Args:
            instrument_id: ID of instrument to remove
        """
        if instrument_id not in self.instruments:
            print(f"Instrument {instrument_id} not found")
            return
        
        instrument = self.instruments[instrument_id]
        if instrument.is_connected():
            instrument.disconnect()
        
        del self.instruments[instrument_id]
        print(f"Removed instrument: {instrument_id}")
    
    def connect_instrument(self, instrument_id: str):
        """
        Connect to a specific instrument.
        
        Args:
            instrument_id: ID of instrument to connect
        """
        if instrument_id not in self.instruments:
            print(f"Instrument {instrument_id} not found")
            return False
        
        instrument = self.instruments[instrument_id]
        try:
            instrument.connect(**instrument._connect_kwargs)
            print(f"✓ Connected to {instrument_id}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to {instrument_id}: {e}")
            return False
    
    def disconnect_instrument(self, instrument_id: str):
        """
        Disconnect from a specific instrument.
        
        Args:
            instrument_id: ID of instrument to disconnect
        """
        if instrument_id not in self.instruments:
            print(f"Instrument {instrument_id} not found")
            return False
        
        instrument = self.instruments[instrument_id]
        try:
            instrument.disconnect()
            print(f"Disconnected from {instrument_id}")
            return True
        except Exception as e:
            print(f"Error disconnecting {instrument_id}: {e}")
            return False
    
    def connect_all(self):
        """Connect to all instruments."""
        results = {}
        for inst_id in self.instruments:
            results[inst_id] = self.connect_instrument(inst_id)
        return results
    
    def disconnect_all(self):
        """Disconnect from all instruments."""
        results = {}
        for inst_id in self.instruments:
            results[inst_id] = self.disconnect_instrument(inst_id)
        return results
    
    def get_status(self):
        """
        Get status of all instruments.
        
        Returns:
            Dictionary with status information
        """
        status = {
            'total': len(self.instruments),
            'connected': sum(1 for i in self.instruments.values() if i.is_connected()),
            'disconnected': sum(1 for i in self.instruments.values() if not i.is_connected()),
            'instruments': {}
        }
        
        for inst_id, instrument in self.instruments.items():
            status['instruments'][inst_id] = {
                'resource_id': instrument.resource_id,
                'connected': instrument.is_connected()
            }
        
        return status
    
    def print_status(self):
        """Print formatted status of all instruments."""
        status = self.get_status()
        
        print("\n" + "="*60)
        print("BENCH STATUS")
        print("="*60)
        print(f"Total: {status['total']} | Connected: {status['connected']} | Disconnected: {status['disconnected']}")
        print("-"*60)
        
        for inst_id, info in status['instruments'].items():
            state = "✓ CONNECTED" if info['connected'] else "✗ DISCONNECTED"
            print(f"{inst_id:15} | {info['resource_id']:35} | {state}")
        
        print("="*60 + "\n")
    
    def test_all_connections(self):
        """
        Test all connections by querying device ID.
        
        Returns:
            Dictionary with device IDs
        """
        results = {}
        print("\n" + "="*60)
        print("TESTING CONNECTIONS")
        print("="*60)
        
        for inst_id, instrument in self.instruments.items():
            if not instrument.is_connected():
                results[inst_id] = None
                print(f"{inst_id}: Not connected")
                continue
            
            try:
                device_id = instrument.get_device_id()
                results[inst_id] = device_id
                print(f"{inst_id}: {device_id}")
            except Exception as e:
                results[inst_id] = None
                print(f"{inst_id}: Error - {e}")
        
        print("="*60 + "\n")
        return results
    
    def __getitem__(self, instrument_id: str) -> Instrument:
        """Get instrument by ID using bench['id'] syntax."""
        return self.instruments[instrument_id]
    
    def __contains__(self, instrument_id: str) -> bool:
        """Check if instrument exists using 'id' in bench syntax."""
        return instrument_id in self.instruments
    
    def __iter__(self):
        """Iterate over instrument IDs."""
        return iter(self.instruments)
    
    def __len__(self):
        """Number of instruments."""
        return len(self.instruments)
    
    def __enter__(self):
        """Context manager entry."""
        self.load()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect all."""
        self.disconnect_all()
        return False
