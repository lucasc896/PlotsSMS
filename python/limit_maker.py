#!/usr/bin/env python
import ROOT as r
import math as ma
import xsec as xs
import smoother as smthr
from collections import OrderedDict

r.gROOT.SetBatch(0)

def point_white_list(model = '', x = None, y = None):
    return {'T2bw_0p25': lambda x,y: x-y >= 100. and x<=800.5,
            'T2bw_0p75': lambda x,y: x-y >= 100. and x<=800.5,
            'T2tt': lambda x,y: x-y >= 100. and x<=1000.5,
            'T2_4body': lambda x,y: x-y >= 0. and x-y <= 81. and x>99. and x<400.}[model]

class limit(object):
    """limit container"""
    def __init__(self, limitmap = None, model = "", label = "", var = ""):
        self._map = limitmap.Clone()
        self._map.SetTitle("UpperLimit")
        self._theoryVar = var
        self._curve = None
        self._curvetwo = None
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

        if self._model == "T2_4body":
            for xbin in range(1, self._ratioMap.GetNbinsX()+1):
                xmass = self._ratioMap.GetXaxis().GetBinCenter(xbin)
                if xmass != 100.: continue
                for ybin in range(1, self._ratioMap.GetNbinsY()+1):
                    ymass = self._ratioMap.GetYaxis().GetBinCenter(ybin)
                    if ymass < 82.:
                        self._ratioMap.SetBinContent(xbin, ybin, 0.95)


        self._postSmoothRatioMap = self._ratioMap.Clone()
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

        # total_curve = r.TGraph()
        print mylist.GetEntries()
        if mylist.GetEntries() > 1:
            self._curve = mylist.At(1)
            self._curvetwo = mylist.At(0)
            # for i in range(mylist.GetEntries()):
            #     curve = sumGraphs(mylist.At(i).Clone(), curve)
            # curve = sumGraphs(mylist.At(1).Clone(), mylist.At(0).Clone())
        else:
            self._curve = mylist.At(0).Clone()    

        # curve = mylist.At(0).Clone()

        self._curve.SetName(self._label)
        if self._curvetwo:
            self._curvetwo.SetName(self._label + "_two")

        # todel = []
        # for n in range(1, curve.GetN()+1):
        #     x = r.Double(0.)
        #     y = r.Double(0.)
        #     curve.GetPoint(n, x, y)
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
        # self._curve = curve

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

                if mstop < 100.:
                    self._simpleMap.SetBinContent(xbin, ybin, 0.)
                    self._ratioMap.SetBinContent(xbin, ybin, 5.)
                    continue

                if self._model == "T2_4body":
                    # made for deltaM plane
                    if mlsp > 80.:
                        self._simpleMap.SetBinContent(xbin, ybin, 0.)
                        self._ratioMap.SetBinContent(xbin, ybin, 5.)
                        continue




                # if mstop < mlsp or mstop > 400 or mlsp > 400. or mstop-mlsp>99: # T2cc
                # # if mstop < mlsp or mstop > 801. or val <= 0. or (mstop < 174. and self._model == "T2tt"):
                # # if mstop < mlsp or mstop > 500 or mlsp > 300. or (val <= 0 and mstop-mlsp < 25.): # T2bw_0p25
                # # if mstop < mlsp or mstop > 800 or mlsp > 300. or (val <= 0 and mstop-mlsp < 25.): # T2bw_0p75
                #     # self._ratioMap.SetBinContent(xbin, ybin, )
                #     self._simpleMap.SetBinContent(xbin, ybin, 0.)
                #     self._ratioMap.SetBinContent(xbin, ybin, 0.)
                #     continue
                if self._model == "T2tt" and self._label == "UpperLimit" and mstop < 174.:
                    self._simpleMap.SetBinContent(xbin, ybin, 0.)
                    self._ratioMap.SetBinContent(xbin, ybin, 100.)
                    continue
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
                if self._model == "T2tt" and mstop == 250. and mlsp == 0. and self._label == "UpperLimit_m1_Sigma":
                    ratio = 0.5
                # if self._model == "T2tt" and mstop < 250. and "ExpectedUpperLimit_p" in self._label:
                #     ratio = 100.

                # changes made from validation plots
                if self._model == "T2tt":
                    if mstop == 225. and mlsp == 50. and "Expected" not in self._label:
                        ratio = float(7.9/thisxs)
                    if mstop == 200. and mlsp == 25. and "Expected" not in self._label:
                        ratio = float(7.5/thisxs)

                self._simpleMap.SetBinContent(xbin, ybin, 1. if ratio < 1. else -1.)
                self._ratioMap.SetBinContent(xbin, ybin, ratio)

