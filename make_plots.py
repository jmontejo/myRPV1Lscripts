#!/usr/bin/env python
import sys
import os
from multiprocessing import Pool
pool = Pool(8)

folder = os.getenv('SWUP_OUTPUTDIR')+"/../"

years = ["2015_2016","2017","2018","2015_2018"]
years = ["2015_2016","2017","2018"]
years = ["2015_2018"]
thevars = {
#    "baseel_pt[0]": "",
#    "baseel_eta[0]": "",
#    "basemu_pt[0]":  "",
#    "basemu_eta[0]": "",
#    "mu_phi[0]":  " -b '6400,-3.2,3.2'",
#    "el_phi[0]":  " -b '6400,-3.2,3.2'",
#    'mt': " -b '20,0,200' ",
#    'met':  " -b '20,0,200' ",
#    'dilep_m': " -b '20,0,400'",
#     'mu_bad': " -b '2,-0.5,1.5' ",
#     'mu_cosmic': " -b '2,-0.5,1.5' ",
#     'mu_d0sig': " -b '20,-5,5' ",
#    'jet_pt[0]': " -b '10,0,200' ",
#    'jet_pt[3]': " -b '10,0,100' ",
#    'Sum$(jet_pt)': " -b '20,0,1000' -n HT",
#    'dilep_m[0]': " -b '20,0,100'",
#    'n_jet': "",
#    'fabs(fwdjet_eta[0])': " -b '10,2.5,4.5'",
#    'Sum$(fabs(fwdjet_eta[0])<2.8)': " -b '5,-0.5,4.5' -n n_fwdjeteta28",
#    'n_fwdjet': " -b '10,-0.5,9.5'",
#    'n_fwdjet20': " -b '10,-0.5,9.5'",
#    'n_bjet': "",
#    'lep_charge[0]': " -b '3,-1.5,1.5'",
#    'n_jet*lep_charge[0]': " -b '31,-15.5,15.5' -n n_jet_times_lep_charge",
#    'minDeltaRll' : " -b '25,0,5' ",
#    'minmax_mass' : " -b '10,0,500e3'",
#    'minDeltaRlj' : " -b '25,0,2.5' ",

#    'num_pv': "",
#    'actual_int_per_xing': "",
#    'av_int_per_xing': "",

#    'calc_mbl(calc_pt(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_eta(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_phi(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_E(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),  jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2])' : "  -n mjjj -b '20,0,2000'",
#    'calc_mbl(el_pt[0],el_eta[0],el_phi[0],el_e[0],mu_pt[0],mu_eta[0],mu_phi[0],mu_e[0])': " -b '20,0,400' -n mass_emu",
#    'calc_pt(bjet_pt[0],bjet_eta[0],bjet_phi[0],bjet_e[0],bjet_pt[1],bjet_eta[1],bjet_phi[1],bjet_e[1])/1000.': " -b '30,0,600' -n pTbb",
#    'fabs(TVector2::Phi_mpi_pi(bjet_phi[0]-bjet_phi[1]))/TMath::Pi()':'-n dphibb -b "10,0,1"',
#    'fabs(bjet_eta[0]-bjet_eta[1])':'-n detabb -b "10,0,5"',
#    'sqrt(pow(TVector2::Phi_mpi_pi(bjet_phi[0]-bjet_phi[1]),2)+pow(bjet_eta[0]-bjet_eta[1],2))':'-n dRbb -b "12,0,6"',
#    'min(calc_mbl(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],bjet_pt[0],bjet_eta[0],bjet_phi[0],bjet_e[0]),calc_mbl(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],bjet_pt[1],bjet_eta[1],bjet_phi[1],bjet_e[1]))/1000.': " -b '15,0,300' -n minmbl",
#    'max(calc_mbl(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],bjet_pt[0],bjet_eta[0],bjet_phi[0],bjet_e[0]),calc_mbl(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],bjet_pt[1],bjet_eta[1],bjet_phi[1],bjet_e[1]))/1000.': " -b '15,0,300' -n maxmbl",
#   
#    "(n_baseel*5+n_basemu)": "-b '20,0.5,20.5'",
#    'subleadmt':'-b "12,0,120"',
#    'mt2':'-b "12,0,120"',
    'fabs(TVector2::Phi_mpi_pi(lep_phi[0]-lep_phi[1]))/TMath::Pi()':'-n dphileplep -b "10,0,1"',
#    'calc_S2(lep_phi[0],lep_phi[1],met_phi,jet_phi[0],jet_phi[1],jet_phi[2],jet_phi[3],Alt$(jet_phi[4],-10.))':" -n phi_variance -b '15,0,3'",
#'calc_mbl(calc_pt(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_eta(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_phi(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_E(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),          calc_pt(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),calc_eta(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),         calc_phi(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),calc_E(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]))':" -n m4j -b '20,0,2000'",
}
cuts = {
#    '1L0b':('n_jet>=4 && n_bjet==0','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
#    'el0b':('n_jet>=4 && n_bjet==0 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
#    'mu0b':('n_jet>=4 && n_bjet==0 && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
#    '1Linclusive':('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
#    'el':('n_jet>=4 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
#    'mu':('n_jet>=4 && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
#    '2LSS':       ('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "Same-sign leptons"),
#    '2LSS2b_el':       ('n_jet>=4 && n_bjet==2 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j2b electron"),
#    '2LSS2b_mu':       ('n_jet>=4 && n_bjet==2  && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j2b muon"),
#    '2LSS3b_el':       ('n_jet>=4 && n_bjet>=3 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b electron"),
#    '2LSS3b_mu':       ('n_jet>=4 && n_bjet>=3  && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b muon"),
#    '2LSS3b_elnomllveto':       ('n_jet>=4 && n_bjet>=3 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b el nomllveto"),
#    '2LSS3b':       ('n_jet>=4 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3bmll40':       ('n_jet>=4 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && Alt$(dilep_m[0],99e3)>40e3 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b mll>40"),
#    '2LSS4j1b':       ('n_jet==4 && n_bjet>=1','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS ==4j1b"),
#    '2LSS5jincl1b':       ('n_jet>=5 && n_bjet>=1','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS >=5j1b"),
    '2LSS6jincl3b':       ('n_jet>=6 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(el_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS >=6j3b"),
}

for year in years:
  for cutname, (bothcut, rawcut, label) in cuts.iteritems():
    tag = "_SS" if "2LSS" in cutname else ""
    configFile = '../Analysis/RPV1L/plotcfg/plotconfig_%s%s.py' % (year,tag)
    outputDir = 'figures/data_mc/%s/%s/' % (year,cutname)
    opts = " --label '%s'"%label
    if "2LSS3b" in cutname: opts += " --ratio2"
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
