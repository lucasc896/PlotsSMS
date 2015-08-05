#!/usr/bin/env python
import ROOT as r
import xsec as xs
import smoother as smthr
from collections import OrderedDict

class limit(object):
    """limit container"""
    def __init__(self, limitmap = None, model = "", label = ""):
        self._map = limitmap.Clone()
        self._nbins = self._map.GetNbinsX()*self._map.GetNbinsX()+1
        self._xbins = range(1, self._map.GetNbinsX()+1)
        self._ybins = range(1, self._map.GetNbinsY()+1)
        self._model = model
        self._label = label
        self._curve = self.curveFromMap() # do the heavy lifting

    def curveFromMap(self):
        """calculate the actual limit curve from the 2d map"""
        
        self.createSimpleMap()
        curve = r.TGraph()

        points = OrderedDict()

        # find all the edges
        n = 1
        for xbin in self._xbins:
            lastVal = 0.
            mstop = self._simpleMap.GetXaxis().GetBinCenter(xbin)
            thisStrip = []
            for ybin in self._ybins:
                val = self._simpleMap.GetBinContent(xbin, ybin)
                mlsp = self._simpleMap.GetYaxis().GetBinCenter(ybin)
                    
                if mstop < mlsp:
                    break

                if lastVal in [0., -1.] and val == 1.:
                    # curve.SetPoint(n, mstop, mlsp)
                    thisStrip.append(mlsp)
                    n += 1
                elif lastVal == 1. and val in [0., -1.]:
                    # curve.SetPoint(n, lastmstop, lastmlsp)
                    thisStrip.append(lastmlsp)
                    # print mstop, lastmlsp
                    n+=1

                lastVal = val
                lastmstop = mstop
                lastmlsp = mlsp
            
            if thisStrip:
                points[mstop] = thisStrip

        # plot in default order
        # n = 1
        # for mstop in points:
        #     for mlsp in points[mstop]:
        #         curve.SetPoint(n, mstop, mlsp)
        #         n+=1

        # plot only top and bottom mlsp points per mstop strip
        n = 0
        for mstop in points:
            # print points[mstop]
            if len(points[mstop]) == 2 and points[mstop][0] == points[mstop][1]:
                # print mstop
                # assume that if a single point is excluded in an mstop
                # strip, then it's likely at low mlsp, so skip it here
                # when drawing the top row
                continue
            curve.SetPoint(n, mstop, points[mstop][-1])
            # print n, mstop, points[mstop][-1]
            n+=1
        for mstop in reversed(points.keys()):
            curve.SetPoint(n, mstop, points[mstop][0])
            # print n, mstop, points[mstop][0]
            n+=1

        # close the loop
        curve.SetPoint(n, points.keys()[0], points[points.keys()[0]][-1])

        return curve




    def createSimpleMap(self):

        self._simpleMap = self._map.Clone()
        
        for xbin in self._xbins:
            mstop = self._map.GetXaxis().GetBinCenter(xbin)
            for ybin in self._ybins:
                mlsp = self._map.GetYaxis().GetBinCenter(ybin)
                val = self._map.GetBinContent(xbin, ybin)
                if mstop < mlsp or mstop > 801. or val <= 0.:
                    # self._ratioMap.SetBinContent(xbin, ybin, )
                    self._simpleMap.SetBinContent(xbin, ybin, 0.)
                    continue
                ratio = float(val/xs.stop(mstop)[0])
                self._simpleMap.SetBinContent(xbin, ybin, 1. if ratio < 1. else -1.)



def main():
    model = ["T2tt", "T2bw_0p75", "T2bw_0p25"][0]
    f = r.TFile.Open("/Users/chrislucas/SUSY/SignalScans/effStudies/SignalSystematics/PlotsSMS/%s_test.root" % model)
    limit_map = f.Get("%s_ExpectedUpperLimit" % model)

    myLimit_nominal = limit(limit_map, "T2tt", "Expected - Central")

    canv = r.TCanvas()

    myLimit_nominal._map.Draw("colz")
    canv.Print("limitTmp.pdf(")

    myLimit_nominal._simpleMap.Draw("colz")
    canv.Print("limitTmp_simp.pdf(")

    myLimit_nominal._curve.Draw("lsame*")
    canv.Print("limitTmp_cont_%s.pdf(" % model)

    # for direc in ["NE", "NW", "SW", "SE"]:
    direc = "NE"
    for num in range(1, 4):
        limit_map = smthr.rebin(limit_map, direc)

        myLimit_smoothed = limit(limit_map, "T2tt", "Expected - Central")

        myLimit_smoothed._map.Draw("colz")
        myLimit_smoothed._map.SetTitle("Smoothed x%d - %s" % (num, direc))
        canv.Print("limitTmp.pdf")

        myLimit_smoothed._simpleMap.Draw("colz")
        myLimit_smoothed._simpleMap.SetTitle("Smoothed x%d - %s" % (num, direc))
        canv.Print("limitTmp_simp.pdf")

        myLimit_smoothed._curve.Draw("c")
        myLimit_smoothed._curve.SetTitle("Smoothed x%d - %s" % (num, direc))
        canv.Print("limitTmp_cont_%s.pdf" % model)

    canv.Clear()
    canv.Print("limitTmp.pdf)")
    canv.Print("limitTmp_simp.pdf)")
    canv.Print("limitTmp_cont_%s.pdf)" % model)    


if __name__ == "__main__":
    main()