import ROOT as r
from copy import deepcopy

def models():
    return ["T2tt", "T2bw_0p75", "T2bw_0p25", "T2_4body", "T2cc"]

def sqProc(q="", daughter=""):
    if not daughter:
        daughter = q
    chi = "#tilde{#chi}^{0}_{1}"
    if daughter == 'b':
        chi = "#tilde{#chi}^{#pm}_{1}"
    out = "pp #rightarrow #tilde{%s} #tilde{%s}" % (q, q)
    out  = "#tilde{%s} #rightarrow %s %s" % (q, daughter, chi)
    # out += "; m(#tilde{g})>>m(#tilde{%s})" % q
    return out

def process_stamp(model = ""):
    return {"T2tt": sqProc("t"),
            "T2bw_0p25": sqProc("t", "b")+" (x=0.25)",
            "T2bw_0p75": sqProc("t", "b")+" (x=0.75)",
            "T2cc": sqProc("t", "c"),
            "T2_4body": sqProc("t", "bf#bar{f'}")}[model]

def model_cols(model = ""):
    return {"T2tt": r.kRed,
            "T2bw_0p25": r.kGreen+1,
            "T2bw_0p75": r.kBlue,
            "T2cc": r.kOrange,
            "T2_4body": r.kViolet}[model]

class contourGroup(object):
    """contour object"""
    def __init__(self, contours, model, label):
        self._contours = contours
        self._colour = model_cols(model)
        self._model = model
        self._label = label

    def __str__(self):
        return self._label

    def process_string(self, string):
        self._label = string

    # def SetColour(self, col):
    #     self._contour.SetLineColor(col)

    def Contours(self):
        return self._contours

    # def Draw(self, copts = "lsame"):
    #     for cont in self._contours:
    #         self._contours[cont].Draw(copts)

def empty():

    hist = r.TH2D("emptyHisto", "", 1, 100., 750., 1, 0., 450. )
    hist.GetXaxis().SetTitle("m_{#tilde{t}} (GeV)")
    hist.SetTitleOffset(1.3, "x")
    hist.GetYaxis().SetTitle("m_{LSP} (GeV)")
    hist.SetTitleOffset(1.4, "y")

    return hist

def get_model_contours(model = "", cont_names = ["ExpectedUpperLimit", "ExpectedUpperLimit_p1_Sigma", "ExpectedUpperLimit_m1_Sigma"]):
    
    if model in ["T2cc", "T2_4body"]:
        infile = "config/SUS14006/chris/%s/%s_obs.root" % (model, model)
        suf = ""
    elif model == "T2tt":
        infile = "config/SUS14006/latest_chris_contours/T2tt/T2tt_newContCurves_newSysts_v2.root"
        suf = ""
    else:
        infile = "config/SUS14006/latest_chris_contours/%s/%s_newContCurves.root" % (model, model)
        suf = "_new"
    print infile
    f = r.TFile.Open(infile)

    contours = {}



    for c in cont_names:
        getter = c + suf
        if model == "T2tt" and "Expected" in c:
            getter += "_two"
        contours[c] = f.Get(getter) 

    print model, contours

    return contours

