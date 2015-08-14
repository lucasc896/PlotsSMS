#!/usr/bin/env python
import ROOT as r
import xsec as xs
import smoother as smthr
from collections import OrderedDict

r.gROOT.SetBatch(0)

class limit(object):
    """limit container"""
    def __init__(self, limitmap = None, model = "", label = "", var = ""):
        self._map = limitmap.Clone()
        self._map.SetTitle("UpperLimit")
        self._theoryVar = var
        self._curve = None
        # self._map.Smooth(1, "k3a")
        self._nbins = self._map.GetNbinsX()*self._map.GetNbinsX()+1
        self._xbins = range(1, self._map.GetNbinsX()+1)
        self._ybins = range(1, self._map.GetNbinsY()+1)
        self._model = model
        self._label = label
        self.createSimpleMap()
        # self.curveFromMap() # do the heavy lifting

    def curveFromMap(self):
        """calculate the actual limit curve from the 2d map"""
        
        curve = r.TGraph()

        points = OrderedDict()

        self._ratioMap.Smooth(1, "k3a")
        # self._ratioMap.Smooth(1, "k3a")
        # self._ratioMap.Smooth(1, "k3a")
        self._ratioMap.SetContour(1)
        self._ratioMap.SetContourLevel(0, 1.)
        # self._ratioMap.SetContourLevel(1, 2.)
        # self._ratioMap.SetContourLevel(2, 1.)
        # self._ratioMap.SetContourLevel(3, 1.1)
        # self._ratioMap.SetMaximum(1.0001)
        self._ratioMap.Draw("cont list")
        r.gPad.Update()
        contours = r.gROOT.GetListOfSpecials().FindObject("contours")
        mylist = contours.At(0)
        try: 
            curve = mylist.First().Clone()
        except ReferenceError:
            return r.TGraph()
        curve.SetName(self._label)
        # todel = []
        for n in range(1, curve.GetN()+1):
            x = r.Double(0.)
            y = r.Double(0.)
            curve.GetPoint(n, x, y)
            # if x <= 0.: todel.append(n)
            # if x > 700.: todel.append(n)
            # if x < 225.: todel.append(n)
            # if y > 210.: todel.append(n)
            # if x - y < 200: todel.append(n)

        # find all the edges
        # n = 1
        # for xbin in self._xbins:
        #     lastVal = 0.
        #     mstop = self._simpleMap.GetXaxis().GetBinCenter(xbin)
        #     thisStrip = []
        #     for ybin in self._ybins:
        #         val = self._simpleMap.GetBinContent(xbin, ybin)
        #         mlsp = self._simpleMap.GetYaxis().GetBinCenter(ybin)
                    
        #         if mstop < mlsp:
        #             break

        #         if lastVal in [0., -1.] and val == 1.:
        #             # curve.SetPoint(n, mstop, mlsp)
        #             thisStrip.append(mlsp)
        #             n += 1
        #         elif lastVal == 1. and val in [0., -1.]:
        #             # curve.SetPoint(n, lastmstop, lastmlsp)
        #             thisStrip.append(lastmlsp)
        #             # print mstop, lastmlsp
        #             n+=1

        #         lastVal = val
        #         lastmstop = mstop
        #         lastmlsp = mlsp
            
        #     if thisStrip:
        #         points[mstop] = thisStrip

        # # plot in default order
        # # n = 1
        # # for mstop in points:
        # #     for mlsp in points[mstop]:
        # #         curve.SetPoint(n, mstop, mlsp)
        # #         n+=1

        # # plot only top and bottom mlsp points per mstop strip
        # n = 0
        # for mstop in points:
        #     # print points[mstop]
        #     if len(points[mstop]) == 2 and points[mstop][0] == points[mstop][1]:
        #         # print mstop
        #         # assume that if a single point is excluded in an mstop
        #         # strip, then it's likely at low mlsp, so skip it here
        #         # when drawing the top row
        #         continue
        #     curve.SetPoint(n, mstop, points[mstop][-1])
        #     # print n, mstop, points[mstop][-1]
        #     n+=1
        # for mstop in reversed(points.keys()):
        #     curve.SetPoint(n, mstop, points[mstop][0])
        #     # print n, mstop, points[mstop][0]
        #     n+=1

        # # close the loop
        # curve.SetPoint(n, points.keys()[0], points[points.keys()[0]][-1])
        self._curve = curve

    def createSimpleMap(self):

        self._simpleMap = self._map.Clone()
        self._simpleMap.SetTitle("Simple")
        self._ratioMap = self._map.Clone()
        self._ratioMap.SetTitle("Ratio")
        
        for xbin in self._xbins:
            mstop = self._map.GetXaxis().GetBinCenter(xbin)
            for ybin in self._ybins:
                mlsp = self._map.GetYaxis().GetBinCenter(ybin)
                val = self._map.GetBinContent(xbin, ybin)
                # if mstop == 200. and mlsp == 100.: print val
                if mstop < mlsp or mstop > 400 or mlsp > 400. or mstop-mlsp>100: # T2cc
                # if mstop < mlsp or mstop > 801. or val <= 0. or (mstop < 174. and self._model == "T2tt"):
                # if mstop < mlsp or mstop > 500 or mlsp > 300. or (val <= 0 and mstop-mlsp < 25.): # T2bw_0p25
                # if mstop < mlsp or mstop > 800 or mlsp > 300. or (val <= 0 and mstop-mlsp < 25.): # T2bw_0p75
                    # self._ratioMap.SetBinContent(xbin, ybin, )
                    self._simpleMap.SetBinContent(xbin, ybin, 0.)
                    self._ratioMap.SetBinContent(xbin, ybin, 100.)
                    continue
                # if self._model == "T2tt" and self._label == "UpperLimit" and mstop < 200.:
                #     self._simpleMap.SetBinContent(xbin, ybin, 0.)
                #     self._ratioMap.SetBinContent(xbin, ybin, 100.)
                #     continue
                thisxs = xs.stop(mstop)[0]
                if self._theoryVar:
                    if self._theoryVar == "p":
                        thisxs *= (100. + xs.stop(mstop)[1])/100.
                    elif self._theoryVar == "m":
                        thisxs *= (100. - xs.stop(mstop)[1])/100.
                ratio = float(val/thisxs)
                if self._model == "T2bw_0p75" and mstop == 225. and mlsp == 50.:
                    ratio = 0.5
                # if self._model == "T2bw_0p25" and mstop == 100. and mlsp == 25.:
                #     ratio = 100.
                # if self._model == "T2bw_0p25" and mstop == 100. and mlsp == 0.:
                #     ratio = 0.5
                self._simpleMap.SetBinContent(xbin, ybin, 1. if ratio < 1. else -1.)
                self._ratioMap.SetBinContent(xbin, ybin, ratio)


