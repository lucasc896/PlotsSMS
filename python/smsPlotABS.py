import ROOT as rt
from array import *
from sms import *
from color import *

class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # obsLimits is a list of opbserved limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA, +2SIGMA, -2SIGMA]
    # Label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, obsLimits, expLimits, expLimitsTwo, energy, lumi, preliminary, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, expLimitsTwo, energy, lumi, preliminary, label)
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, obsLimits, expLimits, expLimitsTwo, energy, lumi, preliminary, label):
        # which SMS?
        self.model = sms(modelname)
        self.OBS = obsLimits
        self.EXP = expLimits
        self.EXPTWO = expLimitsTwo
        print self.EXP
        print self.EXPTWO
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        self.label = label
        # create the reference empty histo
        self.deltaM = True
        self.emptyhisto = self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self):
        #xmin = self.model.Xmin
        #xmax = self.model.Xmax
        #ymin = self.model.Ymin if self.deltaM else self.model.Xmin - self.model.Ymin
        #ymax = self.model.Ymax if self.deltaM else self.model.Xmax - self.model.Ymin
        #self.emptyHisto = rt.TH2D("emptyHisto", "", 1, xmin, xmax, 1, ymin, ymax)
        self.emptyHisto = rt.TH2D("emptyHisto", "", 1, self.model.Xmin, self.model.Xmax, 1, self.model.Ymin, self.model.Ymax)

    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)        

        self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)

        self.c.SetRightMargin(0.19)
        self.c.SetTopMargin(0.08)
        self.c.SetLeftMargin(0.14)
        self.c.SetBottomMargin(0.14)

        # set x axis
        self.emptyHisto.GetXaxis().SetLabelFont(42)
        self.emptyHisto.GetXaxis().SetLabelSize(0.04)
        self.emptyHisto.GetXaxis().SetTitleFont(42)
        self.emptyHisto.GetXaxis().SetTitleSize(0.05)
        self.emptyHisto.GetXaxis().SetTitleOffset(1.2)
        self.emptyHisto.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)

        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.04)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        self.emptyHisto.GetYaxis().SetTitleOffset(1.35)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)
                
    def DrawText(self):
        #redraw axes
        self.c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.model.Xmin, self.model.Ymax)
        graphWhite.SetPoint(1,self.model.Xmax, self.model.Ymax)
        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.68)
        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.68)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
        
        # CMS LABEL
        str = "CMS %s, %s fb^{-1}, #sqrt{s} = %s TeV" %(self.preliminary, self.lumi, self.energy)
        if self.label is not None : str += ", %s" %(self.label)
        textCMS = rt.TLatex(0.16,0.98,str)
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(42)
        textCMS.SetTextSize(0.038)
        textCMS.Draw()
        self.c.textCMS = textCMS
        # MODEL LABEL
        textModelLabel= rt.TLatex(0.16,0.90,"%s  NLO+NLL exclusion" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.040)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        # NLO NLL XSEC
        textNLONLL= rt.TLatex(0.16,0.32,"NLO-NLL exclusion")
        textNLONLL.SetNDC()
        textNLONLL.SetTextAlign(13)
        textNLONLL.SetTextFont(42)
        textNLONLL.SetTextSize(0.040)
        textNLONLL.Draw()
        #self.c.textNLONLL = textNLONLL

    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        
    def DrawLegend(self):
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        if self.OBS is not None : LObsP.SetLineColor(color(self.OBS['colorLine']))
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10)

        LObs = rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        if self.OBS is not None : LObs.SetLineColor(color(self.OBS['colorLine']))
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)

        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        if self.OBS is not None : LObsM.SetLineColor(color(self.OBS['colorLine']))
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10)

        textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(2)
        LExpP.SetLineWidth(2)  
        LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10)

        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(2)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(2)
        LExpM.SetLineWidth(2)  
        LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10)
        LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10)

        textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp

        LExpP2 = rt.TGraph(2)
        LExpP2.SetName("LExpP2")
        LExpP2.SetTitle("LExpP2")
        LExpP2.SetLineColor(color(self.EXP['colorLine']))
        LExpP2.SetLineStyle(3)
        LExpP2.SetLineWidth(2)  
        LExpP2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.50*yRange/100*10)
        LExpP2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.50*yRange/100*10)

        LExp2 = rt.TGraph(2)
        LExp2.SetName("LExp2")
        LExp2.SetTitle("LExp2")
        LExp2.SetLineColor(color(self.EXP['colorLine']))
        LExp2.SetLineStyle(2)
        LExp2.SetLineWidth(4)
        LExp2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.65*yRange/100*10)
        LExp2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.65*yRange/100*10)

        LExpM2 = rt.TGraph(2)
        LExpM2.SetName("LExpM2")
        LExpM2.SetTitle("LExpM2")
        LExpM2.SetLineColor(color(self.EXP['colorLine']))
        LExpM2.SetLineStyle(3)
        LExpM2.SetLineWidth(2)  
        LExpM2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.80*yRange/100*10)
        LExpM2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.80*yRange/100*10)

        textExp2 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.80*yRange/100*10, "Expected #pm 2 #sigma_{experiment}")
        textExp2.SetTextFont(42)
        textExp2.SetTextSize(0.040)
        textExp2.Draw()
        self.c.textExp2 = textExp2

        if "T2bw" in self.model.modelname:
            xval = self.model.xsplitval
            textXVal = rt.TLatex(80, -55, "m_{#tilde{#chi^{#pm}_{1}}} = %sm_{#tilde{t}} + %sm_{#tilde{#chi^{0}_{1}}}" % (str(xval), str(1-xval)))
            textXVal.SetTextFont(42)
            textXVal.SetTextSize(0.035)
            textXVal.Draw()
            self.c.textXVal =textXVal

        LObsP.Draw("LSAME")
        LObs.Draw("LSAME")
        LObsM.Draw("LSAME")

        LExpM.Draw("LSAME") 
        LExp.Draw("LSAME")
        LExpP.Draw("LSAME")

        LExpP2.Draw("LSAME")
        LExp2.Draw("LSAME")
        LExpM2.Draw("LSAME")
        
        self.c.LObsP = LObsP
        self.c.LObs = LObs
        self.c.LObsM = LObsM

        self.c.LExpP = LExpP
        self.c.LExp = LExp
        self.c.LExpM = LExpM

        self.c.LExpP2 = LExpP2
        self.c.LExp2 = LExp2
        self.c.LExpM2 = LExpM2

    def DrawDiagonal(self):
        diagonal = rt.TGraph(3, self.model.diagX, self.model.diagY)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.diagonal = diagonal
        
    def DrawLines(self):

        if self.OBS is not None : 
            # observed
            self.OBS['nominal'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['nominal'].SetLineStyle(1)
            self.OBS['nominal'].SetLineWidth(4)
            # observed + 1sigma
            self.OBS['plus'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['plus'].SetLineStyle(1)
            self.OBS['plus'].SetLineWidth(2)
            # observed - 1sigma
            self.OBS['minus'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['minus'].SetLineStyle(1)
            self.OBS['minus'].SetLineWidth(2)

        # expected + 1sigma
        self.EXP['plus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['plus'].SetLineStyle(2)
        self.EXP['plus'].SetLineWidth(2)                
        # expected + 2sigma
        self.EXP['plus2'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['plus2'].SetLineStyle(3)
        self.EXP['plus2'].SetLineWidth(2)                
        # expected
        self.EXP['nominal'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['nominal'].SetLineStyle(2)
        self.EXP['nominal'].SetLineWidth(4)        
        # expected - 1sigma
        self.EXP['minus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['minus'].SetLineStyle(2)
        self.EXP['minus'].SetLineWidth(2)                        
        # expected - 2sigma
        self.EXP['minus2'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['minus2'].SetLineStyle(3)
        self.EXP['minus2'].SetLineWidth(2)
        # DRAW LINES
        self.EXP['nominal'].Draw("LSAME")
        self.EXP['plus'].Draw("LSAME")
        self.EXP['plus2'].Draw("LSAME")
        self.EXP['minus'].Draw("LSAME")
        self.EXP['minus2'].Draw("LSAME")



        if self.EXPTWO['plus']:
            # expected + 1sigma
            self.EXPTWO['plus'].SetLineColor(color(self.EXPTWO['colorLine']))
            self.EXPTWO['plus'].SetLineStyle(2)
            self.EXPTWO['plus'].SetLineWidth(2)                
        if self.EXPTWO['plus2']:
            # expected + 2sigma
            self.EXPTWO['plus2'].SetLineColor(color(self.EXPTWO['colorLine']))
            self.EXPTWO['plus2'].SetLineStyle(3)
            self.EXPTWO['plus2'].SetLineWidth(2)                
        if self.EXPTWO['nominal']:
            # expected
            self.EXPTWO['nominal'].SetLineColor(color(self.EXPTWO['colorLine']))
            self.EXPTWO['nominal'].SetLineStyle(2)
            self.EXPTWO['nominal'].SetLineWidth(4)        
        if self.EXPTWO['minus']:
            # expected - 1sigma
            self.EXPTWO['minus'].SetLineColor(color(self.EXPTWO['colorLine']))
            self.EXPTWO['minus'].SetLineStyle(2)
            self.EXPTWO['minus'].SetLineWidth(2)                        
        if self.EXPTWO['minus2']:
            # expected - 2sigma
            self.EXPTWO['minus2'].SetLineColor(color(self.EXPTWO['colorLine']))
            self.EXPTWO['minus2'].SetLineStyle(3)
            self.EXPTWO['minus2'].SetLineWidth(2)
        # DRAW LINES
        if self.EXPTWO['nominal']: self.EXPTWO['nominal'].Draw("LSAME")
        if self.EXPTWO['plus']: self.EXPTWO['plus'].Draw("LSAME")
        if self.EXPTWO['plus2']: self.EXPTWO['plus2'].Draw("LSAME")
        if self.EXPTWO['minus']: self.EXPTWO['minus'].Draw("LSAME")
        if self.EXPTWO['minus2']: self.EXPTWO['minus2'].Draw("LSAME")



        if self.OBS is not None : 
            self.OBS['nominal'].Draw("LSAME")
            self.OBS['plus'].Draw("LSAME")
            self.OBS['minus'].Draw("LSAME")

#        c1 = rt.TCanvas()
#        print self.EXP
#        tmp = self.EXP["nominal"]
#        rt.SetOwnership(tmp,True)
#        tmp.Draw("SAME")
#        raw_input("")
