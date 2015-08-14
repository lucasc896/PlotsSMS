import ROOT as r
from pytils import safe_divide
r.gROOT.SetBatch(0)

def obs_holes(model = ""):

    return {"T2bw_0p75": [(150.,25.), (150.,50.), (250.,100.), (350.,200.), (350., 250.), (400.,250.), (100., 0.)],
            "T2bw_0p25": [(125.,25.), (100.,0.)],}[model]

def exp_holes(model = ""):

    return {"T2bw_0p75": [(150.,25.), (150.,50.), (100., 0.)],
            "T2bw_0p25": [(125.,25.), (100., 0.)],}[model]


def polyFilla(hist = None, xbin = None, ybin = None):

    tot = 0.
    count = 0
    if hist.GetBinContent(xbin+1, ybin) > 0.:
        tot += hist.GetBinContent(xbin+1, ybin)
        count += 1
    if hist.GetBinContent(xbin-1, ybin) > 0.:
        tot += hist.GetBinContent(xbin-1, ybin)
        count += 1
    if hist.GetBinContent(xbin, ybin+1) > 0.:
        tot += hist.GetBinContent(xbin, ybin+1)
        count += 1
    if hist.GetBinContent(xbin, ybin-1) > 0.:
        tot += hist.GetBinContent(xbin, ybin-1)
        count += 1
    print xbin, ybin, tot

    return safe_divide(tot, float(count))

def main():

    model = ['T2bw_0p25', 'T2bw_0p75'][1]
    f = r.TFile.Open("../config/SUS14006/latest_chris_contours/%s/%s_obs.root"%(model, model), "UPDATE")

    for histname in ["UpperLimit", "ExpectedUpperLimit", "ExpectedUpperLimit_p1_Sigma", "ExpectedUpperLimit_p2_Sigma", "ExpectedUpperLimit_m1_Sigma", "ExpectedUpperLimit_m2_Sigma"]:
        hist = f.Get("%s_%s" % (model, histname))

        canv = r.TCanvas()

        hist.Draw('colz')
        hist_new = hist.Clone()
        # canv.Print("tmp_%s.pdf" % histname)
        holes = exp_holes(model) if "Expected" in hist else obs_holes(model)
        for hole in holes:
            print "Plugging hole", hole
            xbin = hist.GetXaxis().FindBin(hole[0])
            ybin = hist.GetYaxis().FindBin(hole[1])
            hist_new.SetBinContent(xbin, ybin, polyFilla(hist_new, xbin, ybin))

        hist_new.Draw('colz')
        hist_new.SetName(hist_new.GetName() + "_filled")
        hist_new.Write()
        canv.Print("tmp_%s_filled.pdf" % histname)

if __name__ == "__main__":
    main()