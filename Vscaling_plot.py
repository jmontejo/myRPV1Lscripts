#!/usr/bin/env python
import argparse
default_pts = ["20_2j30","40","60","80"]
default_add_syst = 0.002
parser = argparse.ArgumentParser()
parser.add_argument("--minjet", type=int, default=4)
parser.add_argument("--maxjet", type=int, default=15)
parser.add_argument("--add-syst", type=float, default=default_add_syst)
parser.add_argument("--sample-group", help="Sample group to plot") 
parser.add_argument("--sample", help="Individual sample plot") 
parser.add_argument("--pt", action="append", help="pT thresholds to plot") 
parser.add_argument("--onlyMC16a", action="store_true")
parser.add_argument("--ploterrorband", action="store_true")
parser.add_argument("--print-syst", action="store_true")
opts = parser.parse_args()
if not opts.pt: opts.pt = default_pts

import ROOT
import glob, os
from math import sqrt

ROOT.gROOT.LoadMacro("atlasstyle-00-03-05/AtlasStyle.C")
ROOT.gROOT.LoadMacro("atlasstyle-00-03-05/AtlasUtils.C")
ROOT.SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetLabelFont(43,"XYZ")
ROOT.gStyle.SetLabelSize(20,"XYZ")
ROOT.gStyle.SetTitleFont(43,"XYZ")
ROOT.gStyle.SetTitleSize(30,"XYZ")
ROOT.gROOT.SetBatch(1)
#ROOT.gStyle.SetLineStyleString(9,"100 20")
#ROOT.gStyle.SetLineStyleString(11,"50 12")

ROOT.TH1.SetDefaultSumw2(1)
ROOT.TVirtualFitter.SetMaxIterations(10000)

coloroffset = 2
forinternal = False

samples = {
    "gammajets"          :("Data #gamma+jets",20,3, 0, None),

    "wjets_madgraph"     :("MC W+jets (Madgraph)",27,2, 0, None),
    "wjetsMC"            :("MC W+jets",26,2, 0, None),
    "zjetsMC"            :("MC Z+jets",32,3, 0, None),

    "multibosonsMC"      :("MC VV+jets",24,1, 0, None),

    "Wt1LMC"             :("MC Wt",32,3, 0, None),
    "WtttbarMC"          :("MC ttbar+Wt",32,3, 0, ("Wt1LMC","ttbar1LMC","ttbar2LMC")), #dont rename, matches ttW
    "WtMCcommon"         :("MC Wt common fit",32,3, 0, ("Wt1LMC",)),
    "ttbarMCcommon"      :("MC ttbar common fit",32,3, 0, ("ttbar1LMC","ttbar2LMC")),

    "ttbarMC"            :("MC ttbar",32,3, 0, ("ttbar1LMC","ttbar2LMC")),
    "ttbar1LMC"          :("MC ttbar (1L)",24,3, 0, None),
    "ttbar2LMC"          :("MC ttbar (2L)",28,3, 2, None),
    "ttbar_amcatnlo"     :("MC ttbar (ME)",30,3, 0, None),
    "ttbar_herwig"       :("MC ttbar (PS)",46,3, 0, None),

    "emubjetData"        :("Data emu+bjet",21,3, 2, None),
    "ttbar2LemubMC"      :("MC ttbar (2L) emu+bjet",25,3, 2, None),
    "ttbar2LemuMC"       :("MC ttbar (2L) emu",36,3, 2, None),

    "ttWplusttbar2LSSMC" :("MC ttW+t#bar{t} fakes",46,3, 0, ("ttWMC","ttbar2LSSMC")),
    "ttWMC"              :("MC ttW",28,3, 0, None),
    "ttbar2LSSMC"        :("MC t#bar{t} fakes",30,3, 0, None),
    "dummy"              :("Dummy",32,3, 0, None),
    }

groups = {
    "gammajets" : ("gammajets","dummy","dummy","dummy"),
    "Vjets"     : ("wjetsMC","zjetsMC","wjets_madgraph","gammajets"),
    "ttbar"     : ("ttbar1LMC","ttbar2LemuMC","ttbar2LemubMC","emubjetData"),
    "ttbar2L"   : ("ttbar2LemuMC","ttbar2LemubMC","emubjetData","dummy"),
    "ttbar1L"   : ("ttbar1LMC","ttbarMC","WtttbarMC","dummy"),
    "ttbarsyst" : ("ttbarMC","ttbar_amcatnlo","ttbar_herwig","dummy"),
    "SS3L"      : ("multibosonsMC","ttWMC","ttbar2LSSMC","ttWplusttbar2LSSMC"),
    "Wtcommon"  : ("WtttbarMC","Wt1LMC","ttbarMCcommon","WtMCcommon"),
    "Wt"        : ("Wt1LMC","ttbarMC","WtttbarMC","dummy")
    }

