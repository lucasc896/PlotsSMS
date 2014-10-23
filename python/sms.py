from array import *

class sms():

#    def __str__(self):
#        print self.modelname

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        elif modelname.find("T1bbbb") != -1: self.T1bbbb()
        elif modelname.find("T2cc") != -1: self.T2cc()
        elif modelname.find("T2degen") != -1: self.T2degen()
        else : print "unknown model!",modelname

    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 1400
        self.Ymin = 0
        self.Ymax = 800
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 400
        self.Xmax = 1600
        self.Ymin = 0
        self.Ymax = 1200
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])

    def T2cc(self):
        # model name
        self.modelname = "T2cc"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t},  #tilde{t} #rightarrow c #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 100.-25./2.
        self.Xmax = 350.+25./2.
        self.Ymin = 0.
        self.Ymax = 530.
        # produce sparticle
        self.sParticle = "m_{ #tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0.#80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])

    def T2degen(self):
        # model name
        self.modelname = "T2degen"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t},  #tilde{t} #rightarrow bf#bar{f}#tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 100.-25./2.
        self.Xmax = 350.+25./2.
        self.Ymin = 0.
        self.Ymax = 530.
        # produce sparticle
        self.sParticle = "m_{ #tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0.#80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])
