from collections import OrderedDict as odict
import ROOT as r

class config(object):

    def style(self,LineColor,LineStyle,LineWidth,FillColor):
        return odict([
                ("LineColor",LineColor),
                ("LineStyle",LineStyle),
                ("LineWidth",LineWidth),
                ("FillColor",FillColor),])
    
    def __init__(self) :
        self.model_ = None
        self.dir = None
        self.prelim_ = "Preliminary"
        self.label_ = "#alpha_{T}"
        self.lumi_ = 18.5
        self.xs_ = None
        self.files_ = None
        self.histos_ = None
        self.xsec_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
                ("OBS",self.style(r.kBlack,1,4,None)),
                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
                ("EXP",self.style(r.kRed,7,4,None)),
                ("EXP_SIGMA1",self.style(r.kBlack,7,2,None)),
                ("EXP_SIGMA2",self.style(r.kBlack,5,2,None)),
                ])
        self.cont_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
                ("OBS",self.style(r.kBlack,1,4,r.kBlue)),
                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
                ("EXP",self.style(r.kRed,7,4,None)),
                ("EXP_SIGMA1",self.style(r.kBlack,7,2,None)),
                ("EXP_SIGMA2",self.style(r.kBlack,5,2,None)),
                ])
        self.band_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
                ("OBS",self.style(r.kBlack,1,4,r.kBlue)),
                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
                ("EXP",self.style(r.kBlack,2,4,None)),
                ("EXP_SIGMA1",self.style(None,None,None,r.kGreen)),
                ("EXP_SIGMA2",self.style(None,None,None,r.kYellow)),
                ])

    def __str__(self) :
        print "model",self.model_
#        print "",self.dir = None
#        self.prelim_ = "Preliminary"
#        self.label_ = "#alpha_{T}"
#        self.lumi_ = 18.5
#        self.xs_ = None
#        self.files_ = None
#        self.histos_ = None
#        self.xsec_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
#                ("OBS",self.style(r.kBlack,1,4,None)),
#                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
#                ("EXP",self.style(r.kRed,7,4,None)),
#                ("EXP_SIGMA1",self.style(r.kBlack,7,2,None)),
#                ("EXP_SIGMA2",self.style(r.kBlack,5,2,None)),
#                ])
#        self.cont_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
#                ("OBS",self.style(r.kBlack,1,4,r.kBlue)),
#                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
#                ("EXP",self.style(r.kRed,7,4,None)),
#                ("EXP_SIGMA1",self.style(r.kBlack,7,2,None)),
#                ("EXP_SIGMA2",self.style(r.kBlack,5,2,None)),
#                ])
#        self.band_ = odict([ # LineColor,LineStyle,LineWidth,FillColor
#                ("OBS",self.style(r.kBlack,1,4,r.kBlue)),
#                ("OBS_SIGMA",self.style(r.kBlack,1,2,None)),
#                ("EXP",self.style(r.kBlack,2,4,None)),
#                ("EXP_SIGMA1",self.style(None,None,None,r.kGreen)),
#                ("EXP_SIGMA2",self.style(None,None,None,r.kYellow)),
#                ])

    def init(self):
        self.files_ = odict([
                ("OBS",None),
                ("EXP",None),
                ])
        self.histos_ = odict([
                ("OBS",self.model_+"_UpperLimit"),
                ("EXP",self.model_+"_ExpectedUpperLimit"),
                ("EXP_P1",self.model_+"_ExpectedUpperLimit_p1_Sigma"),
                ("EXP_P2",self.model_+"_ExpectedUpperLimit_p2_Sigma"),
                ("EXP_M1",self.model_+"_ExpectedUpperLimit_m1_Sigma"),
                ("EXP_M2",self.model_+"_ExpectedUpperLimit_m2_Sigma"),
                ])
