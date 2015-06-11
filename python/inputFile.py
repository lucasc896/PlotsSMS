import sys
import ROOT as rt

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        for histo in self.HISTOGRAM.values() : histo.GetZaxis().SetTitle("")
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")
        self.LABEL = self.findATTRIBUTE(fileName, "LABEL")

    def dm(self,input):
        output = rt.TH2F(input.GetName()+"_Clone",
                         input.GetTitle()+"_Clone",
                         input.GetXaxis().GetNbins(),
                         input.GetXaxis().GetXmin(),
                         input.GetXaxis().GetXmax(),
                         input.GetYaxis().GetNbins(),
                         input.GetYaxis().GetXmin(),
                         input.GetYaxis().GetXmax())
        output.GetYaxis().SetTitle("#Delta M (GeV)")
        for xbin in range(1,input.GetXaxis().GetNbins()+1):
            for ybin in range(1,input.GetYaxis().GetNbins()+1):
                xval = input.GetXaxis().GetBinCenter(xbin)
                yval = input.GetYaxis().GetBinCenter(ybin)
                if yval > xval : continue
                bin = output.GetYaxis().FindBin( xval - yval )
                print xbin,ybin,bin,input.GetBinContent(xbin,ybin)
                output.SetBinContent(xbin,bin,input.GetBinContent(xbin,ybin))
                output.SetBinError(xbin,bin,input.GetBinError(xbin,ybin))
        return output

    def interpolate(self,input):
        graph = rt.TGraph2D(input)
        xmin = 0.#self.Xmin#input.GetXaxis().GetXmin()
        xmax = 400.#self.Xmax#input.GetXaxis().GetXmax()
        ymin = 0.#self.Ymin#input.GetYaxis().GetXmin()
        ymax = 400.#self.Ymax#input.GetYaxis().GetXmax()
        print xmin,xmax,ymin,ymax
        output = rt.TH2F(input.GetName()+"_Clone",
                         input.GetTitle()+"_Clone",
                         int(xmax-xmin),xmin,xmax,
                         int(ymax-ymin),ymin,ymax)
        output.GetYaxis().SetTitle("#Delta M (GeV)")
        for xbin in range(1,output.GetXaxis().GetNbins()+1):
            for ybin in range(1,output.GetYaxis().GetNbins()+1):
                val = graph.Interpolate(xbin,ybin)
                output.SetBinContent(xbin,ybin,val)
        return output

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return tmpLINE[1]

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'histogram': rootFileIn.Get(tmpLINE[2])}
            #return {'histogram': self.dm(rootFileIn.Get(tmpLINE[2]))}
            #return {'histogram': self.interpolate(self.dm(rootFileIn.Get(tmpLINE[2])))}
            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'plus2': rootFileIn.Get(tmpLINE[4]),
                    'minus': rootFileIn.Get(tmpLINE[5]),
                    'minus2': rootFileIn.Get(tmpLINE[6]),
                    'colorLine': tmpLINE[7],
                    'colorArea': tmpLINE[8],
                    'colorArea2': tmpLINE[9],
                    }

    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'minus': rootFileIn.Get(tmpLINE[4]),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}
        return None
