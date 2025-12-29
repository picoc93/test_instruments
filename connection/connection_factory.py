from abc import ABC, abstractmethod

class Connection_Factory(ABC):
    @staticmethod
    def create_settings(conn_type: str, raw_settings: dict) -> ConnectionSettings:
        if conn_type == "serial":
            return ASRL(**raw_settings)
        elif conn_type == "gpib":
            return GPIBSettings(**raw_settings)
        elif conn_type == "tcpip":
            return TCPIPSettings(**raw_settings)
        return ConnectionSettings(**raw_settings)