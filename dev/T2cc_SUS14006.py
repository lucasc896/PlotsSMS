import config

class T2cc_SUS14006(config):

    def __init__(self) :
        self.model_ = "T2cc"
        self.xs_ = "input/stop_sbottom"
        self.files_ = odict([
                ("OBS","input/SUS14006/T2cc.root"),
                ("EXP","input/SUS14006/T2cc.root"),
                ])
        self.init()

        
