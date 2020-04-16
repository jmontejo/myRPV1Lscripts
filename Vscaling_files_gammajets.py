#!/usr/bin/env python
import ROOT as root
import math, glob

default_production = "output/rpv1l_photon/"
parser = argparse.ArgumentParser()
parser.add_argument("--production", default=default_production)
parser.add_argument("--minjet", type=int, default=4)
parser.add_argument("--maxjet", type=int, default=15)
opts = parser.parse_args()
root.gROOT.SetBatch(1)
root.TH1.SetDefaultSumw2(1)
tree = root.TChain("CollectionTree")
for f in glob.glob("%s/data*/fetch/data-ntuple/data-ntuple/*root"%(opts.production)):
    tree.AddFile(f)
offset = 0 #cut value is hard coded, 0 == 2.45e3 (FixedCutTight)
intermediatePlots = False #Plot the fit per jet slice, not actually used

cuts = { 
    (40,None): "1",
    (60,None): "1",
    (80,None): "1",
    (20,'2j25'):  'jet_pt[1]>25e3', 
}

hdata = root.TH1F("hdata","hdata;topoETcone40 - 0.022*p_{T}^{#gamma} [GeV];Events/bin",60,-9.55,50.45)
hbkg = root.TH1F("hbkg","hbkg",60,-9.55,50.45)
hcut = root.TH1F("hcut","hcut",60,-9.55,50.45)
theTF1 = root.TF1("crystallball","[0]*ROOT::Math::crystalball_function(x, [1], [2], [3], [4])",-8,50)
hbkgfraction = root.TH1F("hbkgfraction","hbkgfraction",opts.maxjet-opts.minjet+1,opts.minjet-0.5,opts.maxjet+0.5)
hjetn = root.TH1F("hjetn","hjetn;Number of jets;Events",opts.maxjet-opts.minjet+1,opts.minjet-0.5,opts.maxjet+0.5)

def fitFcn(x, p):
            theTF1.SetParameters(p[0],p[1],p[2],p[3],p[4])
            return theTF1.Eval(x[0]) + p[5]*hbkg.GetBinContent(hbkg.FindBin(x[0]))

fcn = root.TF1("fcn",fitFcn,-15,35,6)
fcn.SetParLimits(0,1e-6,1e9)
fcn.SetParLimits(5,1e-6,1e9)
can = root.TCanvas("can")
jetns = {}
lastfit = range(fcn.GetNpar())
for (pt,addcutname), addcut in cuts.iteritems():
    ptcut = pt*1000
    fixed = False
    tree.Draw("(ph_topoetcone40-0.022*ph_pt)/1000. >> hdata"," ph_idTight && ph_trigger && ph_pt[0]>145e3 && Sum$(jet_pt > %f && jet_killedByPhoton==0 && %s ) >=4" %(ptcut,addcut))
    tree.Draw("(ph_topoetcone40-0.022*ph_pt)/1000. >> hbkg", "!ph_idTight && ph_trigger && ph_pt[0]>145e3 && Sum$(jet_pt > %f && jet_killedByPhoton==0 && %s ) >=4" %(ptcut,addcut))
    fcn.SetParameters(hdata.GetBinContent(hdata.GetMaximumBin()),-1,1,1,0,0.3)
    fcn.ReleaseParameter(5)
    fitres = hdata.Fit(fcn,'S')
    fcn.FixParameter(5,fitres.Parameter(5))
    hbkgforplot = hbkg.Clone("hbkgforplot")
    hbkgforplot.Scale(fitres.Parameter(5))
    hbkgcut = hbkgforplot.Clone("hbkgforplot")
    for i in xrange(13+offset,hbkgforplot.GetNbinsX()+1):
        hbkgcut.SetBinContent(i,0)
        isolationPlot(hdata,hbkgforplot,ptname, addnametag)
    hjetn.Reset()
    for n in range(opts.minjet,opts.maxjet+1):
        jetcut  = "==%d" % n
        jetname = "j%dex"% n
        print "Running",jetname,ptcut
        tree.Draw("(ph_topoetcone40-0.022*ph_pt)/1000. >> hdata"," ph_idTight && ph_trigger && ph_pt[0]>145e3 && Sum$(jet_pt > %f && jet_killedByPhoton==0 && %s) %s" %(ptcut,addcut,jetcut))
        tree.Draw("(ph_topoetcone40-0.022*ph_pt)/1000. >> hbkg", "!ph_idTight && ph_trigger && ph_pt[0]>145e3 && Sum$(jet_pt > %f && jet_killedByPhoton==0 && %s) %s" %(ptcut,addcut,jetcut))
        if hdata.Integral(0,12+offset)==0: break
        fcn.SetParameter(0,hdata.GetBinContent(hdata.GetMaximumBin()))
        fitres = hdata.Fit(fcn,'S') #This fit is never used, bkg fraction is fixed
        hbkgforplot = hbkg.Clone("hbkgforplot")
        hbkgforplot.Scale(fitres.Parameter(5))
        hbkgcut = hbkgforplot.Clone("hbkgforplot")
        hdatacut = hdata.Clone("hdata")
        for i in xrange(13+offset,hbkgforplot.GetNbinsX()+1):
            hbkgcut.SetBinContent(i,0)
        if intermediatePlots or fitres.Status()!=0: 
            coolPlot("ph_fit_%s%s%s" % (jetname,ptname,addnametag),[hdata,hbkgforplot,hbkgcut],folder="figures/Vjets_validation/gamma_jets",plotratio=False)
        bkgerror = root.Double(0)
        dataerror = root.Double(0)
        bkginteg = hbkgforplot.IntegralAndError(0,12+offset,bkgerror)
        datainteg = hdata.IntegralAndError(0,12+offset,dataerror)
        bkgfraction = bkginteg/datainteg
        bkgfractionerror = bkgfraction*math.sqrt(pow(bkgerror/bkginteg,2)+pow(dataerror/datainteg,2)) if bkginteg else 0
        datasub = datainteg-bkginteg
        datasuberror = math.sqrt(pow(dataerror,2)+pow(bkgerror,2))
        jetbin = int(jetcut[2:])
        hbkgfraction.SetBinContent(jetbin-opts.minjet+1,bkgfraction)
        hbkgfraction.SetBinError(jetbin-opts.minjet+1,bkgfractionerror)
        title = "njet_gammajets_data_%d"%pt
        if addcutname: title+= "_"+addcutname
        hjetn.SetTitle(title)
        hjetn.SetName(title)
        hjetn.SetBinContent(jetbin-opts.minjet+1,datasub)
        hjetn.SetBinError(jetbin-opts.minjet+1,datasuberror)
        del hbkgforplot, hbkgcut, hdatacut

    jetns[pt] = hjetn.Clone()
outfile = "figures/Vjets_validation/Vscaling_files.root"
routfile = ROOT.TFile.Open(outfile,"update")
for j in jetns.itervalues():
    j.Write()
routfile.Close()