if opts.sample_group:
    group = groups[opts.sample_group]
elif opts.sample:
    group = (opts.sample,"dummy","dummy","dummy")
    opts.sample_group = opts.sample
    
loglikelihoodfit=False
tag = opts.sample_group
tag += "_int" if forinternal else ""
if opts.pt != default_pts:
    tag += "_".join(opts.pt)
if opts.ploterrorband:
    tag += "_errorband"
if opts.add_syst!=default_add_syst:
    tag += "%f"%opts.add_syst
if opts.sample:
    tag += "_sample"
if loglikelihoodfit:
    tag += "_llp"

offset = opts.maxjet-opts.minjet+1
holder = []

iofolder = 'figures/Vjets_validation/'
infile = iofolder+"Vscaling_files.root"
samplefile = ROOT.TFile.Open(infile)

def getSampleHisto(samplename,pt,opts):
    h = None
    a, b, c, d, subsamples = samples[samplename]
    if not subsamples: subsamples = [samplename]
    for sub in subsamples:
        subweight = 1
        if sub.startswith("-"):
            sub = sub[1:]
            subweight = -1
        mc16part = "mc16a" if opts.onlyMC16a else "mc16"
        if "Data" in sub:
            mc16part = "data15" if opts.onlyMC16a else "data"
        histoname = "njet_%s_%s_%s"%(sub,mc16part,pt)
        if histoname == "njet_Wt1LMC_mc16_20_2j30":
            histoname = histoname.replace("Wt1LMC","WtMC")
        if "gammajets" in sub:
            histoname = "njet_%s_%s"%(sub,pt)
        if not h:
            tmp = samplefile.Get(histoname)
            if tmp:
                h = tmp.Clone(samplename)
        else:
            if sub == "ttbar2LMC": #shift by two jets
                tmp1L = h.Clone()
                tmp2L = samplefile.Get(histoname)
                for ib in range(tmp1L.GetNbinsX()):
                    tmp1L.SetBinContent(ib+1, tmp2L.GetBinContent(ib+3))
                    tmp1L.SetBinError(ib+1, tmp2L.GetBinError(ib+3))
                h.Add( tmp1L , subweight)
            else:
                h.Add( samplefile.Get(histoname) , subweight)
    return h

