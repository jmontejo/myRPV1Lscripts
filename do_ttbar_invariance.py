import os
from multiprocessing import Pool
pool = Pool(8)

cuts = {
    "2LSS":"((lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]* lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS ))",
    "2Lemu":"((lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && n_el==1 && n_mu==1)*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS ))",
    "1L": "(lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)", 
}
cuts["2LSSmlj155"] = cuts["2LSS"]+"*(calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],Alt$(lep_pt[1],0),Alt$(lep_eta[1],0),Alt$(lep_phi[1],0),Alt$(lep_e[1],0),jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1], jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3], jet_phi[3],jet_e[3])<155e3)"

variables= {
    "dphileplep": 'fabs(TVector2::Phi_mpi_pi(lep_phi[0]-lep_phi[1]))/TMath::Pi()',
    "maxmindphi": 'max_min_dphi(jet_phi[0],jet_phi[1],jet_phi[2],jet_phi[3],Alt$(jet_phi[4],9),Alt$(jet_phi[5],9),Alt$(jet_phi[6],9),Alt$(jet_phi[7],9))',
    "network_output_2020_11_19_percentil_6j_dcorr_lam10_tuned" : "((network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.449-0.003*(n_bjet>=4)+0.003*(n_bjet==3))+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.614)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.758-0.001*(n_bjet==3)))/4.",
    "network_output_2020_11_19_percentil_6j_dcorr_lam10" : "((network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.449)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.614)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.758))/4.",
    "network_output_2020_11_19_percentil_6j_syst" : "((network_output_2020_11_19_test_checkpoint_6j_syst > 0.428)+(network_output_2020_11_19_test_checkpoint_6j_syst > 0.613)+(network_output_2020_11_19_test_checkpoint_6j_syst > 0.767))/4.",
    "network_output_2020_11_19_percentil10bins_6j_dcorr_lam10" : "((network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.259900)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.398800)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.489400)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.555100)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.613600)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.670100)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.727300)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.789700)+(network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10 > 0.860700))/10.",
    "network_output_2020_11_24_checkpoint_4j_dcorr_lam10_percentil" : "((network_output_2020_11_24_checkpoint_4j_dcorr_lam10.ckpt > 0.383100)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam10.ckpt > 0.605600)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam10.ckpt > 0.737300))/4.",
    "network_output_2020_11_24_checkpoint_4j_dcorr_lam15_percentil" : "((network_output_2020_11_24_checkpoint_4j_dcorr_lam15.ckpt > 0.415900)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam15.ckpt > 0.605000)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam15.ckpt > 0.730600))/4.",
    "network_output_2020_11_24_checkpoint_4j_dcorr_lam20_percentil" : "((network_output_2020_11_24_checkpoint_4j_dcorr_lam20.ckpt > 0.447900)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam20.ckpt > 0.624300)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam20.ckpt > 0.747700))/4.",
    "network_output_2020_11_24_checkpoint_4j_dcorr_lam30_percentil" : "((network_output_2020_11_24_checkpoint_4j_dcorr_lam30.ckpt > 0.522900)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam30.ckpt > 0.611900)+(network_output_2020_11_24_checkpoint_4j_dcorr_lam30.ckpt > 0.701500))/4.",
    "network_output_2020_11_24_checkpoint_4j_syst_lam09_percentil"  : "((network_output_2020_11_24_checkpoint_4j_syst_lam09.ckpt > 0.416700)+(network_output_2020_11_24_checkpoint_4j_syst_lam09.ckpt > 0.620400)+(network_output_2020_11_24_checkpoint_4j_syst_lam09.ckpt > 0.789600))/4.",
    "network_output_2020_11_24_checkpoint_5j_dcorr_lam10_percentil" : "((network_output_2020_11_24_checkpoint_5j_dcorr_lam10.ckpt > 0.388900)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam10.ckpt > 0.598000)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam10.ckpt > 0.741800))/4.",
    "network_output_2020_11_24_checkpoint_5j_dcorr_lam15_percentil" : "((network_output_2020_11_24_checkpoint_5j_dcorr_lam15.ckpt > 0.449400)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam15.ckpt > 0.622100)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam15.ckpt > 0.755200))/4.",
    "network_output_2020_11_24_checkpoint_5j_dcorr_lam20_percentil" : "((network_output_2020_11_24_checkpoint_5j_dcorr_lam20.ckpt > 0.446800)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam20.ckpt > 0.622500)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam20.ckpt > 0.754900))/4.",
    "network_output_2020_11_24_checkpoint_5j_dcorr_lam30_percentil" : "((network_output_2020_11_24_checkpoint_5j_dcorr_lam30.ckpt > 0.501400)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam30.ckpt > 0.649300)+(network_output_2020_11_24_checkpoint_5j_dcorr_lam30.ckpt > 0.754500))/4.",
    "network_output_2020_11_24_checkpoint_5j_syst_lam09_percentil"  : "((network_output_2020_11_24_checkpoint_5j_syst_lam09.ckpt > 0.434100)+(network_output_2020_11_24_checkpoint_5j_syst_lam09.ckpt > 0.624200)+(network_output_2020_11_24_checkpoint_5j_syst_lam09.ckpt > 0.785200))/4.",
    "network_output_2020_11_24_checkpoint_6j_dcorr_lam10_percentil" : "((network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.448600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.613600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.757900))/4.",
    "network_output_2020_11_24_checkpoint_6j_dcorr_lam15_percentil" : "((network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt > 0.435500)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt > 0.630600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt > 0.768300))/4.",
    "network_output_2020_11_24_checkpoint_6j_dcorr_lam20_percentil" : "((network_output_2020_11_24_checkpoint_6j_dcorr_lam20.ckpt > 0.439600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam20.ckpt > 0.604600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam20.ckpt > 0.719700))/4.",
    "network_output_2020_11_24_checkpoint_6j_dcorr_lam30_percentil" : "((network_output_2020_11_24_checkpoint_6j_dcorr_lam30.ckpt > 0.425400)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam30.ckpt > 0.621300)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam30.ckpt > 0.717900))/4.",
    "network_output_2020_11_24_checkpoint_6j_syst_lam09_percentil"  : "((network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.427400)+(network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.612800)+(network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.766100))/4.",
    "network_output_2020_11_24_checkpoint_6j_avg_syst_lam09_dcorr_lam10_percentil"  : "((network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.427400)+(network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.612800)+(network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt > 0.766100)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.448600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.613600)+(network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt > 0.757900))/8.",
    "network_output_2020_11_24_checkpoint_6j_realavg_syst_lam09_dcorr_lam10_percentil"  : "(((network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt+network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt)/2. > 0.433900)+((network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt+network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt)/2. > 0.621600)+((network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt+network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt)/2. > 0.764500))/4.",
    "network_output_2020_11_24_checkpoint_7j_dcorr_lam10_percentil" : "((network_output_2020_11_24_checkpoint_7j_dcorr_lam10.ckpt > 0.426100)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam10.ckpt > 0.584300)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam10.ckpt > 0.717100))/4.",
    "network_output_2020_11_24_checkpoint_7j_dcorr_lam15_percentil" : "((network_output_2020_11_24_checkpoint_7j_dcorr_lam15.ckpt > 0.384700)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam15.ckpt > 0.580300)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam15.ckpt > 0.718000))/4.",
    "network_output_2020_11_24_checkpoint_7j_dcorr_lam20_percentil" : "((network_output_2020_11_24_checkpoint_7j_dcorr_lam20.ckpt > 0.479700)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam20.ckpt > 0.625000)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam20.ckpt > 0.729500))/4.",
    "network_output_2020_11_24_checkpoint_7j_dcorr_lam30_percentil" : "((network_output_2020_11_24_checkpoint_7j_dcorr_lam30.ckpt > 0.515500)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam30.ckpt > 0.604300)+(network_output_2020_11_24_checkpoint_7j_dcorr_lam30.ckpt > 0.693700))/4.",
    "network_output_2020_11_24_checkpoint_7j_syst_lam09_percentil"  : "((network_output_2020_11_24_checkpoint_7j_syst_lam09.ckpt > 0.415800)+(network_output_2020_11_24_checkpoint_7j_syst_lam09.ckpt > 0.599000)+(network_output_2020_11_24_checkpoint_7j_syst_lam09.ckpt > 0.765800))/4.",
    "network_output_2020_11_24_checkpoint_8j_dcorr_lam10_percentil" : "((network_output_2020_11_24_checkpoint_8j_dcorr_lam10.ckpt > 0.443200)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam10.ckpt > 0.616300)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam10.ckpt > 0.751200))/4.",
    "network_output_2020_11_24_checkpoint_8j_dcorr_lam15_percentil" : "((network_output_2020_11_24_checkpoint_8j_dcorr_lam15.ckpt > 0.481100)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam15.ckpt > 0.607500)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam15.ckpt > 0.730300))/4.",
    "network_output_2020_11_24_checkpoint_8j_dcorr_lam20_percentil" : "((network_output_2020_11_24_checkpoint_8j_dcorr_lam20.ckpt > 0.404700)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam20.ckpt > 0.620900)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam20.ckpt > 0.752300))/4.",
    "network_output_2020_11_24_checkpoint_8j_dcorr_lam30_percentil" : "((network_output_2020_11_24_checkpoint_8j_dcorr_lam30.ckpt > 0.484800)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam30.ckpt > 0.623200)+(network_output_2020_11_24_checkpoint_8j_dcorr_lam30.ckpt > 0.728700))/4.",
    "network_output_2020_11_24_checkpoint_8j_syst_lam09_percentil"  : "((network_output_2020_11_24_checkpoint_8j_syst_lam09.ckpt > 0.418700)+(network_output_2020_11_24_checkpoint_8j_syst_lam09.ckpt > 0.595200)+(network_output_2020_11_24_checkpoint_8j_syst_lam09.ckpt > 0.753800))/4.",
}