def deltaM(h2):

    minVal = 100.;
    maxVal = 0.;

    # get the splitting range
    for iY in range(1, 1+h2.GetNbinsY()):
        for iX in range(1, 1+h2.GetNbinsX()):
            if h2.GetBinContent(iX, iY) > 0.:
                val = h2.GetXaxis().GetBinCenter(iX) - h2.GetYaxis().GetBinCenter(iY)
                if val>maxVal:
                    maxVal=val
                if val<minVal:
                    minVal=val

    nbins = int((int(maxVal)+10. - int(minVal))/h2.GetYaxis().GetBinWidth(5))

    h2_dM = r.TH2D(h2.GetName(), h2.GetTitle(),
                    h2.GetNbinsX(), h2.GetXaxis().GetXmin(), h2.GetXaxis().GetXmax(),
                    # nbins, int(minVal), int(maxVal)+10.)
                    nbins+2, 0., int(maxVal)+10.)
    print "delta mass bin hack!!!!"

    for iY in range(1, 1+h2.GetNbinsY()):
        for iX in range(1, 1+h2.GetNbinsX()):
            if h2.GetBinContent(iX, iY) > 0.:
                content = h2.GetBinContent(iX, iY)
                ybinVal = h2.GetXaxis().GetBinCenter(iX) - h2.GetYaxis().GetBinCenter(iY)
                ybin = h2.GetYaxis().FindBin(ybinVal)
                h2_dM.Fill(int(h2.GetXaxis().GetBinCenter(iX)), int(ybinVal), content)

    h2_dM.GetXaxis().SetTitle("mStop (GeV)")
    h2_dM.GetYaxis().SetTitle("deltaM (GeV)")

    return h2_dM

def deltaM_curve(curve = None):
    out = r.TGraph()

    for i in range(curve.GetN()+1):
        x = r.Double(0.)
        y = r.Double(0.)
        curve.GetPoint(i, x, y)
        out.SetPoint(i, x, x-y)
    return out

