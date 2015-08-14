import ROOT as r
from copy import deepcopy

def to_add(model = "", limit = ""):
    add = {
        "T2tt": {
            "UpperLimit": [(525.,0.),(150.,15.), (275.,50.)],
            "UpperLimit_m1_Sigma": [(275.,15.)],
            "UpperLimit_p1_Sigma": [(550.,75.),(550.,0.),(200.,15.)],
            "ExpectedUpperLimit": [(225.,0.),(175.,0.),(647.,0.)][-1:],
            "ExpectedUpperLimit_m1_Sigma": [(675.,0.),(200.,75.)],
            "ExpectedUpperLimit_m2_Sigma": [(688.,0.),(200.,75.)],
            "ExpectedUpperLimit_p1_Sigma": [(600.,0.)],
            "ExpectedUpperLimit_p2_Sigma": [(565.,0.)],
            },
        "T2bw_0p25": {
            "UpperLimit": [],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [],
            "ExpectedUpperLimit": [(375.,275.)],
            "ExpectedUpperLimit_m1_Sigma": [(440.,250.),(360.,50.),(380.,280.)],
            "ExpectedUpperLimit_m2_Sigma": [(475.,250.),(400.,0.),(400.,300.)],
            "ExpectedUpperLimit_p1_Sigma": [(300.,200.),(300.,50.)],
            "ExpectedUpperLimit_p2_Sigma": [(250.,150.)],
            },
        "T2bw_0p75": {
            "UpperLimit": [(445.,0.),(400.,100.),(225.,125.)],
            "UpperLimit_m1_Sigma": [(420.,0.),(410.,60.),(380.,0.)],
            "UpperLimit_p1_Sigma": [(460.,70.),(300.,125.)],
            "ExpectedUpperLimit": [(600.,0.),(225.,125.), (250.,125.)],
            "ExpectedUpperLimit_m1_Sigma": [(660.,0.),(640.,150.)],
            "ExpectedUpperLimit_m2_Sigma": [(680.,0.)],
            "ExpectedUpperLimit_p1_Sigma": [(540.,0.)],
            "ExpectedUpperLimit_p2_Sigma": [(450.,0.)],
            },
    }
    try:
        return add[model][limit]
    except KeyError:
        return []