def main():
#    comparison_plot(-4,4,"ttV_merged","2LSS", "dphileplep",10)
#    comparison_plot(-4,4,"ttV_sherpa_merged","2LSS", "dphileplep",10)
#    comparison_plot(-4,4,"ttbar_merged","2LSS", "dphileplep",10)
#    comparison_plot(-4,4,"ttX_merged","2LSS", "dphileplep",10)
#    comparison_plot(-4,4,"ttV_merged","2LSS", "dphileplep",2)
#    comparison_plot(-4,4,"ttV_sherpa_merged","2LSS", "dphileplep",2)
#    comparison_plot(-4,4,"ttbar_merged","2LSS", "dphileplep",2)
#    comparison_plot(-4,4,"ttX_merged","2LSS", "dphileplep",2)
#    comparison_plot(-4,4,"ttV_merged","2LSSmlj155", "dphileplep",2)
#    comparison_plot(-4,4,"ttV_sherpa_merged","2LSSmlj155", "dphileplep",2)
#    comparison_plot(-4,4,"ttbar_merged","2LSSmlj155", "dphileplep",2)
#    comparison_plot(-4,4,"ttX_merged","2LSSmlj155", "dphileplep",2)
#    comparison_plot( 4,3,"ttV_merged","2LSS", "dphileplep",2)
#    comparison_plot( 4,3,"ttV_sherpa_merged","2LSS", "dphileplep",2)
#    comparison_plot( 4,3,"ttbar_merged","2LSS", "dphileplep",2)
#    comparison_plot( 4,3,"ttX_merged","2LSS", "dphileplep",2)
#    comparison_plot( 4,3,"ttX_merged","2LSSmlj155", "dphileplep",2)
#    comparison_plot( 5,3,"ttX_merged","2LSS", "dphileplep",2)
#    comparison_plot( 6,3,"ttX_merged","2LSS", "dphileplep",2)
#    comparison_plot( 7,3,"ttX_merged","2LSS", "dphileplep",2)
#    
    comparison_plot(-4,4,"ttX_merged","2LSSmlj155", "dphileplep",2,tag="4b")
    comparison_plot(-4,3,"ttX_merged","2LSSmlj155", "dphileplep", 2, "N1N2_higgsino_250_1L20_merged","3bincl",nbjetmin=3, sep=True)
    comparison_plot(-4,4,"ttX_merged","2LSSmlj155", "dphileplep",3,tag="4b")
    comparison_plot(-4,3,"ttX_merged","2LSSmlj155", "dphileplep", 3, "N1N2_higgsino_250_1L20_merged","3bincl",nbjetmin=3, sep=True)
