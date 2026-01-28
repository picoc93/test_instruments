#!/usr/bin/env python3
"""
Bench class for managing multiple electronic test instruments.
Works with the existing Instrument base class and connection handlers.
"""
import json
from typing import Dict, List, Optional, Any
from instrument_base import Instrument


class GenericInstrument(Instrument):
    """
    Generic instrument implementation for use with Bench.
    Can be subclassed for specific instrument types.
    """
    
    def __init__(self, resource_id: str, timeout: float = 1.0, **kwargs):
        """
        Initialize generic instrument.
        
        Args:
            resource_id: Connection string
            timeout: Timeout in seconds
            **kwargs: Additional metadata (type, brand, model, etc.)
        """
        super().__init__(resource_id, timeout)
        self.metadata = kwargs
        self.instrument_id = kwargs.get('id', resource_id)
        self.instrument_type = kwargs.get('type', 'generic')
        self.brand = kwargs.get('brand', 'unknown')
        self.model = kwargs.get('model', 'unknown')
    
    def get_device_id(self) -> str:
        """Get device ID using standard *IDN? command."""
        try:
            return self.query("*IDN?")
        except:
            return "ID not available"
    
    def __str__(self):
        """String representation."""
        status = "connected" if self.is_connected() else "disconnected"
        return f"{self.instrument_id}: {self.brand} {self.model} ({self.instrument_type}) - {status}"
    
    def __repr__(self):
        """Detailed representation."""
        return (f"GenericInstrument(id='{self.instrument_id}', type='{self.instrument_type}', "
                f"brand='{self.brand}', model='{self.model}', resource='{self.resource_id}')")