def main(m):
    firstsample = True
    maxsyst = {}
    maxstatsyst = {}
    for isample,samplename in enumerate(group):

        legendname, imarker, ratiospace, sampleoffset, subsamples = samples[samplename]
        firstpt = True
        usedsample = False
        for ipt, pt in enumerate(opts.pt):
            if not pt in maxsyst: maxsyst[pt] = {}
            if not pt in maxstatsyst: maxstatsyst[pt] = {}
            if len(pt)<=2: pt3lep = pt+"_3lep"
            else: pt3lep = pt[:3]+"3lep"+pt[3:]
            same = "" if firstpt else "same"
            globalsame = "" if firstpt and firstsample else "same"

            h = getSampleHisto(samplename,pt,opts)

            if not h: 
                print "MISSING: ",samplename,pt
                continue
            else: print "Will process",samplename,pt
            #h.SetDirectory(0)
            if not opts.sample and "wjetsMC" in samplename:       h = extendVjets(h, getSampleHisto(samplename.replace("wjets","zjets"),pt,opts))
            if not opts.sample and "zjetsMC" in samplename:       h = extendVjets(h, getSampleHisto(samplename.replace("zjets","wjets"),pt,opts))
            if not opts.sample and "ttbarMCcommon" in samplename: h = extendVjets(h, getSampleHisto(samplename.replace("ttbar","Wt"),pt,opts))
            if not opts.sample and "WtMCcommon" in samplename:    h = extendVjets(h, getSampleHisto(samplename.replace("Wt","ttbar"),pt,opts))
            holder.append(h)
            for b in range(h.GetNbinsX()):
                if h.GetBinContent(b+1) < 0.01: 
                    h.SetBinContent(b+1,0)
                    h.SetBinError(b+1,0)
                if opts.add_syst:
                    h.SetBinError(b+1,max(h.GetBinError(b+1), opts.add_syst*h.GetBinContent(b+1)))
                #h.SetBinError(b+1,max(h.GetBinError(b+1), sqrt(h.GetBinContent(b+1))))
            h.SetMarkerStyle(imarker)
            h.SetLineColor(ipt+coloroffset+1*(ipt>=3))
            h.SetMarkerColor(ipt+coloroffset+1*(ipt>=3))
            h.SetMinimum(0.02)
            h.SetMaximum(1e8)
            m.dummy.cd()
            m.fitfcn.SetParLimits(1,0,3)
            m.fitfcn.SetParLimits(2,0,3)
            loglikelihoodfit=False
            if "tt" in samplename or "Wt" in samplename or "emu" in samplename:
                m.fitfcn.ReleaseParameter(3)
                m.fitfcn.SetParLimits(3,-3.0,3.2)
                m.fitfcn.SetParLimits(2,0,3.0)
                if not "common" in samplename:
                    m.fitfcn.FixParameter(4,0)
                else:
                    m.fitfcn.ReleaseParameter(4)
                if "ttW" in samplename:
                    m.fitfcn.SetParameters(h.GetBinContent(h.GetMaximumBin()), 0.11, 0.8, -2.9, h.GetBinContent(h.GetMaximumBin()))
                    #m.fitfcn.FixParameter(3,1)
                elif "ttbar_herwig" in samplename and "20" in pt:
                    m.fitfcn.SetParameters(h.GetBinContent(h.GetMaximumBin()), 0.17, 0.2, -2.8, h.GetBinContent(h.GetMaximumBin()))
                elif "ttbar_herwig" in samplename:
                    m.fitfcn.SetParameters(h.GetBinContent(h.GetMaximumBin()), 0.17, 0.2, -0.8, h.GetBinContent(h.GetMaximumBin()))
                else:
                    m.fitfcn.SetParameters(h.GetBinContent(h.GetMaximumBin()), 0.17, 0.6, -1.1, h.GetBinContent(h.GetMaximumBin()))
            else:
                m.fitfcn.SetParameters(h.GetBinContent(h.GetMaximumBin()), 0.1, 1.0, 1, h.GetBinContent(h.GetMaximumBin()))
                m.fitfcn.FixParameter(3,1)
                if "wjets" in samplename or "zjets" in samplename:
                    m.fitfcn.ReleaseParameter(4)
                else:
                    m.fitfcn.FixParameter(4,0)
            if "ttbar2LSSMC" in samplename or "ttWMC" in samplename  or ("madgraph" in samplename and "80" in pt):
                loglikelihoodfit=True
            if loglikelihoodfit:
                print "LOGLIKELIHOOD FIT ---------------------------"
                fitres = h.Fit("fitfcn",'S,WL')
            else:
                fitres = h.Fit("fitfcn",'S')
            fitband = h.Clone()
            ROOT.TVirtualFitter.GetFitter().GetConfidenceIntervals(fitband,0.68) #Set CL
            fitband.SetFillColorAlpha(ipt+coloroffset+1*(ipt>=3),0.5)
            if opts.sample:
                m.dummy.cd()
            else:
                m.toppad.cd()

            f = h.GetFunction("fitfcn")
            #f.SetLineColor(ROOT.kGray+1)
            f.SetLineColor(ipt+coloroffset+1*(ipt>=3))
            f.SetLineStyle(2)
            h.GetXaxis().SetRangeUser(opts.minjet-0.5-sampleoffset,opts.maxjet+0.5-sampleoffset)
            h.GetXaxis().SetTitleOffset(1.8)
            h.GetYaxis().SetTitle("Events")
            for b in range(1,h.GetNbinsX()+1):
                h.GetXaxis().SetBinLabel(b,str(int(h.GetBinCenter(b))))
            h.DrawCopy("func,E,P"+globalsame)
            if opts.ploterrorband:
                fitband.DrawCopy("e5 same")
            if opts.sample:
                if ipt==3: m.bottompad1.cd()
                if ipt==2: m.bottompad2.cd()
                if ipt==1: m.bottompad3.cd()
                if ipt==0: m.bottompad4.cd()
            else:
                if isample==3: m.bottompad1.cd()
                if isample==2: m.bottompad2.cd()
                if isample==1: m.bottompad3.cd()
                if isample==0: m.bottompad4.cd()

    
            ratio = h.Clone()
            ratio.Divide(f)
            ratio.GetYaxis().SetRangeUser(0.4,1.6)
            ratio.GetXaxis().SetTitleOffset(5)
            shortname = legendname.replace("Data ","").replace("MC ","")
            ratio.GetYaxis().SetTitle(shortname+" / Fit"+" "*ratiospace)
            ratio.GetYaxis().SetTitleOffset(2.5)
            ratio.GetYaxis().SetTitleSize(17)
            ratio.GetYaxis().SetNdivisions(505)
            ratio.SetMarkerColor(ipt+coloroffset+1*(ipt>=3))
            ratio.DrawCopy("hist,E,P"+("" if opts.sample else same))
            if fitres.Status()!=0 and forinternal:
                m.fittext.DrawLatexNDC(0.5,0.8-0.1*ipt,"#color[%d]{Failed fit}"%(ipt+coloroffset+1*(ipt>=3)))
            ratioband = fitband.Clone()
            ratioband.Divide(f)
            if opts.ploterrorband:
                ratioband.DrawCopy("e5 same")
            if firstpt or opts.sample:
                line = ROOT.TLine(ratio.GetBinLowEdge(1),1,ratio.GetBinLowEdge(ratio.GetNbinsX()+1),1)
                line.SetLineColor(ROOT.kGray)
                line.Draw("same")
                m.lines.append(line)
            if opts.print_syst:
                print "Syst",samplename, pt
                for b in range(1,ratio.GetNbinsX()+1):
                    njet = b+3 #assume all start from 4 jet, include offset for dilepton
                    if njet > opts.maxjet: break
                    syst = abs(1-ratio.GetBinContent(b))
                    print "%d : %.3f" %(njet,syst)
                    maxsyst[pt][njet] = max(maxsyst[pt].get(njet,0), syst)
                print "Syst+stat",samplename, pt
                for b in range(1,ratio.GetNbinsX()+1):
                    njet = b+3 #assume all start from 4 jet, include offset for dilepton
                    if njet > opts.maxjet: break
                    syst = abs(1-ratio.GetBinContent(b))
                    try: stat =  ratio.GetBinError(b)/ratio.GetBinContent(b)
                    except: stat = 1
                    print "%d : %.3f" %(njet,max(stat,syst))
                    maxstatsyst[pt][njet] = max(maxstatsyst[pt].get(njet,0), max(stat,syst))
            #-------------------------------------
            if opts.sample:
                m.toppad.cd()
            else:
                if isample==3: m.pubpad1.cd()
                if isample==2: m.pubpad2.cd()
                if isample==1: m.pubpad3.cd()
                if isample==0: m.pubpad4.cd()
            consecutiveratio = h.Clone()
            for b in range(consecutiveratio.GetNbinsX()+1):
                yield1 = consecutiveratio.GetBinContent(b)
                yield2 = consecutiveratio.GetBinContent(b+1)
                if not yield1 or not yield2:  
                    consecutiveratio.SetBinContent(b,0)
                    consecutiveratio.SetBinError(b,0)
                    continue
                error1 = consecutiveratio.GetBinError(b)
                error2 = consecutiveratio.GetBinError(b+1)
                consecutiveratio.SetBinContent(b,yield2/yield1)
                consecutiveratio.SetBinError(b,sqrt(pow(error1/yield1,2)+pow(error2/yield2,2))*yield2/yield1)
            yaxis = consecutiveratio.GetYaxis()
            xaxis = consecutiveratio.GetXaxis()
            if "Wt" in samplename or "tt" in samplename or "emu" in samplename or opts.sample:
                yaxis.SetRangeUser(0. if isample==3 else 0.01,1.29)
            else:
                yaxis.SetRangeUser(0. if isample==3 else 0.01,0.49)
            yaxis.SetTitle("r(j) "+shortname+ " "*ratiospace)
            yaxis.SetTitleSize(0.8* yaxis.GetTitleSize())
            #xaxis.SetTitleSize(0.03)
            if opts.sample:
                xaxis.SetTitleOffset(2)
            else:
                xaxis.SetTitleOffset(4)
            xaxis.SetRangeUser(opts.minjet-0.5-sampleoffset,opts.maxjet-0.5-sampleoffset)
            consecutiveratio.SetMarkerColor(ipt+coloroffset+1*(ipt>=3))
            consecutiveratio.SetLineColor(ipt+coloroffset+1*(ipt>=3))
            yaxis.SetNdivisions(505)
            for b in range(1,h.GetNbinsX()+1):
                bcenter = h.GetBinCenter(b)
                xaxis.SetBinLabel(b,"%d/%d"%(bcenter+1,bcenter))
            xaxis.SetTitle("(N_{jets}+1)/N_{jets}")
            consecutiveratio.DrawCopy("E,P,hist"+same)
            m.ratiofcn.SetParameters(f.GetParameter(1),f.GetParameter(2),f.GetParameter(3))
            m.ratiofcn.SetLineStyle(2)
            m.ratiofcn.SetLineColor(ipt+coloroffset+1*(ipt>=3))
            #m.ratiofcn.SetLineColor(ROOT.kGray+1)
            errorgraph = GetErrorGraph(m.ratiofcn)
            holder.append(errorgraph)
            m.ratiofcn.DrawCopy("same")
            errorgraph.SetFillColorAlpha(ipt+coloroffset+1*(ipt>=3),0.5)
            if opts.ploterrorband:
                errorgraph.Draw("same4")
            if fitres.Status()!=0 and forinternal:
                m.fittext.DrawLatexNDC(0.5,0.8-0.1*ipt,"#color[%d]{Failed fit}"%(ipt+coloroffset+1*(ipt>=3)))
            if firstsample:
                m.legendpt.AddEntry(h,"jet p_{T} > %s GeV" % pt.split("_")[0],"l")
                print "AddEntry",pt
            firstpt = False
            usedsample = True
        if usedsample: 
            firstsample = False
            hsample = h.Clone(h.GetName()+"samp")
            hsample.SetMarkerColor(1)
            holder.append(hsample)
            m.legendsamp.AddEntry(hsample,legendname,"p")
    m.pubpad4.cd()
    addLegendToPad(m)
    if not opts.sample:
        m.pubcanvas.SaveAs(iofolder+"Vscaling_jetn_ratios_%s.pdf"%tag)
    m.toppad.cd()
    addLegendToPad(m,first=False)
    if not opts.sample:
        m.toppad.SetLogy(1)
    m.intcanvas.SaveAs(iofolder+"Vscaling_jetn_%s.pdf"%tag)
    if opts.print_syst:
        for pt, syst in maxsyst.iteritems():
            print "Max syst",pt
            for njet, jsyst in syst.iteritems():
                print "\t\t%d : %.3f," %(njet, jsyst)
        for pt, statsyst in maxstatsyst.iteritems():
            print "Max stat+syst",pt
            for njet, jstatsyst in statsyst.iteritems():
                print "\t\t%d : %.3f," %(njet, jstatsyst)