#    
#    comparison_plot(-4,3,"ttX_merged","2LSS", "dphileplep", 2, "data")
#    comparison_plot(-4,3,"ttX_merged","2LSS", "dphileplep", 4, "data")
#    
#    ####################################################
#    
#    comparison_plot( 5,4,"ttbar_mc16a","1L", "network_output_2020_06_02_checkpoints_checkpoint_NJETj", 4)
#    comparison_plot( 6,4,"ttbar_mc16a","1L", "network_output_2020_06_02_checkpoints_checkpoint_NJETj", 4)
#    comparison_plot( 7,4,"ttbar_mc16a","1L", "network_output_2020_06_02_checkpoints_checkpoint_NJETj", 4)
#    comparison_plot( 5,4,"ttbar_mc16a","1L", "network_output_2020_06_09_checkpoints_checkpoint_NJETj", 4)
#    comparison_plot( 6,4,"ttbar_mc16a","1L", "network_output_2020_06_09_checkpoints_checkpoint_NJETj", 4)
#    comparison_plot( 7,4,"ttbar_mc16a","1L", "network_output_2020_06_09_checkpoints_checkpoint_NJETj", 4)
#    
#    for chk in (1, 2, 3):
#        for j in (5, 6, 7):
#            comparison_plot( j,4,"ttbar_mc16a","1L",    "network_output_2020_09_09_checkpoint_NJETj_%d"%chk, 4)
#            comparison_plot( j,4,"ttbar_mc16a","2Lemu", "network_output_2020_09_09_checkpoint_NJETj_%d"%chk, 4)
#            comparison_plot( j,4,"data"       ,"2Lemu", "network_output_2020_09_09_checkpoint_NJETj_%d"%chk, 4)
#            if j==6:
#                comparison_plot( j,4,"ttbar_mc16a","1L",    "network_output_2020_09_09_checkpoint_NJETj_special_%d"%chk, 4)
#                comparison_plot( j,4,"ttbar_systPS_mc16a","1L",    "network_output_2020_09_09_checkpoint_NJETj_special_%d"%chk, 4)
#                comparison_plot( j,4,"ttbar_systME_mc16a","1L",    "network_output_2020_09_09_checkpoint_NJETj_special_%d"%chk, 4)
#    comparison_plot( 6,4,"ttbar_mc16a","1L",    "maxmindphi", 10)

