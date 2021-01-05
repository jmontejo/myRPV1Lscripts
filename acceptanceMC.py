import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--min-jets", type=int, default=4)
parser.add_argument("--max-jets", type=int, default=15)
parser.add_argument("--pt", action="append",default=[])
parser.add_argument("--btagger", default='77')
parser.add_argument("--cut", default="")
parser.add_argument("--fast", action="store_true")
parser.add_argument("--cutname", default="")
parser.add_argument("--pack", help="Run only this pack, default is all")
opts = parser.parse_args()
opts.pt = [int(x) for x in opts.pt]

import ROOT as ROOT
from SWup.coolPlot import coolPlot
import math, glob, sys
from collections import OrderedDict

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
ROOT.gStyle.SetTitleSize(20,"XYZ")
ROOT.gROOT.SetBatch(1)
ROOT.TH1.SetDefaultSumw2(1)


if opts.cutname: opts.cutname = "_"+opts.cutname
jetbtag = opts.btagger #'truth'
minjets = opts.min_jets
maxjets = opts.max_jets

def printDict(corrs,L,k,x0,btagger,pt,cut):
    if not corrs or len(corrs)<=1:
        print "Not enough entries in correlation list, probably broke early due to using --fast. len(corrs)=",len(corrs)
        return
    if not btagger: btagger="70"
    pt_cut = str(pt)+cut if cut else pt
    sumerr = sum([1./cerr for c,cerr in corrs[:-1]])
    sumc   = sum([c/cerr for c,cerr in corrs[:-1]])
    corr = sumc/sumerr
    if corr<1:
        print "WARNING correlation factor smaller than one, setting to 1:",corr
        if corr<0.9:
            print "ERROR correlation factor way smaller than one, intervene:",corr
            #sys.exit(1)
        corr = "1., #%f"%corr
    block = """
    _fixedvalues['{btag}_{pt}']={{
           "fixedCorrel" : {corr},
                 "acc_L" : {L},
                 "acc_k" : {k},
                "acc_x0" :{x0},
    }}
    """.format(corr=corr,L=L,k=k,x0=x0,btag=btagger,pt=pt_cut)
    print block

packs = {
"ttV": (
    ("ttX_merged_nohf", ""),
    ("ttV_sherpa_nohf", ""),
    ("ttbar_nohf", ""),
),
"ttV_nocorr": (
    ("ttV_sherpa_nohf", ""),
    ("ttV_sherpa_nocorr_nohf", ""),
),
"Nominal": (
    ("ttbar_nohf", ""),
#    ("ttbar_nohf_allowmistag", ""),
#    ("ttbar_norecohf", ""),
#    ("ttbar_norecohf_allowmistag", ""),
),
"Rad"    : (
    ("ttbar_nohf", ""),
    ("ttbar_nohf_weight_Rad_High", ""),
    ("ttbar_nohf_weight_Rad_Low", ""),
    ),
"Syst"   : (
    ("ttbar_nohf", ""),
    ("ttbar_systME_nohf", "aMcAtNlo"),
    ("ttbar_systPS_nohf", "H7"),
    ("ttbar_nohf_btagup", ""),
    ("ttbar_nohf_btagdown",""), 
    ),
"Scales" : (
    ("ttbar_nohf", ""),
    ("ttbar_nohf_weight_scale_muR20_muF10", ""),
    ("ttbar_nohf_weight_scale_muR05_muF10", ""),
    ("ttbar_nohf_weight_shower_up", ""),
    ("ttbar_nohf_weight_shower_down", ""),
    ),
}
def nicename(name):
    name = name.replace("mc15a_","").replace("_ttbar","").replace("_ht","")
    name = name.replace("powhegpy6","Powheg+Py6")
    name = name.replace("powhegpy8","Powheg+Py8")
    name = name.replace("sherpa","Sherpa")
    name = name.replace("_radhi"," Rad High")
    name = name.replace("_radlo"," Rad Low")
    name = name.replace("_btagup"," Btag Up")
    name = name.replace("_btagdown"," Btag Down")
    name = name.replace("_nohf","")
    name = name.replace("ttX_merged","ttbar+ttV")
    name = name.replace("ttV_","ttV ")
    if "weight" in name:
        bname, wname = name.split("_weight")
        wname = wname.replace("_"," ")
        name = bname + ' ' + wname
    if "_allowmistag" in name:
        name = name.replace("_allowmistag"," include mistags")
    if "systME" in name:
        name = name.replace("systME","aMC@NLO+Py8")
    elif "systPS" in name:
        name = name.replace("systPS","Powheg+Hpp")
    else:
        name = name.replace("ttbar","ttbar Powheg+Pythia")
    return name

