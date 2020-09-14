#!/usr/bin/env python
import ROOT
import glob
import argparse
import os

ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2(1)

default_production = "/eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/"
parser = argparse.ArgumentParser()
parser.add_argument("--production", default=default_production)
parser.add_argument("--minjet", type=int, default=4)
parser.add_argument("--maxjet", type=int, default=15)
parser.add_argument("--onlyMC16a", action="store_true")
parser.add_argument("--quick-test", action="store_true")
parser.add_argument("--sample", help="Exported sample name") 
parser.add_argument("--filter-sample", default="",help="Pattern to filter within the sample") 
parser.add_argument("--outsample", help="Sample name in the output file") 
parser.add_argument("--sample-cut", help="Cut specific to this sample") 
opts = parser.parse_args()

isData = "data" in opts.sample
hists = {}
cuts = { 
    (20,None): None,
    (40,None): None,
    (60,None): None,
    (80,None): None,
    (100,None): None,
}


if not isData:
    mc16part = "mc16a" if opts.onlyMC16a or opts.quick_test else "mc16"
    files = glob.glob(opts.production+"/%s_%s*/*%s*root"% (opts.sample, mc16part,opts.filter_sample))
else:
    mc16part = "data15" if opts.onlyMC16a or opts.quick_test else "data"
    files = glob.glob(opts.production+"/data/%s*%s*root"% (opts.sample, mc16part,opts.filter_sample))
tree = ROOT.TChain()
for f in files:
    treename = f.split("/")[-2]
    if not isData: treename += "_Nom"
    tree.AddFile(f,ROOT.TTree.kMaxEntries,treename)

mc16part = "test" if opts.quick_test else mc16part

for (jetpt,cutname), cut in cuts.iteritems():
    tag = mc16part+"_"+str(jetpt)
    cutstring = "(lep_pt[0]>27e3 && (el_trigger || mu_trigger))*(xs_weight*weight*sf_total*sf_mu_trigger*sf_el_trigger*139100)"
    if opts.sample_cut:
        cutstring += "*(%s)"% opts.sample_cut
    if cutname: 
        tag += "_"+cutname
        cutstring += "*(%s)"% cut
    histoname = "njet_%s_%s"%(opts.outsample,tag)
    hjet = ROOT.TH1D(histoname,histoname+";Number of jets;Events",opts.maxjet-opts.minjet+1,opts.minjet-0.5,opts.maxjet+0.5)
    print ("Sum$(jet_pt>%de3) >> %s" % (jetpt,histoname), cutstring)
    tree.Draw("Sum$(jet_pt>%de3) >> %s" % (jetpt,histoname), cutstring.format(pt=jetpt),"",10000 if opts.quick_test else ROOT.TTree.kMaxEntries)
    hists[(jetpt,cutname)] = hjet

outfile = "figures/Vjets_validation/Vscaling_files.root"
routfile = ROOT.TFile.Open(outfile,"update")
for j in hists.itervalues():
    j.Write()
routfile.Close()
