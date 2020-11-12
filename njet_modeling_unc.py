import ROOT
import glob
import os
from math import sqrt
from SWup.coolPlot import coolPlot
from multiprocessing import Pool


ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

campaign = ["mc16a","mc16d","mc16e","mc16"]
campaign = ["mc16"]
pts = [20,40,60,80,100]

systsA = [
 "weight_pdf_up",
 "weight_pdf_down",
 "weight_pdf_mmht",
 "weight_pdf_ct14",
]
systsB = [
 "weight_scale_muR20_muF20",
 "weight_scale_muR05_muF05",
 "weight_scale_muR10_muF20",
 "weight_scale_muR10_muF05",
 "weight_scale_muR20_muF10",
 "weight_scale_muR05_muF10",
]
systsC = {
    "ttV_sherpa" : [("ttV","aMcAtNlo")],
    "fourtop"    : [("fourtop_syst","Herwig 7")],
}

samples = ["multibosons","ttV_sherpa","minor","fourtop"]
maxjet = 15
minjet = 4

def variationsAndPlot(systlist, systname, nominal, c,sample, pt, njet, cut, tree, alternative=False):
    hists = {}
    if alternative:
        titlelist = [s[1] for s in systlist]
        systlist  = [s[0] for s in systlist]
    else:
        titlelist = [s.replace("weight_","").      replace("sf_total__SYST_","").replace("/sf_total","") for s in systlist]

    for sys in systlist:
        hname = "hsys_%s%s%d"%(sample,sys,pt)
        hsys = ROOT.TH1D(hname,hname+";Number of jets;Events",maxjet-minjet+1,minjet-0.5,maxjet+0.5)
        if alternative:
            sysfiles = glob.glob("/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/%s_%s*/*root"%(sys,c))
            systree = ROOT.TChain()
            for f in sysfiles:
                systreename = f.split("/")[-2]+"_Nom"
                systree.AddFile(f,ROOT.TTree.kMaxEntries,systreename)
            if not systree.GetEntries():
                print "NO ENTRIES",sys,c
            systree.Draw("%s >> %s"%(njet,hname),cut,'goff')
        else: 
            tree.Draw("%s >> %s"%(njet,hname),cut+'*(%s)'%sys,'goff')
        hists[sys] = hsys
    print "Will plot","njet_%s_%s_%d_%s"%(c,sample,pt,systname)
    coolPlot("njet_%s_%s_%d_%s"%(c,sample,pt,systname) ,[nominal]+[hists[s] for s in systlist],formats=("png","pdf","C"),folder="figures/njet_syst", titlelist = ["nominal"]+titlelist , yrangeratio=[0.01,1.99],forcehistoption=True)

def main():
    pool = Pool()
    for sample in samples:
      for c in campaign:
        files = glob.glob("/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/%s_%s*/*root"%(sample,c))
        tree = ROOT.TChain()
        for f in files:
            treename = f.split("/")[-2]+"_Nom"
            tree.AddFile(f,ROOT.TTree.kMaxEntries,treename)
        if not tree.GetEntries():
            print "NO ENTRIES",sample,c
            continue
        
        can = ROOT.TCanvas()
        for i,pt in enumerate(pts):
            hname = "h1d_%s%d"%(sample,pt)
            h1d = ROOT.TH1D(hname,hname+";Number of jets;Events",maxjet-minjet+1,minjet-0.5,maxjet+0.5)
            njet = "min(n_jet{},%d)"%maxjet
            if pt==20: 
                njet = njet.format("")
            else:
                njet = njet.format(pt)
            cut = '(weight*xs_weight)*((el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total * sf_el_trigger * sf_mu_trigger )'
            print "Will draw",pt
            tree.Draw("%s >> %s"%(njet,hname),cut,'goff')
            h1d.SetLineWidth(2)
            h1d.SetLineColor(i+1)
        
            pool.apply_async(variationsAndPlot,  args=(systsA, "systsA", h1d.Clone(), c,sample,pt, njet, cut, tree))
            pool.apply_async(variationsAndPlot,  args=(systsB, "systsB", h1d.Clone(), c,sample,pt, njet, cut, tree))
            if sample in systsC:
                pool.apply_async(variationsAndPlot,  args=(systsC[sample], "systsC", h1d.Clone(), c,sample,pt, njet, cut, tree, sample))
        del tree
    pool.close()
    pool.join()

if __name__ == "__main__": main()