class Bench:
    """
    Manages a collection of electronic test instruments.
    
    Features:
    - Load/save instrument configurations from/to JSON
    - Connect/disconnect all or specific instruments
    - Query instruments by ID or type
    - Add/remove instruments dynamically
    - Status monitoring and reporting
    """
    
    def __init__(self, config_path: str):
        """
        Initialize the bench with a configuration file.
        
        Args:
            config_path: Path to the JSON configuration file
        """
        self.config_path = config_path
        self.instruments: Dict[str, Instrument] = {}
        self.config_data: Optional[Dict] = None
    
    def load_config(self) -> bool:
        """
        Load the instrument configuration from JSON file.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.config_path, 'r') as f:
                self.config_data = json.load(f)
            
            # Create instrument objects
            for instr_config in self.config_data.get('instruments', []):
                instrument_id = instr_config.get('id')
                if not instrument_id:
                    print(f"Warning: Instrument configuration missing 'id' field: {instr_config}")
                    continue
                
                # Extract connection parameters
                resource_id = instr_config.get('address') or instr_config.get('resource_id')
                if not resource_id:
                    print(f"Warning: Instrument {instrument_id} missing address/resource_id")
                    continue
                
                timeout = instr_config.get('settings', {}).get('timeout', 1000) / 1000.0  # Convert ms to seconds
                
                # Create instrument
                self.instruments[instrument_id] = GenericInstrument(
                    resource_id=resource_id,
                    timeout=timeout,
                    id=instrument_id,
                    type=instr_config.get('type', 'generic'),
                    brand=instr_config.get('brand', 'unknown'),
                    model=instr_config.get('model', 'unknown'),
                    settings=instr_config.get('settings', {})
                )
            
            print(f"Loaded {len(self.instruments)} instrument(s) from configuration")
            return True
            
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            return False
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
    
    def connect_all(self) -> Dict[str, bool]:
        """
        Connect to all instruments in the configuration.
        
        Returns:
            Dictionary with instrument IDs as keys and connection status as values
        """
        results = {}
        for inst_id, instrument in self.instruments.items():
            try:
                # Get connection settings from metadata
                settings = instrument.metadata.get('settings', {})
                
                # Extract connection parameters based on type
                connect_kwargs = {}
                if 'baud_rate' in settings:
                    connect_kwargs['baud_rate'] = settings['baud_rate']
                if 'data_bits' in settings:
                    connect_kwargs['bytesize'] = settings['data_bits']
                if 'parity' in settings:
                    parity_map = {
                        'none': 'N',
                        'even': 'E',
                        'odd': 'O',
                        'mark': 'M',
                        'space': 'S'
                    }
                    connect_kwargs['parity'] = parity_map.get(settings['parity'].lower(), 'N')
                if 'stop_bits' in settings:
                    connect_kwargs['stopbits'] = settings['stop_bits']
                
                instrument.connect(**connect_kwargs)
                results[inst_id] = True
                print(f"✓ Connected to {inst_id}")
                
            except Exception as e:
                results[inst_id] = False
                print(f"✗ Failed to connect to {inst_id}: {e}")
        
        return results
    
    def connect_instrument(self, instrument_id: str, **kwargs) -> bool:
        """
        Connect to a specific instrument by ID.
        
        Args:
            instrument_id: Instrument ID from configuration
            **kwargs: Additional connection parameters to override defaults
            
        Returns:
            True if successful, False otherwise
        """
        instrument = self.instruments.get(instrument_id)
        if not instrument:
            print(f"Error: Instrument '{instrument_id}' not found in configuration")
            return False
        
        try:
            # Merge default settings with provided kwargs
            settings = instrument.metadata.get('settings', {})
            connect_kwargs = {}
            
            if 'baud_rate' in settings:
                connect_kwargs['baud_rate'] = settings['baud_rate']
            if 'data_bits' in settings:
                connect_kwargs['bytesize'] = settings['data_bits']
            if 'parity' in settings:
                parity_map = {'none': 'N', 'even': 'E', 'odd': 'O', 'mark': 'M', 'space': 'S'}
                connect_kwargs['parity'] = parity_map.get(settings['parity'].lower(), 'N')
            if 'stop_bits' in settings:
                connect_kwargs['stopbits'] = settings['stop_bits']
            
            # Override with user-provided kwargs
            connect_kwargs.update(kwargs)
            
            instrument.connect(**connect_kwargs)
            print(f"✓ Connected to {instrument_id}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to connect to {instrument_id}: {e}")
            return False
    
    def disconnect_all(self) -> Dict[str, bool]:
        """
        Disconnect from all instruments.
        
        Returns:
            Dictionary with instrument IDs as keys and disconnection status as values
        """
        results = {}
        for inst_id, instrument in self.instruments.items():
            try:
                instrument.disconnect()
                results[inst_id] = True
            except Exception as e:
                print(f"Error disconnecting {inst_id}: {e}")
                results[inst_id] = False
        
        return results
    
    def disconnect_instrument(self, instrument_id: str) -> bool:
        """
        Disconnect from a specific instrument.
        
        Args:
            instrument_id: Instrument ID
            
        Returns:
            True if successful, False otherwise
        """
        instrument = self.instruments.get(instrument_id)
        if not instrument:
            print(f"Error: Instrument '{instrument_id}' not found")
            return False
        
        try:
            instrument.disconnect()
            return True
        except Exception as e:
            print(f"Error disconnecting {instrument_id}: {e}")
            return False
    
    def get_instrument(self, instrument_id: str) -> Optional[Instrument]:
        """
        Get an instrument object by ID.
        
        Args:
            instrument_id: Instrument ID
            
        Returns:
            Instrument object or None if not found
        """
        return self.instruments.get(instrument_id)
    
    def get_instruments_by_type(self, instrument_type: str) -> List[Instrument]:
        """
        Get all instruments of a specific type.
        
        Args:
            instrument_type: Type of instrument (psu, scope, awg, dmm, etc.)
            
        Returns:
            List of Instrument objects matching the type
        """
        return [
            inst for inst in self.instruments.values()
            if inst.instrument_type == instrument_type
        ]
    
    def get_all_instruments(self) -> Dict[str, Instrument]:
        """
        Get all instrument objects.
        
        Returns:
            Dictionary of all instruments (ID: Instrument)
        """
        return self.instruments
    
    def test_all_connections(self) -> Dict[str, Optional[str]]:
        """
        Test all instrument connections by querying device ID.
        
        Returns:
            Dictionary with instrument IDs as keys and device ID responses as values
        """
        results = {}
        for inst_id, instrument in self.instruments.items():
            if instrument.is_connected():
                try:
                    device_id = instrument.get_device_id()
                    results[inst_id] = device_id
                    print(f"{inst_id}: {device_id}")
                except Exception as e:
                    results[inst_id] = None
                    print(f"{inst_id}: Error - {e}")
            else:
                results[inst_id] = None
                print(f"{inst_id}: Not connected")
        
        return results
    
    def add_instrument(self, instrument_config: Dict[str, Any]) -> bool:
        """
        Add a new instrument to the bench.
        
        Args:
            instrument_config: Instrument configuration dictionary
            
        Returns:
            True if successful, False otherwise
        """
        instrument_id = instrument_config.get('id')
        if not instrument_id:
            print("Error: Instrument configuration must have an 'id' field")
            return False
        
        resource_id = instrument_config.get('address') or instrument_config.get('resource_id')
        if not resource_id:
            print(f"Error: Instrument {instrument_id} missing address/resource_id")
            return False
        
        if instrument_id in self.instruments:
            print(f"Warning: Instrument '{instrument_id}' already exists. Overwriting...")
        
        try:
            timeout = instrument_config.get('settings', {}).get('timeout', 1000) / 1000.0
            
            self.instruments[instrument_id] = GenericInstrument(
                resource_id=resource_id,
                timeout=timeout,
                id=instrument_id,
                type=instrument_config.get('type', 'generic'),
                brand=instrument_config.get('brand', 'unknown'),
                model=instrument_config.get('model', 'unknown'),
                settings=instrument_config.get('settings', {})
            )
            
            print(f"Added instrument: {instrument_id}")
            return True
            
        except Exception as e:
            print(f"Error adding instrument: {e}")
            return False
    
    def remove_instrument(self, instrument_id: str) -> bool:
        """
        Remove an instrument from the bench.
        
        Args:
            instrument_id: Instrument ID to remove
            
        Returns:
            True if successful, False otherwise
        """
        instrument = self.instruments.get(instrument_id)
        if not instrument:
            print(f"Error: Instrument '{instrument_id}' not found")
            return False
        
        # Disconnect if connected
        if instrument.is_connected():
            instrument.disconnect()
        
        del self.instruments[instrument_id]
        print(f"Removed instrument: {instrument_id}")
        return True
    
    def save_config(self, output_path: Optional[str] = None) -> bool:
        """
        Save the current configuration to a JSON file.
        
        Args:
            output_path: Output file path. If None, overwrites the original config.
            
        Returns:
            True if successful, False otherwise
        """
        if output_path is None:
            output_path = self.config_path
        
        try:
            # Build configuration from current instruments
            config = {
                'instruments': [
                    {
                        'id': inst.instrument_id,
                        'type': inst.instrument_type,
                        'brand': inst.brand,
                        'model': inst.model,
                        'address': inst.resource_id,
                        'settings': inst.metadata.get('settings', {})
                    }
                    for inst in self.instruments.values()
                ]
            }
            
            with open(output_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print(f"Configuration saved to {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get status of all instruments.
        
        Returns:
            Dictionary with instrument status information
        """
        status = {
            'total_instruments': len(self.instruments),
            'connected': sum(1 for inst in self.instruments.values() if inst.is_connected()),
            'disconnected': sum(1 for inst in self.instruments.values() if not inst.is_connected()),
            'instruments': {}
        }
        
        for inst_id, instrument in self.instruments.items():
            status['instruments'][inst_id] = {
                'type': instrument.instrument_type,
                'brand': instrument.brand,
                'model': instrument.model,
                'connected': instrument.is_connected(),
                'address': instrument.resource_id
            }
        
        return status
    
    def print_status(self):
        """Print a formatted status report of all instruments."""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("BENCH STATUS")
        print("="*70)
        print(f"Total Instruments: {status['total_instruments']}")
        print(f"Connected: {status['connected']}")
        print(f"Disconnected: {status['disconnected']}")
        print("-"*70)
        
        for inst_id, inst_info in status['instruments'].items():
            status_str = "✓ CONNECTED" if inst_info['connected'] else "✗ DISCONNECTED"
            print(f"{inst_id:15} | {inst_info['type']:8} | {inst_info['brand']:15} "
                  f"{inst_info['model']:15} | {status_str}")
        
        print("="*70 + "\n")
    
    def __enter__(self):
        """Context manager entry."""
        self.load_config()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - disconnect all instruments."""
        self.disconnect_all()
        return False
    
    def __str__(self):
        """String representation."""
        return f"Bench with {len(self.instruments)} instrument(s)"
    
    def __repr__(self):
        """Detailed representation."""
        return f"Bench(config_path='{self.config_path}', instruments={len(self.instruments)})"


# Convenience function to create instrument-specific subclasses
def create_instrument_class(class_name: str, device_id_command: str = "*IDN?"):
    """
    Factory to create instrument-specific subclasses.
    
    Args:
        class_name: Name of the instrument class
        device_id_command: Command to get device ID
        
    Returns:
        New instrument class
    """
    def get_device_id(self) -> str:
        try:
            return self.query(device_id_command)
        except:
            return "ID not available"
    
    return type(
        class_name,
        (GenericInstrument,),
        {'get_device_id': get_device_id}
    )
