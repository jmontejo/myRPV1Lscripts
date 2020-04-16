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

files = glob.glob("/eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_mc16*/*root")
tree = ROOT.TChain()
for f in files:
    treename = f.split("/")[-2]+"_Nom"
    tree.AddFile(f,ROOT.TTree.kMaxEntries,treename)

pts = [20,40,60,80]
bcuts = {
# "incl": 9,
 "0btag": 0,
}
systs = [
 "weight_scale_muR20_muF20",
 "weight_scale_muR05_muF05",
 "weight_scale_muR10_muF20",
 "weight_scale_muR10_muF05",
 "weight_scale_muR20_muF10",
 "weight_scale_muR05_muF10",
 "weight_pdf_up",
 "weight_pdf_down",
 "weight_pdf_mmht",
 "weight_pdf_ct14",
]
for bcutname, bcut in bcuts.iteritems():
    h2d = ROOT.TH2F("h2d","h2d;Lepton charge asymmetry;Number of jets",3,-0.5,2.5,7,3.5,10.5)
    h1d = ROOT.TH1F("h1d","h1d;Lepton charge asymmetry;Number of jets",7,3.5,10.5)
    can = ROOT.TCanvas()
    hists = {}
    for i,pt in enumerate(pts):
        tree.Draw("Sum$(jet_pt>%de3):lep_charge[0]+1 >> h2d"%pt,'(Sum$(jet_pt>%de3 && jet_bjet)<=%d)*(weight*xs_weight)*(jet_pt[1]>30e3 && lep_pt[0]>27e3 && (el_trigger || mu_trigger))*(sf_total * sf_el_trigger * sf_mu_trigger )'%(pt,bcut),'goff')
        for b in range(1,h1d.GetNbinsX()+1):
            if h2d.GetBinContent(1,b) and h2d.GetBinContent(3,b):
              h1d.SetBinContent(b, h2d.GetBinContent(3,b) / h2d.GetBinContent(1,b))
              h1d.SetBinError(b, sqrt(pow(h2d.GetBinError(3,b)/h2d.GetBinContent(3,b),2) + pow(h2d.GetBinError(1,b)/h2d.GetBinContent(1,b),2))*h1d.GetBinContent(b))
        printNice(h1d,pt)
        h1d.GetXaxis().SetTitle("Number of jets")
        h1d.GetYaxis().SetTitle("Lepton charge asymmetry")
        h1d.GetYaxis().SetRangeUser(1.1,4)
        h1d.SetLineWidth(2)
        h1d.SetLineColor(i+1)
        hists[(pt,"nominal")] = h1d.Clone("%d"%pt)

        for sys in systs:
            tree.Draw("Sum$(jet_pt>%de3):lep_charge[0]+1 >> h2d"%pt,'(Sum$(jet_pt>%de3 && jet_bjet)<=%d)*(weight*xs_weight)*(jet_pt[1]>30e3 && lep_pt[0]>27e3 && (el_trigger || mu_trigger))*(sf_total * sf_el_trigger * sf_mu_trigger )*%s'%(pt,bcut,sys),'goff')
            for b in range(1,h1d.GetNbinsX()+1):
                if h2d.GetBinContent(1,b) and h2d.GetBinContent(3,b):
                  h1d.SetBinContent(b, h2d.GetBinContent(3,b) / h2d.GetBinContent(1,b))
                  h1d.SetBinError(b, sqrt(pow(h2d.GetBinError(3,b)/h2d.GetBinContent(3,b),2) + pow(h2d.GetBinError(1,b)/h2d.GetBinContent(1,b),2))*h1d.GetBinContent(b))
            hists[(pt,sys)] = h1d.Clone(sys+"%d"%pt)
    
        coolPlot("W_charge_asym_%s_%dsys"%(bcutname,pt) ,[hists[(pt,s)] for s in ["nominal"]+systs],formats=("png","pdf","C"),folder="figures/charge_asymmetry", titlelist = ["nominal"]+[s.replace("weight_","") for s in systs] , yrangeratio=[0.9,1.1])
    coolPlot("W_charge_asym_"+bcutname ,[hists[(p,"nominal")] for p in pts],formats=("png","pdf"),folder="figures/charge_asymmetry", titlelist = ["jet p_{T} > %d GeV"%p for p in pts],plotratio=False )

