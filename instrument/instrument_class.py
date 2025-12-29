from abc import ABC, abstractmethod

class Instrument(ABC):
    def __init__(self, resource_id):
        self.resource_id = resource_id

    @abstractmethod
    def connect(self): pass