sigmoid = "([0]/(1+exp(-[1]*(x-[2]))))"
myf = ROOT.TF1("myf",sigmoid,minjets-0.5,maxjets+0.5)
myf.SetParameters(8.16905e-01,1.56430e-01,-3.36409e+00)

haccnils = ROOT.TH1D("haccnils","haccnils",maxjets-minjets+1,minjets-0.5,maxjets+0.5)
hcorrel = ROOT.TH1D("hcorrel","hcorrel",maxjets-minjets+1,minjets-0.5,maxjets+0.5)
hcharmfraction = ROOT.TH1D("hcharmfraction","hcharmfraction",maxjets-minjets+1,minjets-0.5,maxjets+0.5)
for pack,samples in packs.iteritems():
    if opts.pack and opts.pack!=pack: continue
    map_charmfraction = OrderedDict()
    map_correl = OrderedDict()
    map_accnils = OrderedDict()
    for sample,samplepattern in samples:
        tree = ROOT.TChain()
        samplefolder = sample.replace("_btagdown","").replace("_btagup","").replace("_allowmistag","").replace("_norecohf","").replace("_nohf","").replace("_nocorr","")
        samplefolder = samplefolder.replace("_amcatnlo","AF2").replace("_herwig","AF2")
        if "weight" in samplefolder:
            samplefolder = samplefolder[:samplefolder.find("_weight")] 
        files = glob.glob("/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/%s_mc16*/mc16_*%s*.root" % (samplefolder,    samplepattern))
        for f in files:
            print f
            treename = f.split("/")[-2]+"_Nom"
            if "ttX" in sample and "ttbar" in f: treename = treename.replace("ttX_merged","ttbar")
            if "ttX" in sample and not "ttbar" in f: treename = treename.replace("ttX_merged","ttV_sherpa")
            if opts.fast:
                tree.AddFile(f,100000,treename)
            else:
                tree.AddFile(f,ROOT.TTree.kMaxEntries,treename)
        if not tree.GetEntries():
            print "Something wrong here",sample,samplepattern,samplefolder,len(files)
            sys.exit(1)
        samplename = nicename(sample)
        haccnils.SetTitle("%s;number of jets;#epsilon_{b}" % samplename)
        hcorrel      .SetTitle("%s;number of jets;Correlation factor" % samplename)
        for jetpt in opts.pt:
            if jetpt not in map_charmfraction: map_charmfraction[jetpt] = []
            if jetpt not in map_correl: map_correl[jetpt] = []
            if jetpt not in map_accnils: map_accnils[jetpt] = []
            hbjets2d = ROOT.TH2D("hbjets2d","hbjets2d",4,-0.5,3.5,maxjets-minjets+1,minjets - 0.5, maxjets + 0.5)
            weight = "weight*xs_weight*sf_total*sf_mu_trigger*sf_el_trigger*(1+0.6*(mc_channel_number==413008))*(lep_pt[0]>27e3 && (el_trigger || mu_trigger))"
            if opts.cut:
                weight += "*"+opts.cut
            if "btagup" in sample:
                weight += "*sf_total__SYST_FT_EFF_Eigen_B_0__1up/sf_total"
            elif "btagdown" in sample:
                weight += "*sf_total__SYST_FT_EFF_Eigen_B_0__1down/sf_total"
            if "nohf" in sample:
                weight += "*(n_truth_C<2)*(n_truth_B==2)"
            if "norecohf" in sample:
                weight += "*(Sum$(jet_HadronConeExclTruthLabelID==5)<=2 && Sum$(jet_HadronConeExclTruthLabelID==4)<=1)"
            if "weight_Rad_High" in sample:
                weight += "*(weight_shower_up*weight_scale_muR05_muF05)"
            elif "weight_Rad_Low" in sample:
                weight += "*(weight_shower_down*weight_scale_muR20_muF20)"
            elif "weight" in sample:
                sysweight = sample[sample.find("weight"):]
                weight += "*(%s)"%sysweight

            #if 'truthfakeUonly' in jetbtag:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(((jet_HadronConeExclTruthLabelID==5 && rndm<0.8) || (jet_HadronConeExclTruthLabelID==0 && rndm<0.01) ) && jet_pt>%de3),2) >> hbjets2d" % (jetpt,jetpt),weight)
            #elif 'truthfakeConly' in jetbtag:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(((jet_HadronConeExclTruthLabelID==5 && rndm<0.8) || (jet_HadronConeExclTruthLabelID==4 && rndm<0.2) ) && jet_pt>%de3),2) >> hbjets2d" % (jetpt,jetpt),weight)
            #elif 'truthfake' in jetbtag:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(((jet_HadronConeExclTruthLabelID==5 && rndm<0.8) || ((jet_HadronConeExclTruthLabelID==4 || jet_HadronConeExclTruthLabelID==15) && rndm<0.2) ||(jet_HadronConeExclTruthLabelID==0 && rndm<0.01) ) && jet_pt>%de3),2) >> hbjets2d" % (jetpt,jetpt),weight)
            #elif 'truth' in jetbtag:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_HadronConeExclTruthLabelID==5),2) >> hbjets2d" % (jetpt,jetpt),weight)
            #elif 'allowmistag' in sample:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_bjet%s),2) >> hbjets2d" % (jetpt,jetpt,jetbtag),weight)
            #else:
            #    tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_bjet%s && jet_HadronConeExclTruthLabelID!=0),2) >> hbjets2d" % (jetpt,jetpt,jetbtag),weight)
            if 'allowmistag' in sample:
                tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_bjet%s),3) >> hbjets2d" % (jetpt,jetpt,jetbtag),weight)
            else:
                #tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_bjet%s && jet_HadronConeExclTruthLabelID!=0),3) >> hbjets2d" % (jetpt,jetpt,jetbtag),weight) #allow 3 btag
                tree.Draw("Sum$(jet_pt>%de3):min(Sum$(jet_pt>%de3 && jet_bjet%s),3) >> hbjets2d" % (jetpt,jetpt,jetbtag),weight) #allowmistag

            if hbjets2d.Integral()==0:
                print "Empty 2D histo", pack, sample
                continue
            correlations =[]
            for j in range(maxjets-minjets+1):

                hbjets = hbjets2d.ProjectionX(hbjets2d.GetName()+str(j),j+1,j+1)
                if not hbjets.Integral(): continue
                hbjets.Scale(1./hbjets.Integral())
                Ntotal = hbjets.Integral()
                N0acc  = hbjets.GetBinContent(1)
                N0err  = hbjets.GetBinError(1)
                N1acc  = hbjets.GetBinContent(2)
                N1err  = hbjets.GetBinError(2)
                N2acc  = hbjets.GetBinContent(3)+hbjets.GetBinContent(4)
                print hbjets.GetBinContent(3),hbjets.GetBinContent(4)
                N2err  = math.sqrt(hbjets.GetBinError(3)*hbjets.GetBinError(3)+hbjets.GetBinError(4)*hbjets.GetBinError(4))
                
                if N1acc<=0 or N2acc<=0: break
                charmfrac = hbjets.GetBinContent(4)/N2acc
                if hbjets.GetBinContent(4):
                    charmfrac_err = charmfrac*math.sqrt(pow(hbjets.GetBinError(4)/hbjets.GetBinContent(4),2)+pow(N2err/N2acc,2))
                else: charmfrac_err = 0

                #term = (2*g**3 + 5.19615*math.sqrt(4*g**3*j - g**2*h**2 - 18*g*h*j + 4*h**3 + 27*j**2) - 9*g*h + 27*j)**(1/3)
                #b = 0.264567*term - (0.419974*(3*h - g**2))/term + g/3.
                #c = g - 2*(b)
                #r = j/(b*b*c)
                if "nocorr" in sample:
                    Cbacc = 1.
                    Cbacc_err = 1.
                    accnils = math.sqrt(N2acc)
                    accnils_err = accnils/2.*N2err/N2acc
                else:
                    Cbacc = 4.*Ntotal*N2acc/((N1acc+2*N2acc)**2)
                    Cbacc_err = Cbacc*math.sqrt(pow(N2err/N2acc,2)+pow(2*math.sqrt(N1err*N1err+4*N2err*N2err)/(N1acc+2*N2acc),2))
                    accnils = (N1acc + 2* N2acc)/2.
                    accnils_err = 0.5* math.sqrt( N1err* N1err +  N2err*N2err*4)
            
                correlations.append((Cbacc,Cbacc_err))
            
                hcharmfraction.SetBinContent(j+1,charmfrac)
                hcharmfraction.SetBinError(j+1,charmfrac_err)
                hcorrel.SetBinContent(j+1,Cbacc)
                hcorrel.SetBinError(j+1,Cbacc_err)
                haccnils.SetBinContent(j+1,accnils)
                haccnils.SetBinError(j+1,accnils_err)
            if (sample=="ttbar_nohf" and not "2LSS" in opts.cutname) or sample=="ttX_merged_nohf":
                haccnils.Fit("myf")
                printDict(correlations,myf.GetParameter(0),myf.GetParameter(1),myf.GetParameter(2),opts.btagger,jetpt,opts.cutname)
                hcharmfraction.Fit("myf")
            map_charmfraction[jetpt].append( hcharmfraction.Clone(samplename+hcharmfraction.GetName()) )
            map_correl[jetpt].append( hcorrel.Clone(samplename+hcorrel.GetName()) )
            map_accnils[jetpt].append( haccnils.Clone(samplename+haccnils.GetName()) )
    
    if opts.fast: pack += "_fast"
    for jetpt in opts.pt:
        a = coolPlot(pack+"_charmfraction_pt%dbtag%s%s"%(jetpt,jetbtag,opts.cutname),map_charmfraction[jetpt],folder="figures/acceptance_correction",yrangeratio=(0.901,1.999),yrange=(0.,0.1),formats=("png","pdf"),legendcoord=(0.5,0.5,0.9,0.9),statuncertainty=True)
        del a
        a = coolPlot(pack+"_correl_pt%dbtag%s%s"%(jetpt,jetbtag,opts.cutname),map_correl[jetpt],folder="figures/acceptance_correction",yrangeratio=(0.901,1.099),yrange=(0.96,1.1),formats=("png","pdf"),legendcoord=(0.5,0.5,0.9,0.9),statuncertainty=True)
        del a
        a = coolPlot(pack+"_acc_pt%dbtag%s%s"%(jetpt,jetbtag,opts.cutname),map_accnils[jetpt],folder="figures/acceptance_correction",yrangeratio=(0.901,1.099),yrange=(0.41,1.1),formats=("png","pdf"),legendcoord=(0.5,0.5,0.9,0.9),statuncertainty=True)
        del a
    del map_correl
    del map_accnils