class M(object):
  def __init__(self, sample):
    thefcn1 = "[0] * pow([1],x-{minjet}) * tgamma([2]/[1] + [3] + x)*tgamma([3]+{minjet})/( tgamma({minjet} + [2]/[1] + [3]) * tgamma([3] + x) )".format(minjet=opts.minjet)
    thefcn2 = "[4] * pow([1],x-{minjet}-{offset}) * tgamma([2]/[1] + [3] + x-{offset})*tgamma([3]+{minjet})/( tgamma({minjet} + [2]/[1] + [3]) * tgamma([3] + x-{offset}) )".format(minjet=opts.minjet,offset=offset)
    self.fitfcn = ROOT.TF1("fitfcn","(x<%d-0.5) ? %s : %s"%(offset+opts.minjet,thefcn1,thefcn2),opts.minjet-0.5-2,offset+opts.maxjet+0.5)
    self.ratiofcn = ROOT.TF1("ratiofcn","[0] + [1]/(x+[2])",opts.minjet-0.5-2,opts.maxjet+0.5)
    self.lines = []
    
    activepanels = 4 if opts.sample else 4- group.count("dummy")

    self.dummy = ROOT.TCanvas("dummy","dummy", 800, 800 )
    self.intcanvas = ROOT.TCanvas("jetn","jetn", 800, 1000 )
    self.pubcanvas = ROOT.TCanvas("pubjetn","pubjetn", 800, 1000 )

    self.toppad     = ROOT.TPad("toppad",     "toppad  ",   0.0, 0.45, 1., 1., 0, 0, 0 )
    self.bottompad1 = ROOT.TPad("bottompad1", "bottompad1", 0.0, 0.  , 1., 0.15, 0, 0, 0) 
    self.bottompad2 = ROOT.TPad("bottompad2", "bottompad2", 0.0, 0.15, 1., 0.25, 0, 0, 0) 
    self.bottompad3 = ROOT.TPad("bottompad3", "bottompad3", 0.0, 0.25, 1., 0.35, 0, 0, 0) 
    self.bottompad4 = ROOT.TPad("bottompad4", "bottompad4", 0.0, 0.35, 1., 0.45, 0, 0, 0) 
    if activepanels == 3:
        self.bottompad1 = ROOT.TPad("bottompad1", "bottompad1", 0.0, 0.  , 1., 0.10, 0, 0, 0) 
        self.bottompad2 = ROOT.TPad("bottompad2", "bottompad2", 0.0, 0.10, 1., 0.25, 0, 0, 0) 
    elif activepanels == 1:
        self.toppad     = ROOT.TPad("toppad",     "toppad  ",   0.0, 0.25, 1., 1., 0, 0, 0 )
        self.bottompad1 = ROOT.TPad("bottompad1", "bottompad1", 0.0, 0.  , 1., 0., 0, 0, 0) 
        self.bottompad2 = ROOT.TPad("bottompad2", "bottompad2", 0.0, 0.  , 1., 0., 0, 0, 0) 
        self.bottompad3 = ROOT.TPad("bottompad3", "bottompad3", 0.0, 0.  , 1., 0., 0, 0, 0) 
        self.bottompad4 = ROOT.TPad("bottompad4", "bottompad4", 0.0, 0.00, 1., 0.25, 0, 0, 0) 

    self.intcanvas.cd()
    self.toppad.Draw()
    self.toppad.cd()
    self.toppad.SetLeftMargin(0.20)
    self.toppad.SetBottomMargin(0.)
    if opts.sample:
        self.toppad.SetBottomMargin(0.2)
    self.intcanvas.cd()
    self.bottompad1.Draw()
    self.bottompad1.cd()
    self.bottompad1.SetLeftMargin(0.20)
    self.bottompad1.SetTopMargin(0.)
    self.bottompad1.SetBottomMargin(0.3333)
    self.intcanvas.cd()
    self.bottompad2.Draw()
    self.bottompad2.cd()
    self.bottompad2.SetLeftMargin(0.20)
    self.bottompad2.SetTopMargin(0.)
    self.bottompad2.SetBottomMargin(0.0)
    if activepanels == 3:
        self.bottompad2.SetBottomMargin(0.3333)
    self.intcanvas.cd()
    self.bottompad3.Draw()
    self.bottompad3.cd()
    self.bottompad3.SetLeftMargin(0.20)
    self.bottompad3.SetTopMargin(0.)
    self.bottompad3.SetBottomMargin(0.0)
    self.intcanvas.cd()
    self.bottompad4.Draw()
    self.bottompad4.cd()
    self.bottompad4.SetLeftMargin(0.20)
    self.bottompad4.SetTopMargin(0.)
    self.bottompad4.SetBottomMargin(0.0)
    if activepanels == 1:
        self.bottompad4.SetBottomMargin(0.3333)
    self.intcanvas.cd()
    self.legendpt = ROOT.TLegend( 0.47,0.7,0.66,0.9)
    self.legendpt.SetFillStyle(0)
    self.legendpt.SetLineColor(0)
    self.legendpt.SetBorderSize(0)
    self.legendpt.SetShadowColor(10)
    self.legendsamp = ROOT.TLegend( 0.66,0.65,0.93,0.9)
    self.legendsamp.SetFillStyle(0)
    self.legendsamp.SetLineColor(0)
    self.legendsamp.SetBorderSize(0)
    self.legendsamp.SetShadowColor(10)

    self.pubpad1 = ROOT.TPad("pubpad1", "pubpad1", 0.0, 0.  , 1., 0.25, 0, 0, 0) 
    self.pubpad2 = ROOT.TPad("pubpad2", "pubpad2", 0.0, 0.25, 1., 0.45, 0, 0, 0) 
    self.pubpad3 = ROOT.TPad("pubpad3", "pubpad3", 0.0, 0.45, 1., 0.65, 0, 0, 0) 
    self.pubpad4 = ROOT.TPad("pubpad4", "pubpad4", 0.0, 0.65, 1., 1.  , 0, 0, 0) 
    if activepanels == 3:
        self.pubpad1 = ROOT.TPad("pubpad1", "pubpad1", 0.0, 0.  , 1., 0.20, 0, 0, 0) 
        self.pubpad2 = ROOT.TPad("pubpad2", "pubpad2", 0.0, 0.20, 1., 0.45, 0, 0, 0) 
    self.pubcanvas.cd()
    self.pubpad1.Draw()
    self.pubpad1.cd()
    self.pubpad1.SetLeftMargin(0.20)
    self.pubpad1.SetTopMargin(0.)
    self.pubpad1.SetBottomMargin(0.3333)
    self.pubcanvas.cd()
    self.pubpad2.Draw()
    self.pubpad2.cd()
    self.pubpad2.SetLeftMargin(0.20)
    self.pubpad2.SetTopMargin(0.)
    self.pubpad2.SetBottomMargin(0.0)
    if activepanels == 3:
        self.pubpad2.SetBottomMargin(0.3333)
    self.pubcanvas.cd()
    self.pubpad3.Draw()
    self.pubpad3.cd()
    self.pubpad3.SetLeftMargin(0.20)
    self.pubpad3.SetTopMargin(0.)
    self.pubpad3.SetBottomMargin(0.0)
    self.pubcanvas.cd()
    self.pubpad4.Draw()
    self.pubpad4.cd()
    self.pubpad4.SetLeftMargin(0.20)
    self.pubpad4.SetTopMargin(0.4)
    self.pubpad4.SetBottomMargin(0.0)
    if activepanels == 1:
        self.pubpad4.SetBottomMargin(0.3333)
    self.pubcanvas.cd()

    self.fittext = ROOT.TLatex()
    self.fittext.SetNDC()
    self.fittext.SetTextSize(20)
    self.fittext.SetTextFont(43)