def main():
    model = ["T2cc", "T2_4body", "T2tt", "T2bw_0p75", "T2bw_0p25"][1]
    limname = ["ExpectedUpperLimit",
                "ExpectedUpperLimit_p1_Sigma", "ExpectedUpperLimit_p2_Sigma",
                "ExpectedUpperLimit_m1_Sigma", "ExpectedUpperLimit_m2_Sigma",
                "UpperLimit", "UpperLimit_p1_Sigma", "UpperLimit_m1_Sigma"][:-2]
    # f = r.TFile.Open("/Users/chrislucas/SUSY/Parked/Signal/PlotsSMS/config/SUS14006/latest_chris_contours/%s/%s_newContCurves.root" % (model, model))
    # fobs = r.TFile.Open("/Users/chrislucas/Desktop/lazy_stats/obs/CLs_frequentist_T2tt_2012dev_1b_ge4j_0b_ge4j_1b_le3j_0b_le3j_xsLimit.root")
    # fexp = r.TFile.Open("/Users/chrislucas/Desktop/lazy_stats/exp/CLs_frequentist_T2tt_2012dev_1b_ge4j_0b_ge4j_1b_le3j_0b_le3j_xsLimit.root")
    f = r.TFile.Open("/Users/chrislucas/SUSY/Parked/Signal/PlotsSMS/config/SUS14006/chris/%s/%s_obs.root" % (model, model))
    fo = r.TFile.Open("%s_newContCurves.root" % model, "UPDATE")

    print f

    rebin = False
    if model == "T2bw_0p75":
        rebin = False
    if model == "T2bw_0p25":
        rebin = False
    if model == "T2tt":
        rebin = False

    canv = r.TCanvas("c1", "c1",1500, 700)
    canv.Divide(2)

    var = ""
    for lname in limname:
        print lname
        if "Expected" not in lname:
            if "Sigma" in lname:
                if "p1" in lname: var = "p"
                if "m1" in lname: var = "m"
                tmpname = lname.split("_")[0]
            else:
                tmpname = lname
        else:
            tmpname = lname

        # only use this for T2tt
        # if "Expected" not in lname:
        #     limit_map = fobs.Get("%s_%s" % (model, tmpname))
        # else:
        #     limit_map = fexp.Get("%s_%s" % (model, tmpname))
        limit_map = f.Get("%s_%s" % (model, tmpname))
        limit_map.RebinY(2)
        if rebin:
            limit_map = smthr.rebin(limit_map, "NE")

        limit_map_deltam = deltaM(limit_map)

        # print "%s_%s" % (model, tmpname), fobs, fexp
        myLimit_nominal = limit(limit_map_deltam, model, lname, var)

        canv.cd(1)
        thisratio = myLimit_nominal._ratioMap.Clone()
        thisratio2 = myLimit_nominal._ratioMap.Clone()
        # thisratio.GetXaxis().SetRangeUser(100., 350.)
        # thisratio.GetYaxis().SetRangeUser(0., 350.)
        thisratio.GetZaxis().SetRangeUser(0.7, 1.1)
        thisratio.Draw("colztext")
        
        canv.cd(2)
        myLimit_nominal.curveFromMap()
        # myLimit_nominal._ratioMap.GetXaxis().SetRangeUser(100., 350.)
        # myLimit_nominal._ratioMap.GetYaxis().SetRangeUser(0., 350.)
        myLimit_nominal._ratioMap.Draw("colz")
        myLimit_nominal._curve.Draw("lsame")
        if myLimit_nominal._curvetwo: 
            myLimit_nominal._curvetwo .Draw("lsame")
        
            # new_curve = deltaM_curve(myLimit_nominal._curvetwo)
            # new_curve.Draw("la")
        canv.Print("limit_%s_%s.pdf" % (model, lname))

        canv1 = r.TCanvas()
        # get back the smoothed colour map
        # note: smooth used on the ratio map to avoid artefacts
        # if lname == "UpperLimit":
        #     smoothFactorMap = myLimit_nominal._postSmoothRatioMap.Clone()
        #     smoothFactorMap.Divide(thisratio2)
            
            # limit_map.GetXaxis().SetRangeUser(100., 400.)
            # limit_map.GetYaxis().SetRangeUser(0., 400.)
        #     limit_map.Draw("colztext")
        #     canv1.Print("limit_limitMapRaw.pdf")

        #     print limit_map.GetNbinsX(), limit_map.GetNbinsY()

            # smoothFactorMap.GetXaxis().SetRangeUser(100., 400.)
            # smoothFactorMap.GetYaxis().SetRangeUser(0., 400.)
        #     smoothFactorMap.Draw("colz")
        #     canv1.Print("limit_smoothFactorMapRaw.pdf")
        #     facts = {}
        #     for xbin in range(1, smoothFactorMap.GetNbinsX()+2):
        #         xmass = smoothFactorMap.GetXaxis().GetBinCenter(xbin)
        #         for ybin in range(1, smoothFactorMap.GetNbinsY()+2):
        #             ymass = smoothFactorMap.GetYaxis().GetBinCenter(ybin)
        #             smoothFactor = smoothFactorMap.GetBinContent(xbin, ybin)
        #             # print xmass, ymass, smoothFactor
                    
        #             if ymass > xmass-100:
        #                 smoothFactor = 0.

        #             if xmass - ymass == 100.:
        #                 smoothFactor = 1.

        #             if ymass == 300. and model == "T2tt":
        #                 smoothFactor = 1.

        #             if xmass < 200. and model == "T2tt":
        #                 smoothFactor = 0.

        #             if model == "T2bw_0p25" and xmass == 125. and ymass == 0.:
        #                 smoothFactor = 1.
        #             if model == "T2bw_0p25" and xmass == 550.:
        #                 smoothFactor = 1.
        #             if model == "T2bw_0p25" and ymass == 300.:
        #                 smoothFactor = 1.
        #             # if model == "T2bw_0p25" and xmass > 600.:
        #             #     smoothFactor = 1.
        #             # if model == "T2bw_0p25" and ymass > 350.:
        #             #     smoothFactor = 1.


        #             if ma.isnan(smoothFactor):
        #                 smoothFactor = 1.

        #             if smoothFactor > 2. or smoothFactor < 0.2:
        #                 smoothFactor = 1.

        #             if model == "T2bw_0p75" and xmass == 200. and ymass == 100.:
        #                 smoothFactor = 27.

        #             if model == "T2bw_0p75" and xmass == 400. and ymass == 225.:
        #                 smoothFactor = 2.

        #             if model == "T2bw_0p75" and xmass == 225. and ymass == 125.:
        #                 smoothFactor = 3.25

        #             # print xmass, ymass, smoothFactor

        #             smoothFactorMap.SetBinContent(xbin, ybin, smoothFactor)
        #             facts["%s_%s" % (xmass, ymass)] = smoothFactor
            # smoothFactorMap.GetXaxis().SetRangeUser(100., 400.)
            # smoothFactorMap.GetYaxis().SetRangeUser(0., 400.)
        #     # smoothFactorMap.Write()
        #     # print facts
        #     print facts["200.0_100.0"]
        #     smoothFactorMap.Draw("colztext")
            # smoothFactorMap. GetXaxis().SetRangeUser(100., 400.)
            # smoothFactorMap. GetYaxis().SetRangeUser(0., 400.)
        #     canv1.Print("limit_smoothFactorMap.pdf")

        #     # limit_map_smoothed = limit_map.Clone()
        #     # limit_map_smoothed.Multiply(smoothFactorMap)

        #     limit_map_smoothed = r.TH2D("%s_UpperLimit_smoothed" % model, "%s_UpperLimit_smoothed" % model,
        #                                 38, 87.5, 1037.5,
        #                                 39, -12.5, 962.5)

        #     for xbin in range(1, limit_map_smoothed.GetNbinsX()+2):
        #         xmass = limit_map_smoothed.GetXaxis().GetBinCenter(xbin)
        #         for ybin in range(1, limit_map_smoothed.GetNbinsY()+2):
        #             ymass = limit_map_smoothed.GetYaxis().GetBinCenter(ybin)

        #             try:
        #                 fact = facts["%s_%s" % (xmass, ymass)]
        #             except KeyError:
        #                 # print "No %s_%s" % (xmass, ymass)
        #                 fact = 1.
        #             if type(fact) != float:
        #                 print fact

        #             if ma.isnan(limit_map.GetBinContent(xbin, ybin)) or ma.isnan(fact):
        #                 continue

        #             limit_map_smoothed.SetBinContent(xbin, ybin, fact * limit_map.GetBinContent(xbin, ybin))

        #             # these values taken from asymptotic limits
        #             if model == "T2bw_0p75":
        #                 if xmass == 100. and ymass == 0.:
        #                     # upper limit comes out as ~700. assume there's a CLs plot problem, so use 150. for now
        #                     limit_map_smoothed.SetBinContent(xbin, ybin, 150.)
        #             if model == "T2bw_0p25":
        #                 if xmass == 100. and ymass == 0.:
        #                     limit_map_smoothed.SetBinContent(xbin, ybin, 94.85)
        #                 if xmass == 475. and ymass == 275.:
        #                     limit_map_smoothed.SetBinContent(xbin, ybin, 0.25)

        #     # limit_map_smoothed.SetMaximum(200.)
        #     # limit_map_smoothed.SetMinimum(1.e-2)
        #     # canv1.SetLogz(1)
        #     limit_map_smoothed.Draw("colztext")
        #     canv1.Print("limit_smoothedMap.pdf")
        #     print smoothFactorMap.GetMean()
        #     print limit_map_smoothed.GetMean()
        #     print limit_map.GetMean()
        #     limit_map_smoothed.SetName("%s_UpperLimit_smoothed" % model)
        #     limit_map_smoothed.Write()

        # myLimit_nominal._curve.Write()
        # if myLimit_nominal._curvetwo:
        #     myLimit_nominal._curvetwo.Write()
        # limit_map.Write()

        del myLimit_nominal

    fo.Close()


if __name__ == "__main__":
    main()