def to_remove(model = "", limit = ""):
    remove = {
        "T2tt": {
            "ExpectedUpperLimit": [(200.,100.),(200.,75.),(200.,50.),(625.,0.),(650.,25.),(600.,150.)],
            "ExpectedUpperLimit_m1_Sigma": [(625.,175.),(625.,225.),(675.,175.),(680.,110.),(200.,20.),(220.,125.)],
            "ExpectedUpperLimit_m2_Sigma": [(590.,240.),(580.,250.),(275.,125.),(250.,75.)],
            "ExpectedUpperLimit_p1_Sigma": [(550.,125.)],
            "ExpectedUpperLimit_p2_Sigma": [],
            "UpperLimit": [(200.,50.),(175.,75.),(150.,50.),(225.,25.),(220.,60.),],
            "UpperLimit_m1_Sigma": [(200.,50.),(500.,25.),(220.,20.)],
            # "UpperLimit_p1_Sigma": [(240.,25.),(525.,50.),(525.,75.),(400,100.)],
            "UpperLimit_p1_Sigma": [(225.,75.),(175.,75.),(200.,50.),(235.,35.)]
            },
        "T2bw_0p25": {
            "UpperLimit": [(510.,300.)],
            "UpperLimit_m1_Sigma": [(510.,300.),(375.,200.)],
            "UpperLimit_p1_Sigma": [(510.,300.), (300.,280.)],
            "ExpectedUpperLimit": [(510.,300.),(375.,220.),(350.,75.),(420.,320.)],
            "ExpectedUpperLimit_m1_Sigma": [(510.,300.),(440.,270.),(420.,150.),(410.,310.)],
            "ExpectedUpperLimit_m2_Sigma": [(510.,310.),(470.,220.),(460.,230.),(420.,40.),(380.,0.),(475.,300.),(410.,310.)],
            "ExpectedUpperLimit_p1_Sigma": [(510.,300.),(400.,300.),(330.,210.),(330.,180.),(275.,0.)],
            "ExpectedUpperLimit_p2_Sigma": [(375.,275.),(310.,190.),(300.,125.)],
            },
        "T2bw_0p75": {
            "UpperLimit": [(440.,280.),(380.,280.),(450.,100.),(400.,0.),(420.,20.),(375.,80.)],
            "UpperLimit_m1_Sigma": [(440.,280.),(380.,280.),(310.,110.),(330.,110.),(380.,0.),(390.,40.)],
            "UpperLimit_p1_Sigma": [(440.,280.),(380.,280.),(500.,20.),(450.,50.),(450.,80.),(390.,90.),(310.,120.)],
            "ExpectedUpperLimit": [(550.,120.),(500.,150),(400.,225.),(250.,150.),(380.,160.),(420.,140.)],
            "ExpectedUpperLimit_m1_Sigma": [(660.,40.),(620.,0.),(540.,220.),(625.,125.),(660.,110.),(600.,200.),(650.,175.),(250.,160.),(425.,250.),(425.,200.),(450.,160.)],
            "ExpectedUpperLimit_m2_Sigma": [(680.,210.),(625.,200.),(625.,240.),(670.,100.),(310.,160.),(450.,250.),(440.,260.),(450.,200.)],
            "ExpectedUpperLimit_p1_Sigma": [(530.,0.),(520.,50.),(375.,125.),(260.,160.)],
            "ExpectedUpperLimit_p2_Sigma": [(400.,0.),(425.,20.),(450.,100.)],
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
    fpath = "/Users/chrislucas/SUSY/Parked/Signal/PlotsSMS/config/SUS14006/latest_chris/%s/%s_obs.root" % (model, model)
    # fpath = "/Users/chrislucas/SUSY/SignalScans/effStudies/SignalSystematics/PlotsSMS/%s_test.root" % model

    f = r.TFile.Open(fpath, 'UPDATE')

    curves = {}
    maps = {}
    data = {}

    for k in f.GetListOfKeys():
        name = k.GetName()
        if "_new" in name: continue
        if model in name:
            maps[name] = k.ReadObj()
            continue
        curves[name] = k.ReadObj()

    if [False, True][0]:
        print "WARNING: Trimming T2tt maps!"
        if raw_input("Continue? (y/n)") != "y": exit()
        if model != "T2tt": exit("Wrong model for trimming")
        new_maps = trim_maps(maps)
        for m in new_maps:
            new_maps[m].Write()
        f.Close()
        exit()


    # get values
    for c in curves:
        data[c] = extract_data(curves[c])

    for c in data:
        # hack to pick only one curve at a time
        # if c != "ExpectedUpperLimit": continue

        new_graph = r.TGraph()
        new_graph.SetName(c+"_new")
        new_vals = []

        # update new_vals list while ignoring points to remove
        for point in data[c]:
            if drop_point(point, model, c): continue
            new_vals.append(point)

        # add new points
        for new_point in to_add(model, c):
            new_vals.append(new_point)

        new_vals = order_points(new_vals)

        if c == "UpperLimit" and model == "T2tt":
            # new_vals = [(519.0, 19.0), (514.0, 39.0), (499.0, 49.0), (499.0, 74.0), (496.0, 96.0), (474.0, 99.0), (464.0, 114.0), (441.0, 116.0), (424.0, 124.0), (399.0, 124.0), (368.0, 118.0), (250.0, 15.0), (150.0, 15.0), (150.0, 0.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (500.0, 0.0), (525.0, 0.0), (519.0, 19.0)]
            new_vals = [(519.0, 19.0), (514.0, 39.0), (499.0, 49.0), (499.0, 74.0), (496.0, 96.0), (474.0, 99.0), (464.0, 114.0), (441.0, 116.0), (424.0, 124.0), (399.0, 124.0), (368.0, 118.0), (250.0, 15.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (500.0, 0.0), (525.0, 0.0), (519.0, 19.0)]

        if c == "UpperLimit_m1_Sigma" and model == "T2tt":
            # new_vals = [(475.0, 0.0), (474.0, 24.0), (474.0, 49.0), (474.0, 74.0), (463.0, 88.0), (449.0, 99.0), (424.0, 99.0), (399.0, 99.0), (388.0, 113.0), (349.0, 99.0), (275., 15.), (150.0, 0.0), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (475.0, 0.0)]
            new_vals = [(475.0, 0.0), (474.0, 24.0), (474.0, 49.0), (474.0, 74.0), (463.0, 88.0), (449.0, 99.0), (424.0, 99.0), (399.0, 99.0), (388.0, 113.0), (349.0, 99.0), (275., 15.), (200.0, 0.0), (250.0, 0.0), (275.0, 0.0), (300.0, 0.0), (325.0, 0.0), (350.0, 0.0), (375.0, 0.0), (400.0, 0.0), (425.0, 0.0), (450.0, 0.0), (475.0, 0.0), (475.0, 0.0)]

        for ipoint, point in enumerate(new_vals):
            new_graph.SetPoint(ipoint, *point)

        new_graph.Write()

    f.Close()

def main():

    for model in ["T2tt", "T2bw_0p75", "T2bw_0p25"][:1]:
        do_exact_science(model)

if __name__ == "__main__":
    main()