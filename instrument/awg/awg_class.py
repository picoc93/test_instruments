from abc import ABC, abstractmethod

class AWG(Instrument):
    def connect(self): return f"AWG {self.resource_id} connected."