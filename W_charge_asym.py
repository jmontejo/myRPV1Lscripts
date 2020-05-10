import ROOT
import glob
import os
from math import sqrt
from SWup.coolPlot import coolPlot

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

def printNice(h,pt):

    head = '    chargeasym["%d"] = {\n'%pt
    for b in range(1,h.GetNbinsX()):
        j = int(h.GetBinCenter(b))
        ca = h.GetBinContent(b)
        head += '       %d:%.2f,\n'%(j,ca)
    head += '}'
    print head

campaign = ["mc16a","mc16d","mc16e","mc16"]
campaign = ["mc16"]
pts = [20,40,60,80,100]
pts = [80,100]
bcuts = {
# "incl": 9,
 "0btag": 0,
}

systsA = [
 "sf_total__SYST_PRW_DATASF__1down/sf_total",
 "sf_total__SYST_PRW_DATASF__1up/sf_total",
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

for c in campaign:
    files = glob.glob("/eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.119_a/rpv2l_4j20_shrink/wjets_%s*/*root"%c)
    tree = ROOT.TChain()
    for f in files:
        treename = f.split("/")[-2]+"_Nom"
        tree.AddFile(f,ROOT.TTree.kMaxEntries,treename)
    
    for bcutname, bcut in bcuts.iteritems():
        h2d = ROOT.TH2D("h2d","h2d;Lepton charge asymmetry;Number of jets",3,-0.5,2.5,7,3.5,10.5)
        h1d = ROOT.TH1D("h1d","h1d;Lepton charge asymmetry;Number of jets",7,3.5,10.5)
        can = ROOT.TCanvas()
        hists = {}
        for i,pt in enumerate(pts):
            njet = "n_jet"
            nbjet = "n_bjet"
            if pt!=20: 
                njet += str(pt)
                nbjet += str(pt)
            cut = '((%s)<=%d)*(weight*xs_weight)*((el_trigger || mu_trigger) && lep_trigger_matched)'%(nbjet,bcut)
            #cut = '((%s)<=%d)*(weight*xs_weight)*((el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total * sf_el_trigger * sf_mu_trigger )'%(nbjet,bcut)
            print "Will draw",pt
            print tree.GetEntries()
            print tree.Draw("%s:lep_charge[0]+1 >> h2d"%njet,cut,'goff')
            print h2d.GetEntries()
            for b in range(1,h1d.GetNbinsX()+1):
                if h2d.GetBinContent(1,b) and h2d.GetBinContent(3,b):
                  print b, h2d.GetBinContent(3,b), h2d.GetBinContent(1,b)
                  h1d.SetBinContent(b, h2d.GetBinContent(3,b) / h2d.GetBinContent(1,b))
                  h1d.SetBinError(b, sqrt(pow(h2d.GetBinError(3,b)/h2d.GetBinContent(3,b),2) + pow(h2d.GetBinError(1,b)/h2d.GetBinContent(1,b),2))*h1d.GetBinContent(b))
            printNice(h1d,pt)
            h1d.GetXaxis().SetTitle("Number of jets")
            h1d.GetYaxis().SetTitle("Lepton charge asymmetry")
            h1d.GetYaxis().SetRangeUser(1.1,4)
            h1d.SetLineWidth(2)
            h1d.SetLineColor(i+1)
            hists[(pt,"nominal")] = h1d.Clone("%d"%pt)
    
            for sys in systsB:
                print "Will draw",pt,sys
                tree.Draw("%s:lep_charge[0]+1 >> h2d"%njet,cut+'*%s'%sys,'goff')
                for b in range(1,h1d.GetNbinsX()+1):
                    if h2d.GetBinContent(1,b) and h2d.GetBinContent(3,b):
                      h1d.SetBinContent(b, h2d.GetBinContent(3,b) / h2d.GetBinContent(1,b))
                      h1d.SetBinError(b, sqrt(pow(h2d.GetBinError(3,b)/h2d.GetBinContent(3,b),2) + pow(h2d.GetBinError(1,b)/h2d.GetBinContent(1,b),2))*h1d.GetBinContent(b))
                hists[(pt,sys)] = h1d.Clone(sys+"%d"%pt)
            coolPlot("W_charge_asym_%s_%s_%dsystsB"%(c,bcutname,pt) ,[hists[(pt,s)] for s in ["nominal"]+systsB],formats=("png","pdf","C"),folder="figures/charge_asymmetry", titlelist = ["nominal"]+[s.replace("weight_","").replace("sf_total__SYST_","").replace("/sf_total","") for s in systsB] , yrangeratio=[0.9,1.1])
            for sys in systsA:
                print "Will draw",pt,sys
                tree.Draw("%s:lep_charge[0]+1 >> h2d"%njet,cut+'*%s'%sys,'goff')
                for b in range(1,h1d.GetNbinsX()+1):
                    if h2d.GetBinContent(1,b) and h2d.GetBinContent(3,b):
                      h1d.SetBinContent(b, h2d.GetBinContent(3,b) / h2d.GetBinContent(1,b))
                      h1d.SetBinError(b, sqrt(pow(h2d.GetBinError(3,b)/h2d.GetBinContent(3,b),2) + pow(h2d.GetBinError(1,b)/h2d.GetBinContent(1,b),2))*h1d.GetBinContent(b))
                hists[(pt,sys)] = h1d.Clone(sys+"%d"%pt)
            coolPlot("W_charge_asym_%s_%s_%dsystsA"%(c,bcutname,pt) ,[hists[(pt,s)] for s in ["nominal"]+systsA],formats=("png","pdf","C"),folder="figures/charge_asymmetry", titlelist = ["nominal"]+[s.replace("weight_","").replace("sf_total__SYST_","").replace("/sf_total","") for s in systsA] , yrangeratio=[0.9,1.1])
        coolPlot("W_charge_asym_%s_%s"%(c,bcutname) ,[hists[(p,"nominal")] for p in pts],formats=("png","pdf"),folder="figures/charge_asymmetry", titlelist = ["jet p_{T} > %d GeV"%p for p in pts],plotratio=False )
    del tree
