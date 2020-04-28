#!/usr/bin/env python
import sys
import os
from multiprocessing import Pool
pool = Pool(1)

folder = os.getenv('SWUP_OUTPUTDIR')+"/../"

years = ["2015_2016","2017","2018","2015_2018"]
years = ["2015_2016","2017","2018"]
years = ["2015_2018"]
thevars = {
    "baseel_pt[0]": "",
    "baseel_eta[0]": "",
    "basemu_pt[0]":  "",
    "basemu_eta[0]": "",
    'mt': " -b '20,0,200' ",
    'met':  " -b '20,0,200' ",
    'dilep_m': "",
    'n_jet': "",
    'n_bjet': "",
    'num_pv': "",
    'actual_int_per_xing': "",
    'av_int_per_xing': "",
}
cuts = {
    '1Linclusive':('n_jet>=4 && jet_pt[1]>30e3','(n_lep>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
    'el':('n_jet>=4 && jet_pt[1]>30e3 && n_baseel>=1 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(n_lep>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
    'mu':('n_jet>=4 && jet_pt[1]>30e3 && n_basemu>=1 && basemu_pt[0] > Alt$(baseel_pt[0],0)','(n_lep>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
    '2LSS':       ('n_jet>=4 && jet_pt[1]>30e3','(lep_pt[0]>27e3 && lep_pt[1]>15e3 && (el_trigger || mu_trigger) && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "Same-sign leptons")
}

for year in years:
  for cutname, (bothcut, rawcut, label) in cuts.iteritems():
    tag = "_SS" if cutname=="2LSS" else ""
    configFile = '../Analysis/RPV1L/plotcfg/plotconfig_%s%s.py' % (year,tag)
    outputDir = 'figures/data_mc/%s/%s/' % (year,cutname)
    opts = " --label '%s'"%label
    cut = "(%s)*(%s)"%(bothcut,rawcut)
    if "2L" in cutname:
        samplecut = 'Fakes#0'
    else:
        samplecut = 'Fakes#(fakeWeight)*(%s)'%bothcut

    varstring = "-v "+" -v ".join([var for var in thevars.keys() if (not var.startswith("baseel") or cutname=="el") and (not var.startswith("basemu") or cutname=="mu") ] )

    command = "plot-multi.py -c rpv2l_4j20_shrink --normalize -o {outputDir} --cut '{cut}' --sample-cut '{samplecut}' {opts} -p {config} {var}".format(
        outputDir=outputDir, cut=cut, samplecut=samplecut, opts=opts, config=configFile, var=varstring)
    print command
    pool.apply_async(os.system, args=(command,))
pool.close()
pool.join()
