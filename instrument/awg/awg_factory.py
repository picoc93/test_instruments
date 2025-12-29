class AWG_Factory:

    def create_AWG(awg_id):
        if awg_id == "feeltech_fy3224s":
            return Owon()
        else:
            raise ValueError(f"Unknown instrument type: {awg_id}")