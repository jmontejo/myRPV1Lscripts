#!/usr/bin/env python
import argparse
default_folder = "/afs/cern.ch/work/a/atlrpv1l/outputs/input_for_fit_21.2.119_a_shapefix/pt20.0_minjet3_btag/"
parser = argparse.ArgumentParser()
parser.add_argument("--folder",default=default_folder)
parser.add_argument("--tag",default="")
opts = parser.parse_args()

import ROOT
import glob, os
from math import sqrt
from SWup.ext.tabulate import tabulate, tabulate_formats

with_error = False

files = glob.glob(opts.folder+"/*root")
print opts.folder,"has files: ", len(files)

yields = {}
for f in files:
    if "higgsino" in f and not "_higgsino" in f: continue
    if "stop" in f and not "stop_tbs_1075_600" in f: continue
    if "gluino" in f: continue
    if "incl" in f and not "15jincl" in f: continue
    if "excl" in f and "15jexcl" in f: continue
    if not "__" in f: continue
    name, rest = os.path.basename(f).split("__")
    if "shape" in rest: continue
    name = name.replace("_mc","")
    jet = int(rest[5:rest.find("j")])
    rfile = ROOT.TFile.Open(f)
    h = rfile.Get(name)
    if not h: h = rfile.Get(name+"_higgsino")
    if not name in yields: yields[name] = {}
    print f, name, jet
    yields[name][jet] = [(h.GetBinContent(b), h.GetBinError(b)) for b in range(1,h.GetNbinsX()+1)]
    rfile.Close()

headers1 = ["0 b-tag $\\ell^{-}$", "0 b-tag $\\ell^{+}$", "0 b-tag $m_{ll}$", "1 b-tag", "2 b-tag", "3 b-tag", "$\\geq$ 4 b-tag"]
headers2 = ["0 b-tag $3\\ell$", "0 b-tag", "1 b-tag", "2 b-tag", "3 b-tag", "$\\geq$ 4 b-tag"]
samples = [
    ("ttbar","\\ttbar"),
    ("wjets","$W$+jets"),
    ("zjets","$Z$+jets"),
    ("singletop","Single top"),
    ("multibosons","Dibosons"),
    ("ttV_sherpa","\\ttbar V"),
    ("qcd","Fake leptons"),
    ("fourtop","Four tops"),
    ("minor","Minor electroweak"),
    ("total","\hline Total background"),
    ("data","Data"),
    ("C1N1_higgsino_500","Higgsino C1N1 (500 \\gev)"),
    ("N1N2_higgsino_500","Higgsino N1N2 (500 \\gev)"),
    ("C1N1_higgsino_300_1L20","Higgsino C1N1 (300 \\gev)"),
    ("N1N2_higgsino_300_1L20","Higgsino N1N2 (300 \\gev)"),
    ("stop_tbs_1075_600","Stop (1075 \\gev) to higgsino (600 \\gev)"),
#    ("ttV_sherpa","\\ttbar V"),
#    ("ttW_sherpa","\\ttbar W"),
#    ("ttll_sherpa","\\ttbar ll"),
#    ("ttZhad_sherpa","\\ttbar Z (qq,vv)"),
]

for jet in range(4,15+1):
  table1 = []
  table2 = []
  total = None
  for sample, samplelatex in samples:
    if sample != "total":
        if not sample in yields:
            print "Missing sample",sample
            continue
        syields = yields[sample]
        jyields = syields[jet]
        if "higgsino" in sample or "stop" in sample: pass
        elif not total: total = jyields
        else:
            total = [(x+y, ex+ey) for (x,ex),(y,ey) in zip(total,jyields)]
    else:
        if not total: continue
        jyields = total
    row1 = [samplelatex]
    if with_error:
        row1 += ["{0:.0f} +/- {1:.0f}".format(val,err) for b,(val,err) in enumerate(jyields) if b < 7]
    else:
        row1 += ["{0:.1f}".format(max(0,val),err) for b,(val,err) in enumerate(jyields) if b < 7]
    table1.append(row1)
    if sample=="qcd" or sample == "C1N1_higgsino_300_1L20": continue
    row2 = [samplelatex]
    if with_error:
        row2 += ["{0:.1f} +/- {1:.1f}".format(val,err) for b,(val,err) in enumerate(jyields) if b >= 7 and b<13]
    else:
        row2 += ["{0:.1f}".format(max(0,val),err) for b,(val,err) in enumerate(jyields) if b >= 7 and b<13]
    table2.append(row2)

  outfolder = "tables/"+opts.tag
  if not os.path.exists(outfolder): os.mkdir(outfolder)
  with open(outfolder+"/yields_1L_%dj.tex"%jet,"w") as outfile:
    outfile.write( tabulate(table1,headers=["\\textbf{1-lepton, %d jets (20 \\gev)}"%jet]+headers1,tablefmt="latex_raw") )
  with open(outfolder+"/yields_2L_%dj.tex"%jet,"w") as outfile:
    outfile.write( tabulate(table2,headers=["\\textbf{Same-sign leptons, %d jets (20 \\gev)}"%jet]+headers2,tablefmt="latex_raw") )