#    comparison_plot( 6,4,"ttbar_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4, zoom=True)
#    comparison_plot( 6,4,"ttbar_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide3", 4, zoom=True)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide3", 4)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide3", 4)
#    comparison_plot( 6,3,"ttbar_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4, "C1N1_higgsino_250_1L20_mc16e", nbjetmin=3, sep=True)
#    comparison_plot( 6,3,"ttbar_merged","1L",    "network_output_2020_11_04_checkpoint_6j_slide3", 4, "C1N1_higgsino_250_1L20_mc16e", nbjetmin=3, sep=True)
#    comparison_plot( 6,4,"ttbar_mc16a","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4, zoom=True, exactly4=True)
#    comparison_plot( 6,4,"ttbar_systME_mc16a","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4, exactly4=True)
#    comparison_plot( 6,4,"ttbar_systPS_mc16a","1L",    "network_output_2020_11_04_checkpoint_6j_slide1", 4, exactly4=True)
#    comparison_plot( 6,4,"ttbar_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4, zoom=True)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4)
#    comparison_plot( 6,4,"ttbar_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_syst", 4, zoom=True)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_syst", 4)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_syst", 4)
#    comparison_plot( 6,4,"C1N1_higgsino_250_1L20_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4)
#    comparison_plot( 6,4,"C1N1_higgsino_250_1L20_merged","1L",    "network_output_2020_11_19_test_checkpoint_6j_syst", 4)

#    comparison_plot( 6,4,"ttbar_merged","1L",        "network_output_2020_11_19_percentil10bins_6j_dcorr_lam10", 10)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L", "network_output_2020_11_19_percentil10bins_6j_dcorr_lam10", 10)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L", "network_output_2020_11_19_percentil10bins_6j_dcorr_lam10", 10)
#    comparison_plot( 6,4,"ttbar_merged","1L",        "network_output_2020_11_19_percentil_6j_syst", 4, zoom=True)
#    comparison_plot( 6,4,"ttbar_systME_merged","1L", "network_output_2020_11_19_percentil_6j_syst", 4)
#    comparison_plot( 6,4,"ttbar_systPS_merged","1L", "network_output_2020_11_19_percentil_6j_syst", 4)