def get_legend():

    outg = []
    outt = []

    LObsP = r.TGraph(2)
    LObsP.SetName("LObsP")
    LObsP.SetTitle("LObsP")
    LObsP.SetLineColor(r.kBlack)
    LObsP.SetLineStyle(1)
    LObsP.SetLineWidth(3)
    LObsP.SetPoint(0, 305., 420.)
    LObsP.SetPoint(1,355., 420.)

    outg.append(LObsP)

    LExpP = r.TGraph(2)
    LExpP.SetName("LExpP")
    LExpP.SetTitle("LExpP")
    LExpP.SetLineColor(r.kBlack)
    LExpP.SetLineStyle(2)
    LExpP.SetLineWidth(3)
    LExpP.SetPoint(0, 305., 390.)
    LExpP.SetPoint(1,355., 390.)

    outg.append(LExpP)

    textObs = r.TLatex(160., 415., "Observed")
    textObs.SetTextFont(42)
    textObs.SetTextSize(0.04)

    outt.append(textObs)

    textExp = r.TLatex(160., 385., "Expected")
    textExp.SetTextFont(42)
    textExp.SetTextSize(0.04)

    outt.append(textExp) 

    modx = 520.
    mody = 390.

    texpp = r.TLatex(modx+55., mody+30., "pp #rightarrow #tilde{t} #tilde{t},")
    texpp.SetTextFont(42)
    texpp.SetTextSize(0.035)
    outt.append(texpp)

    for model in models():
        graph = r.TGraph(2)
        graph.SetName("model")
        graph.SetTitle("model")
        graph.SetLineColor(model_cols(model))
        graph.SetLineStyle(1)
        graph.SetLineWidth(3)
        graph.SetPoint(0, modx, mody)
        graph.SetPoint(1, modx+50., mody)

        outg.append(graph)

        textT2tt = r.TLatex(modx+60., mody-6., process_stamp(model))
        textT2tt.SetTextFont(42)
        textT2tt.SetTextSize(0.03)
        outt.append(textT2tt)

        mody -= 40.



    # tex1 = r.TLatex(135., 410., "CMS Preliminary")
    # tex1.SetTextFont(42)
    # tex1.SetTextSize(0.03)
    # outt.append(tex1)

    # tex2 = r.TLatex(135., 375., "#sqrt{s } = 8 TeV")
    # tex2.SetTextFont(42)
    # tex2.SetTextSize(0.03)
    # outt.append(tex2)

    # texL = r.TLatex(135., 340., "#int L dt = 18.5 fb^{-1}")
    # texL.SetTextFont(42)
    # texL.SetTextSize(0.03)
    # outt.append(texL)

    # tex3 = r.TLatex(135., 305., "#alpha_{T} Parked")
    # tex3.SetTextFont(42)
    # tex3.SetTextSize(0.03)
    # outt.append(tex3)


    # tex3 = r.TLatex(120., 465., "CMS Preliminary, 18.5 fb^{-1}, #sqrt{s } = 8 TeV, #alpha_{T}")
    tex3 = r.TLatex(460., 460., "18.5 fb^{-1} (8 TeV), #alpha_{T}")
    tex3.SetTextFont(42)
    tex3.SetTextSize(0.045)
    outt.append(tex3)

    tex4 = r.TLatex(100., 460., "CMS")
    tex4.SetTextFont(42)
    tex4.SetTextSize(0.045)
    outt.append(tex4)

    return {"graphs":outg, "text":outt}

def get_text():

    text1 = r.TLatex(150., 510., "CMS Preliminary, #sqrt{s} = 8TeV,  #alpha_{T}")
    text1.SetTextFont(42)
    text1.SetTextSize(0.04)

    return [text1]

def main():

    r.gStyle.SetOptStat(0)

    mods = models()

    model_contours = {}

    for mod in mods:
        model_contours[mod] = get_model_contours(mod, ["ExpectedUpperLimit", "UpperLimit"])

    canv = r.TCanvas("canv", "canv", 600, 600)
    r.gPad.SetLeftMargin(2.)
    # lg = r.TLegend(0.6, 0.6, 0.89, 0.89)
    emptyHisto = empty()
    emptyHisto.Draw("")

    for model in mods:
        for cont_name in model_contours[model]:
            this_contour = model_contours[model][cont_name]
            
            if model == "T2tt":
                remove = []
                doremove = False
                for i in range(this_contour.GetN()+1):
                    x = r.Double(0.)
                    y = r.Double(0.)
                    this_contour.GetPoint(i, x, y)
                    if doremove: remove.append(i)
                    if x == 200.:
                        doremove = True
                    
                for i in reversed(remove):
                    this_contour.RemovePoint(i)

            this_contour.Draw("lsame")
            
            this_contour.SetLineColor(model_cols(model))

            if "Expected" in cont_name:
                this_contour.SetLineWidth(3)
                this_contour.SetLineStyle(2)
            else:
                this_contour.SetLineWidth(3)

    leg = get_legend()
    for l in leg:
        if l == "graphs":
            for g in leg[l]:
                g.Draw("lsame")
        else:
            for t in leg[l]:
                t.Draw()

    canv.Print("tmp.pdf")

if __name__ == "__main__":
    main()