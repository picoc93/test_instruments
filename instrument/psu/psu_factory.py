from abc import ABC, abstractmethod

class PSU_Factory:

    def create_PSU(psu_id):
        if psu_id == "owon_spm3051":
            return Owon()
        else:
            raise ValueError(f"Unknown instrument type: {psu_id}")