#    comparison_plot( 6,4,"ttbar_merged","2Lemu", "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4)
#    comparison_plot( 6,4,"data"       ,"2Lemu", "network_output_2020_11_19_test_checkpoint_6j_dcorr_lam10", 4)
#    comparison_plot( 6,4,"ttbar_merged","2Lemu", "network_output_2020_11_19_test_checkpoint_6j_syst", 4)
#    comparison_plot( 6,4,"data"       ,"2Lemu", "network_output_2020_11_19_test_checkpoint_6j_syst", 4)

    branches = [
        "network_output_2020_11_24_checkpoint_NJETj_syst_lam09_percentil", 
        #"network_output_2020_11_24_checkpoint_NJETj_dcorr_lam10_percentil",
        "network_output_2020_11_24_checkpoint_NJETj_dcorr_lam15_percentil",
        #"network_output_2020_11_24_checkpoint_NJETj_dcorr_lam20_percentil",
        #"network_output_2020_11_24_checkpoint_NJETj_dcorr_lam30_percentil",
    ]
    for j in [6]:
    #for j in (6, 5, 7, 4, 8):
      for b in branches:
       # comparison_plot( j,4,"ttbar_merged", "1L", b, 4, zoom=True)
        comparison_plot( j,4,"ttbar_systPS_merged", "1L", b, 4, zoom=True)
        comparison_plot( j,4,"ttbar_systME_merged", "1L", b, 4, zoom=True)
    #comparison_plot( 6,4,"ttbar_mc16e", "1L",        "network_output_2020_11_24_checkpoint_6j_realavg_syst_lam09_dcorr_lam10_percentil", 4, zoom=True)
    #comparison_plot( 6,4,"ttbar_systPS_mc16e", "1L", "network_output_2020_11_24_checkpoint_6j_realavg_syst_lam09_dcorr_lam10_percentil", 4, zoom=True)
    #comparison_plot( 6,4,"ttbar_systME_mc16e", "1L", "network_output_2020_11_24_checkpoint_6j_realavg_syst_lam09_dcorr_lam10_percentil", 4, zoom=True)



def get_title(njet,samplename, nbjet, bincl=False):
    samplename = samplename.replace("_merged","")
    jincl = "#geq " if njet < 0 else""
    njet = abs(njet)
    bincl = "#geq " if bincl else""
    title = '%s %s%dj %s%db'%(samplename,jincl,njet,bincl,nbjet)
    return title

