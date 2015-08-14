import ROOT as r
from copy import deepcopy

def to_add(model = "", limit = ""):
    add = {
        "T2tt": {
            "UpperLimit": [(200., 0.)],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            },
        "T2bw_0p25": {
            "UpperLimit": [],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            },
        "T2bw_0p75": {
            "UpperLimit": [],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            },
    }
    try:
        return add[model][limit]
    except KeyError:
        return []

def to_remove(model = "", limit = ""):
    remove = {
        "T2tt": {
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            "UpperLimit": [(225.,0.)],
            "UpperLimit_m1_Sigma": [],
            # "UpperLimit_p1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            },
        "T2bw_0p25": {
            "UpperLimit": [],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            },
        "T2bw_0p75": {
            "UpperLimit": [],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [],
            "ExpectedUpperLimit_m1_Sigma": [],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit_p2_Sigma": [],
            },
    }
    try:
        return remove[model][limit]
    except KeyError:
        return []

def drop_point(point = (), model = "", limit = ""):
    for rem in to_remove(model, limit):
        if model == "T2tt" and point[0] < 200.: return True #hack to remove all points below 200 GeV strip
        if abs(point[0] - rem[0]) > 12.: continue
        if abs(point[1] - rem[1]) > 12.: continue
        return True
    return False

def extract_data(graph = None):

    out = []

    for n in range(graph.GetN()):
        x = r.Double()
        y = r.Double()
        val = graph.GetPoint(n, x, y)
        out.append((x, y))

    return out

def round_25(val = None):
    extra = val%25
    if val < 12.5:
        return val-extra
    else:
        return val+(25-extra)

def order_points(points = []):
    # hacky method copied from Rob in compareXs.py

    tmp = {}
    for p in points:
        dm = p[0]-p[1] #mass splitting
        dm = round_25(dm)
        if dm not in tmp.keys(): tmp[dm] = []
        tmp[dm].append(p)
    
    newtmp = {}
    for key, t in tmp.items():
        if len(t) > 1:
            if t[0][0] > t[1][0]:
                newtmp[-key] = t[0]
                newtmp[key] = t[1]
            else:
                newtmp[-key] = t[1]
                newtmp[key] = t[0]
        else:
            newtmp[key] = t[0]

    out = [newtmp[key] for key in sorted(newtmp.keys())] + [newtmp[sorted(newtmp.keys())[0]]]

    return out


#---------------------------------------------------------------------#

def trim_maps(maps = {}):
    out = {}

    for m in maps:
        newmap = maps[m].Clone()
        newmap.SetName(newmap.GetName() + "_trimmed")
        for xbin in range(1, maps[m].GetNbinsX()+1):
            if maps[m].GetXaxis().GetBinCenter(xbin) < 200.:
                for ybin in range(1, maps[m].GetNbinsY()+1):
                    val = newmap.GetBinContent(xbin, ybin)
                    if val > 0.:
                        newmap.SetBinContent(xbin, ybin, 0.) # set to zero if below 200 GeV and has a value
            if maps[m].GetXaxis().GetBinCenter(xbin) > 200.: break
        out[m] = newmap
    return out

#---------------------------------------------------------------------#

def do_exact_science(model = ""):
    fpath = "/Users/chrislucas/SUSY/Parked/Signal/PlotsSMS/config/SUS14006/latest_chris_contours/%s/%s_newContCurves.root" % (model, model)
    print fpath

    f = r.TFile.Open(fpath, 'UPDATE')
    # f = r.TFile.Open(fpath, 'READ')

    curves = {}
    maps = {}
    data = {}

    #  for k in f.GetListOfKeys():
    #     name = k.GetName()
    #     print name, k
    #     if "_new" in name: continue
    #     if model in name:
    #         maps[name] = k.ReadObj()
    #         continue
    #     curves[name] = k.ReadObj()

    curves['UpperLimit'] = f.Get("UpperLimit")

    if [False, True][0]:
        print "WARNING: Trimming T2tt maps!"
        if raw_input("Continue? (y/n)") != "y": exit()
        if model != "T2tt": exit("Wrong model for trimming")
        new_maps = trim_maps(maps)
        for m in new_maps:
            new_maps[m].Write()
        f.Close()
        exit()

    canv = r.TCanvas()

    # get values
    for c in curves:
        if c != "UpperLimit": continue
        print curves[c].GetN()
        data[c] = extract_data(curves[c])

    print data
    for c in data:
        # hack to pick only one curve at a time

        new_graph = r.TGraph()
        new_graph.SetName(c+"_new")
        new_vals = []
        print data[c]
        # update new_vals list while ignoring points to remove
        for point in data[c]:
            if drop_point(point, model, c): continue
            new_vals.append(point)

        # add new points
        for new_point in to_add(model, c):
            new_vals.append(new_point)

        # new_vals = order_points(new_vals)
        print new_vals

        # if c == "UpperLimit" and model == "T2tt":
        #     # new_vals = [(519.0, 19.0), (514.0, 39.0), (499.0, 49.0), (499.0, 74.0), (496.0, 96.0), (474.0, 99.0), (464.0, 114.0), (441.0, 116.0), (424.0, 124.0), (399.0, 124.0), (368.0, 118.0), (250.0, 15.0), (150.0, 15.0), (150.0, 0.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (500.0, 0.0), (525.0, 0.0), (519.0, 19.0)]
        #     new_vals = [(519.0, 19.0), (514.0, 39.0), (499.0, 49.0), (499.0, 74.0), (496.0, 96.0), (474.0, 99.0), (464.0, 114.0), (441.0, 116.0), (424.0, 124.0), (399.0, 124.0), (368.0, 118.0), (250.0, 15.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (500.0, 0.0), (525.0, 0.0), (519.0, 19.0)]

        # if c == "UpperLimit_m1_Sigma" and model == "T2tt":
        #     # new_vals = [(475.0, 0.0), (474.0, 24.0), (474.0, 49.0), (474.0, 74.0), (463.0, 88.0), (449.0, 99.0), (424.0, 99.0), (399.0, 99.0), (388.0, 113.0), (349.0, 99.0), (275., 15.), (150.0, 0.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (475.0, 0.0)]
        #     new_vals = [(475.0, 0.0), (474.0, 24.0), (474.0, 49.0), (474.0, 74.0), (463.0, 88.0), (449.0, 99.0), (424.0, 99.0), (399.0, 99.0), (388.0, 113.0), (349.0, 99.0), (275., 15.), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (475.0, 0.0)]

        for ipoint, point in enumerate(new_vals):
            new_graph.SetPoint(ipoint, *point)

        new_graph.Write()
        new_graph.Draw("al")
        canv.Print("tmp"+c+".pdf")


    f.Close()

def main():

    for model in ["T2tt", "T2bw_0p75", "T2bw_0p25"][:1]:
        do_exact_science(model)

if __name__ == "__main__":
    main()