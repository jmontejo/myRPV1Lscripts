#!/usr/bin/env python
import sys
import os
from multiprocessing import Pool
pool = Pool(8)

folder = os.getenv('SWUP_OUTPUTDIR')+"/../"

years = ["2015_2016","2017","2018","2015_2018"]
years = ["2015_2016","2017","2018"]
thevars = {
#    "baseel_pt[0]": "",
#    "baseel_eta[0]": "",
#    "basemu_pt[0]":  "",
#    "basemu_eta[0]": "",
#    'mt': " -b '20,0,200' ",
#    'met':  " -b '20,0,200' ",
#    'dilep_m': "",
#    'n_jet': "",
#    'n_bjet': "",
    'n_jet*lep_charge[0]': " -b '31,-15.5,15.5' -n n_jet_times_lep_charge",
#    'num_pv': "",
#    'actual_int_per_xing': "",
#    'av_int_per_xing': "",
}
cuts = {
    '1L0b':('n_jet>=4 && n_bjet==0','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
    'el0b':('n_jet>=4 && n_bjet==0 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
    'mu0b':('n_jet>=4 && n_bjet==0 && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
#    '1Linclusive':('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
#    'el':('n_jet>=4 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
#    'mu':('n_jet>=4 && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
#    '2LSS':       ('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "Same-sign leptons")
}

for year in years:
  for cutname, (bothcut, rawcut, label) in cuts.iteritems():
    tag = "_SS" if cutname=="2LSS" else ""
    configFile = '../Analysis/RPV1L/plotcfg/plotconfig_%s%s.py' % (year,tag)
    outputDir = 'figures/data_mc/%s/%s/' % (year,cutname)
    opts = " --label '%s'"%label
    cut = "(%s)*(%s)"%(bothcut,rawcut)

    for varname, varextra in thevars.iteritems():
        if varname.startswith("baseel_") and not cutname=="el": continue
        if varname.startswith("basemu_") and not cutname=="mu": continue
        if "2L" in cutname or "dilep_m" in varname: 
            samplecut = 'Fakes#0'
        else:
            samplecut = 'Fakes#(fakeWeight)*(%s)'%bothcut
        if os.path.exists(outputDir+"/"+varname.replace("[","").replace("]","")+".png"): 
            print "Exists", outputDir+"/"+varname+".png"
            continue
        command = "plot.py -c rpv2l_4j20_shrink --normalize -o {outputDir} --cut '{cut}' --sample-cut '{samplecut}' {opts} -p {config} \'{var}\' {varextra}".format(
            outputDir=outputDir, cut=cut, samplecut=samplecut, opts=opts, config=configFile, var=varname, varextra=varextra)
        print command
        pool.apply_async(os.system, args=(command,))
pool.close()
pool.join()