def comparison_plot(njet, nbjetmax, sample, cutname, varname, nbins, sample2=None, tag=None, nbjetmin=1, sep=False, zoom=False, exactly4=False):
    if "2LSS" in cutname:
        folder = '/eos/user/a/atlrpv1l/rpv1l/output/skimexport/ntupleProd_21.2.126_a_2LSS/rpv2l_4j20_shrink/'
    elif "network_output_2020_06" in varname:
        folder="/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/export_21.2.119/"
    else:
        folder="/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/"
    cut = cuts[cutname]
    varname =  varname.replace("NJET",str(abs(njet)))
    var = variables.get(varname, varname)
    
    vartitle = varname if varname in variables else var
    if vartitle == "dphileplep":
        vartitle = "#Delta#phi(l,l)/#pi"
    ratio = "--ratio-fixed-range  '0.5,1.5' "
    exactly4=int(exactly4)

    if njet<0:
        jetcut = "n_jet>=%d"%(-njet)
    else:
        jetcut = "n_jet==%d"%(njet)

    extra = " --x-title '%s'"%vartitle
    if not sample2:
        samples = "-s {folder}/{sample} "*(nbjetmax+2-nbjetmin+exactly4)
        samples = samples.format(folder=folder,sample=sample)
        cuts_per_sample = "--cut-per-sample '(%s && n_bjet>=%d)' "%(jetcut,nbjetmin)
        cuts_per_sample+= " ".join(["--cut-per-sample '(%s && n_bjet==%d)' "%(jetcut,nb) for nb in range(nbjetmin,nbjetmax+exactly4)])
        cuts_per_sample+= "--cut-per-sample '(%s && n_bjet>=%d)' "%(jetcut,nbjetmax)
        titles_per_sample = "--title-per-sample '%s' " % get_title(njet,sample, nbjetmin, bincl=True)
        titles_per_sample+= " ".join(["--title-per-sample '%s' " % get_title(njet,sample, nb) for nb in range(nbjetmin,nbjetmax+exactly4)])
        titles_per_sample+= "--title-per-sample '%s' " % get_title(njet,sample, nbjetmax, bincl=True)
        if cutname == "1L":
            ratio = "--ratio-fixed-range  '0.7,1.3' "
            extra+= " --klmean "
    else:
        samples = "-s {folder}/{sample} "*(nbjetmax+1-nbjetmin) + "-s {folder}/{sample2} "*(nbjetmax+1-nbjetmin+exactly4)
        samples = samples.format(folder=folder,sample=sample,sample2=sample2)
        cuts_per_sample = " ".join(["--cut-per-sample '(%s && n_bjet==%d)' "%(jetcut,nb) for nb in range(nbjetmin,nbjetmax+exactly4)])
        cuts_per_sample+= "--cut-per-sample '(%s && n_bjet>=%d)' "%(jetcut,nbjetmax)
        cuts_per_sample *= 2
        titles_per_sample = " ".join(["--title-per-sample '%s' " % get_title(njet,sample, nb) for nb in range(nbjetmin,nbjetmax+exactly4)])
        titles_per_sample+= "--title-per-sample '%s' " % get_title(njet,sample, nbjetmax, bincl=True)
        titles_per_sample+= " ".join(["--title-per-sample '%s' " % get_title(njet,sample2, nb) for nb in range(nbjetmin,nbjetmax+exactly4)])
        titles_per_sample+= "--title-per-sample '%s' " % get_title(njet,sample2, nbjetmax, bincl=True)
        if sep: extra+=" --sep "

    if zoom:
        ratio = "--ratio-fixed-range  '0.9,1.1' "

    if sep: titles_per_sample = ""
    jname = "%dj%s"%(abs(njet),"incl" if njet<0 else "")
    if not sample2:
        plotname = "_".join([sample,varname,cutname,jname,"%dbins"%nbins])
    else:
        plotname = "_".join([sample,"vs_"+sample2,varname,cutname,jname,"%dbins"%nbins])
    if tag: plotname += "_"+tag
    if nbjetmin!=1: plotname += "_min%db"%nbjetmin

    cmd = "plot-comp.py '{var}' --cut '{cut}' -o figures/ttbar_invariance/ \
           {samples} {cuts_per_sample} {titles_per_sample} {ratio} -c rpv2l_4j20_shrink \
           -n {plotname} {extra} -b '{nbins},0,1' ".format(var=var,cut=cut,samples=samples,cuts_per_sample=cuts_per_sample, titles_per_sample=titles_per_sample,ratio=ratio,plotname=plotname,extra=extra,nbins=nbins)
    print cmd
    pool.apply_async(os.system, args=(cmd,))

if __name__ == "__main__": main()

pool.close()
pool.join()
    
#plot-comp.py $dphileplep \
#--cut "$cut" \
#-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
#-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
#--cut-per-sample '(n_jet==4 && n_bjet>=2)' --cut-per-sample '(n_jet==5 && n_bjet>=2)' --cut-per-sample '(n_jet>=6 && n_bjet>=2)' \
#--cut-per-sample '(n_jet==4 && n_bjet>=2)' --cut-per-sample '(n_jet==5 && n_bjet>=2)' --cut-per-sample '(n_jet>=6 && n_bjet>=2)' \
#--title-per-sample 'ttV+ttbar 4j #geq 2b' --title-per-sample 'ttV+ttbar 5j #geq 2b' --title-per-sample 'ttV+ttbar 6j #geq 2b' \
#--title-per-sample 'N1N2 250 GeV 4j #geq 2b' --title-per-sample 'N1N2 250 GeV 5j #geq 2b' --title-per-sample 'N1N2 250 GeV 6j #geq 2b' \
#--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
#-n ttX_vs_signaldphileplep_coarse_2b_vs_jets -b "2,0,1" 
