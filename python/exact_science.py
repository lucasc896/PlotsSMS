import ROOT as r
from copy import deepcopy

def to_add(model = "", limit = ""):
    add = {
        "T2tt": {
            "UpperLimit": [(525.,0.),(225.,50.)][:1],
            "UpperLimit_m1_Sigma": [],
            "UpperLimit_p1_Sigma": [(550.,75.),(550.,0.)],
            "ExpectedUpperLimit": [(225.,0.),(175.,0.),(647.,0.)][-1:],
            "ExpectedUpperLimit_m1_Sigma": [(675.,0.)],
            "ExpectedUpperLimit_m2_Sigma": [(688.,0.),],
            "ExpectedUpperLimit_p1_Sigma": [(600.,0.)],
            "ExpectedUpperLimit_p2_Sigma": [(565.,0.)],
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
            "ExpectedUpperLimit_m1_Sigma": [(625.,175.),(625.,225.),(675.,175.),(680.,110.),(200.,20.)],
            "ExpectedUpperLimit_m2_Sigma": [],
            "ExpectedUpperLimit_p1_Sigma": [(550.,125.)],
            "ExpectedUpperLimit_p2_Sigma": [],
            "UpperLimit": [(200.,50.),(175.,75.),(150.,50.),(225.,25.),(220.,60.),],
            "UpperLimit_m1_Sigma": [(200.,50.),(500.,25.),],
            "UpperLimit_p1_Sigma": [(240.,25.),(525.,50.),(525.,75.),],
            },
    }
    try:
        return remove[model][limit]
    except KeyError:
        return []

def drop_point(point = (), model = "", limit = ""):
    for rem in to_remove(model, limit):
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


def do_exact_science(model = ""):
    # fpath = "/Users/chrislucas/SUSY/SignalScans/effStudies/SignalSystematics/PlotsSMS/config/SUS14006/latest_chris/%s/%s_obs.root" % (model, model)
    fpath = "/Users/chrislucas/SUSY/SignalScans/effStudies/SignalSystematics/PlotsSMS/T2tt_test.root"

    f = r.TFile.Open(fpath, 'UPDATE')

    curves = {}
    data = {}

    for k in f.GetListOfKeys():
        name = k.GetName()
        if model in name: continue
        if "_new" in name: continue
        curves[name] = k.ReadObj()

    # get values
    for c in curves:
        data[c] = extract_data(curves[c])

    for c in data:
        print c
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
        if c == "UpperLimit":
            print new_vals

        for ipoint, point in enumerate(new_vals):
            new_graph.SetPoint(ipoint, *point)

        new_graph.Write()

    f.Close()

def main():

    for model in ["T2tt", "T2bw_0p75", "T2bw_0p25"][:1]:
        do_exact_science(model)

if __name__ == "__main__":
    main()