from abc import ABC, abstractmethod

class Oscilloscope_Factory:

    def create_Oscilloscope(oscilloscope_id):
        if oscilloscope_id == "gw_instek_gds_806s":
            return Owon()
        else:
            raise ValueError(f"Unknown instrument type: {oscilloscope_id}")