def addLegendToPad(m,first=True):
    m.legendpt.Draw()
    if first:
        dummyf = ROOT.TF1()
        dummyf.SetLineStyle(2)
        dummyf.SetLineWidth(2)
        dummyf.SetLineColor(ROOT.kGray+1)
        m.legendsamp.AddEntry(dummyf,"Parameterized fit","l")
        holder.append(dummyf)
        
    m.legendsamp.Draw()
    atl = ROOT.TLatex(0.24,0.84,"ATLAS Internal")
    atl.SetNDC()
    atl.SetTextFont(72)
    atl.SetTextSize(0.78 * atl.GetTextSize())
    atl.Draw("same")
    lumi = ROOT.TLatex(0.24,0.79,"#sqrt{s}=13 TeV, 3.2 - 14.8 fb^{-1}")
    lumi.SetNDC()
    lumi.SetTextFont(72)
    lumi.SetTextSize(0.75 * atl.GetTextSize())
    lumi.Draw("same")

def GetErrorGraph(f):
    fitter = ROOT.TVirtualFitter.GetFitter()
    grapherrors = ROOT.TGraphErrors(opts.maxjet-opts.minjet+2)
    for i in range(grapherrors.GetN()): #compute one bin before and one after to make it smoother
        jet = max(opts.minjet-0.5, i+opts.minjet-1)
        #jet = min(jet, opts.maxjet-0.5)
        error = fitter.GetCovarianceMatrixElement(1,1) + fitter.GetCovarianceMatrixElement(2,2)/pow(jet+1,2) + 2*fitter.GetCovarianceMatrixElement(1,2)/(jet+1)
        grapherrors.SetPoint(i, jet, f.Eval(jet))
        grapherrors.SetPointError(i, 0, sqrt(error))
    return grapherrors

def extendVjets(h1,h2,jetoffset=0):
    if not h2: jetoffset=0
    h = ROOT.TH1D(h1.GetName()+"ext",h1.GetTitle()+"ext",offset+opts.maxjet-opts.minjet+1,opts.minjet-0.5,offset+opts.maxjet+0.5)
    h.SetDirectory(0)
    for b in range(h1.GetNbinsX()):
        h.SetBinContent(b+1+jetoffset,h1.GetBinContent(b+1))
        h.SetBinError(b+1+jetoffset,h1.GetBinError(b+1))
        if h2:
            h.SetBinContent(b+1+offset,h2.GetBinContent(b+1))
            h.SetBinError(b+1+offset,h2.GetBinError(b+1))
    return h

if __name__ == "__main__": 
    m = M(opts.sample)
    main(m)