def main():
    model = ["T2cc", "T2tt", "T2bw_0p75", "T2bw_0p25"][0]
    limname = ["ExpectedUpperLimit",
                "ExpectedUpperLimit_p1_Sigma", "ExpectedUpperLimit_p2_Sigma",
                "ExpectedUpperLimit_m1_Sigma", "ExpectedUpperLimit_m2_Sigma",
                "UpperLimit", "UpperLimit_p1_Sigma", "UpperLimit_m1_Sigma"]
    f = r.TFile.Open("/Users/chrislucas/SUSY/Parked/Signal/PlotsSMS/config/SUS14006/latest_chris_contours/%s/%s_obs.root" % (model, model))
    fo = r.TFile.Open("%s_newContCurves.root" % model, "UPDATE")

    rebin = False
    if model == "T2bw_0p75":
        rebin = False
    if model == "T2bw_0p25":
        rebin = False
    if model == "T2tt":
        rebin = False

    canv = r.TCanvas()
    canv.Divide(2)

    var = ""
    for lname in limname:
        if "Expected" not in lname:
            if "Sigma" in lname:
                if "p1" in lname: var = "p"
                if "m1" in lname: var = "m"
                tmpname = lname.split("_")[0]
            else:
                tmpname = lname
        else:
            tmpname = lname
        limit_map = f.Get("%s_%s" % (model, tmpname))
        if rebin:
            limit_map = smthr.rebin(limit_map, "NE")

        myLimit_nominal = limit(limit_map, model, lname, var)

        canv.cd(1)
        thisratio = myLimit_nominal._ratioMap.Clone()
        thisratio.GetXaxis().SetRangeUser(0., 800.)
        thisratio.GetYaxis().SetRangeUser(0., 350.)
        thisratio.GetZaxis().SetRangeUser(0.7, 1.1)
        thisratio.Draw("colztext")
        
        canv.cd(2)
        myLimit_nominal.curveFromMap()
        myLimit_nominal._ratioMap.GetXaxis().SetRangeUser(0., 800.)
        myLimit_nominal._ratioMap.GetYaxis().SetRangeUser(0., 350.)
        myLimit_nominal._ratioMap.Draw("colz")
        myLimit_nominal._curve.Draw("lsame")
        
        canv.Print("limit_%s_%s.pdf" % (model, lname))

        myLimit_nominal._curve.Write()
        limit_map.Write()

        del myLimit_nominal

    fo.Close()


if __name__ == "__main__":
    main()