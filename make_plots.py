#!/usr/bin/env python
import sys
import os
from multiprocessing import Pool
pool = Pool(8)
from time import sleep

folder = os.getenv('SWUP_OUTPUTDIR')+"/../"

years = ["2015_2016","2017","2018","2015_2018"]
years = ["2015_2016","2017","2018"]
years = ["2015_2018"]
years = ["2015_2016"]
thevars = {
#    'n_jet': "",
    'n_bjet': "",
#    'mt': " -b '20,0,200' ",
#    'met':  " -b '20,0,200' ",
#    "lep_pt[0]": "",
#    "abs(lep_eta[0])": "  -b '20,-2.5,2.5' ",
#    "lep_pt[1]": " -b '20,0,100' ",
#    "lep_eta[1]": "",
#    "Max$(abs(lep_eta))": " -b '20,-2.5,2.5' ",
#    'dilep_m[0]': " -b '20,0,200'", #low mass
#    '(dilep_m[0]<101e3 && dilep_m[0]>81e3)*5 + n_lep': " -b '10,0.5,10.5' -n dilep_plus_nlep",
#    "basemu_pt[0]":  "",
#    "basemu_eta[0]": "",
#    "mu_phi[0]":  " -b '6400,-3.2,3.2'",
#    "el_phi[0]":  " -b '6400,-3.2,3.2'",
#     'mu_bad': " -b '2,-0.5,1.5' ",
#     'mu_cosmic': " -b '2,-0.5,1.5' ",
#     'mu_d0sig': " -b '20,-5,5' ",
#    'jet_pt[0]': " -b '10,0,200' ",
#    'jet_pt[3]': " -b '10,0,100' ",
#    'Sum$(jet_pt)': " -b '20,0,1000' -n HT",
#    'dilep_m': " -b '20,0,400'",
#    'Max$(lep_iplv)': " -b '10,0,1' -n max_iplv",
#    'MaxIf$(lep_iplv,lep_is_muon==1)': " -b '10,0,1' -n max_iplv_mu",
#    'MaxIf$(lep_iplv,lep_is_muon==0)': " -b '10,0,1' -n max_iplv_el",
#    'network_output_2020_06_02_checkpoints_checkpoint_4j':  ' -b "12,0,1"',
#    'max_min_dphi(jet_phi[0],jet_phi[1],jet_phi[2],jet_phi[3],Alt$(jet_phi[4],9),Alt$(jet_phi[5],9),Alt$(jet_phi[6],9),Alt$(jet_phi[7],9))': " -b '10,0,4' -n max_min_dphi",
#    'network_output_2020_09_02_checkpoints_checkpoint_5j':  ' -b "6,0,1"',
#    'network_output_2020_09_02_checkpoints_checkpoint_6j':  ' -b "6,0,1"',
#    'network_output_2020_09_02_checkpoints_checkpoint_7j':  ' -b "6,0,1"',
#    'fabs(fwdjet_eta[0])': " -b '10,2.5,4.5'",
#    'Sum$(fabs(fwdjet_eta[0])<2.8)': " -b '5,-0.5,4.5' -n n_fwdjeteta28",
#    'n_fwdjet': " -b '10,-0.5,9.5'",
#    'n_fwdjet20': " -b '10,-0.5,9.5'",
#    'lep_charge[0]': " -b '3,-1.5,1.5'",
#    'n_mu': " -b '3,-0.5,2.5'",
#    'n_cosmics': " -b '3,-0.5,2.5'",
#    'MinIf$(jet_btagbin,jet_bjet)': " -b '6,-0.5,5.5' ",
#    'MaxIf$(jet_btagbin,!jet_bjet)': " -b '6,-0.5,5.5' ",
#    'MaxIf$(jet_btagbin,jet_bjet)': " -b '6,-0.5,5.5' ",
#    'Sum$(lep_charge)': " -b '9,-4.5,4.5'",
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
#    'fabs(TVector2::Phi_mpi_pi(lep_phi[0]-lep_phi[1]))/TMath::Pi()':'-n dphileplep -b "10,0,1"',
#    'calc_S2(lep_phi[0],lep_phi[1],met_phi,jet_phi[0],jet_phi[1],jet_phi[2],jet_phi[3],Alt$(jet_phi[4],-10.))':" -n phi_variance -b '15,0,3'",
#'calc_mbl(calc_pt(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_eta(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_phi(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),calc_E(jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1]),          calc_pt(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),calc_eta(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),         calc_phi(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]),calc_E(jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3]))':" -n m4j -b '20,0,2000'",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3])" : " -b '100,0,200e3' -n minmax_mlj_short_upto4j_fine",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3])" : " -b '20,0,300e3' --no-data -n minmax_mlj_short_upto4j_nodata",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3])" : " -b '20,0,200e3' -n minmax_mlj_short_upto4j",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3],Alt$(jet_pt[4],0),Alt$(jet_eta[4],0),Alt$(jet_phi[4],0),Alt$(jet_e[4],0))" : " -b '20,0,200e3' -n minmax_mlj_short_upto5j",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3],Alt$(jet_pt[4],0),Alt$(jet_eta[4],0),Alt$(jet_phi[4],0),Alt$(jet_e[4],0),Alt$(jet_pt[5],0),Alt$(jet_eta[5],0),Alt$(jet_phi[5],0),  Alt$(jet_e[5],0))" : " -b '20,0,200e3' -n minmax_mlj_short_upto6j",
#    "calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],lep_pt[1],lep_eta[1],lep_phi[1],lep_e[1],MinIf$(jet_pt[0],jet_bjet[0]),MinIf$(jet_eta[0],jet_bjet[0]),MinIf$(jet_phi[0],jet_bjet[0]),MinIf$(jet_e[0],jet_bjet[0]),MinIf$(jet_pt[1],jet_bjet[1]),MinIf$(jet_eta[1],jet_bjet[1]),MinIf$(jet_phi[1],jet_bjet[1]),MinIf$(jet_e[1],jet_bjet[1]),MinIf$(jet_pt[2],jet_bjet[2]),MinIf$(jet_eta[2],jet_bjet[2]),MinIf$(jet_phi[2],jet_bjet[2]),MinIf$(jet_e[2],jet_bjet[2]),MinIf$(jet_pt[3],jet_bjet[3]),MinIf$(jet_eta[3],jet_bjet[3]),MinIf$(jet_phi[3],jet_bjet[3]),MinIf$(jet_e[3],jet_bjet[3]),MinIf$(jet_pt[4],jet_bjet[4]),MinIf$(jet_eta[4],jet_bjet[4]),MinIf$(jet_phi[4],jet_bjet[4]),MinIf$(jet_e[4],jet_bjet[4]),MinIf$(jet_pt[5],jet_bjet[5]),MinIf$(jet_eta[5],jet_bjet[5]),MinIf$(jet_phi[5],jet_bjet[5]),  MinIf$(jet_e[5],jet_bjet[5]))" : " -b '20,0,300e3' -n minmax_mlb",
}
cuts = {
    'ZZ':('n_jet>=4','(lep_pt[0]>27e3 && n_el>=1 && n_mu>=1 && n_baseel>=2 && n_basemu>=2 && (dilep_m[0]<101e3 && dilep_m[0]>81e3) && n_lep>=3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
#    '1Linclusive':('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched )*(sf_total*sf_mu_trigger*sf_el_trigger)',"Single lepton"),
#    'el':('n_jet>=4 && (!lep_is_muon[0])','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger)',"Electron channel"),
#    'mu':('n_jet>=4 && lep_is_muon[0]   ','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger)',"Muon channel"),
#    '2LSS':       ('n_jet>=4','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "Same-sign leptons"),
#    '2LSS3b':     ('n_jet>=4 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3b4j':     ('n_jet>=4 && n_jet==4 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3b5j':     ('n_jet>=4 && n_jet==5 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3b6j':     ('n_jet>=4 && n_jet==6 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3bleq6j':     ('n_jet>=4 && n_jet<=6 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS3bleq6jhighpte':     ('lep_pt[0]>50e3 && !lep_is_muon[0] && n_jet>=4 && n_jet<=6 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b"),
#    '2LSS5j3b':     ('n_jet>=5 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 5j3b"),

#    '2LSS1b':       ('n_jet>=4 && n_bjet>=1','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j1b"),
#    '2LSS2b_el':       ('n_jet>=4 && n_bjet==2 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j2b electron"),
#    '2LSS2b_mu':       ('n_jet>=4 && n_bjet==2  && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j2b muon"),
#    '2LSS3b_el':       ('n_jet>=4 && n_bjet>=3 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b electron"),
#    '2LSS3b_mu':       ('n_jet>=4 && n_bjet>=3  && basemu_pt[0] > Alt$(baseel_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b muon"),
#    '2LSS3b_elnomllveto':       ('n_jet>=4 && n_bjet>=3 && baseel_pt[0] > Alt$(basemu_pt[0],0)','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b el nomllveto"),
#    '2LSS3j3b':       ('n_jet>=3 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 3j3b"),
#    '2LSS3b_mu':  ('n_jet>=4 && n_bjet>=3','(n_mu>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b #geq 1 muon"),
#    '2LSS3b_el':  ('n_jet>=4 && n_bjet>=3','(n_el>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b #geq 1 electron"),
#    '2LSS3bmll40':       ('n_jet>=4 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && Alt$(dilep_m[0],99e3)>40e3 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS 4j3b mll>40"),
#    '2LSS4j1b':       ('n_jet==4 && n_bjet>=1','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS ==4j1b"),
#    '2LSS5jincl1b':       ('n_jet>=5 && n_bjet>=1','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS >=5j1b"),
#    '2LSS6jincl3b':       ('n_jet>=6 && n_bjet>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "SS >=6j3b"),
#    '3L':       ('n_jet>=2 && n_bjet>=0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L 2j"),
#    '3L_mll':       ('n_jet>=2 && n_bjet>=0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && dilep_m[0] > 81e3 && dilep_m[0]<101e3)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L mll 2j"),
#    '3L_mllveto':   ('n_jet>=2 && n_bjet>=0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L mll veto 2j"),
#    '3L_4j_mll':       ('n_jet>=4 && n_bjet>=0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && dilep_m[0] > 81e3 && dilep_m[0]<101e3)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L mll 4j"),
#    '3L_4j_mllveto':   ('n_jet>=4 && n_bjet>=0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L mll veto 4j"),
#    '3L_4j1b':       ('n_jet>=4 && n_bjet>=1 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L 4j1b"),
#    '3L_4j0b':       ('n_jet>=4 && n_bjet==0 && n_lep>=3','(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS )', "3L 4j0b"),
}

for year in years:
  for cutname, (bothcut, rawcut, label) in cuts.iteritems():
    tag = ""
    if "2LSS" in cutname: tag = "_SS"
    if "3L" in cutname: tag = "_3L"
    configFile = '../Analysis/RPV1L/plotcfg/plotconfig_%s%s.py' % (year,tag)
    outputDir = 'figures/data_mc/%s/%s/' % (year,cutname)
    opts = " --label '%s'"%label
    if "2LSS3b" in cutname: opts += " --ratio2"
    if "3L" in cutname: opts += " --no-overlay"
    if "2Lemu" in cutname: opts += " --no-overlay"
    if "ZZ" in cutname: opts += " --no-overlay"
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
        sleep(1)
pool.close()
pool.join()
