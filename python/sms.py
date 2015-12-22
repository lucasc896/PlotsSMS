from array import *

class sms():

#    def __str__(self):
#        print self.modelname

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        elif modelname.find("T1bbbb") != -1: self.T1bbbb()
        elif modelname.find("T2cc") != -1: self.T2cc()
        elif modelname.find("T2degen") != -1: self.T2degen()
        elif modelname.find("T2tt") != -1: self.T2tt()
        elif modelname.find("T2bw_0p75") != -1: self.T2bw_0p75()
        elif modelname.find("T2bw_0p25") != -1: self.T2bw_0p25()
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
        self.Xmin = 100.-25.#/2.
        self.Xmax = 350.+25.#/2.
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
        self.Xmin = 100.-25.#/2.
        self.Xmax = 350.+25.#/2.
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

    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t},  #tilde{t} #rightarrow t #tilde{#chi}^{0}_{1}";
        # scan range to plot
        # self.Xmin = 100.-25.#/2.
        self.Xmin = 200.
        self.Xmax = 712.5+25.#/2.
        self.Ymin = 0.
        self.Ymax = 450.
        # self.Ymax = 300.
        # produce sparticle
        self.sParticle = "m_{ #tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0.#80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])

    def T2bw_0p75(self):
        # model name
        self.modelname = "T2bw_0p75"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t},  #tilde{t} #rightarrow b #tilde{#chi}^{#pm}_{1}";
        # scan range to plot
        # self.Xmin = 100.-25.#/2.
        # self.Xmax = 800.+25.#/2.
        self.Xmin = 100.
        self.Xmax = 750.
        self.Ymin = 0.
        self.Ymax = 450.
        # produce sparticle
        self.sParticle = "m_{ #tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0.#80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])
        self.xsplitval = 0.75
        

    def T2bw_0p25(self):
        # model name
        self.modelname = "T2bw_0p25"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t},  #tilde{t} #rightarrow b #tilde{#chi}^{#pm}_{1}";
        # scan range to plot
        # self.Xmin = 100.-25.#/2.
        self.Xmin = 100.
        # self.Xmax = 800.+25.#/2.
        self.Xmax = 550.
        self.Ymin = 0.
        # self.Ymax = 800.
        self.Ymax = 450.
        # produce sparticle
        self.sParticle = "m_{ #tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 0.#80
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])
        self.xsplitval = 0.25