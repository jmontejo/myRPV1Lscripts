cd $SWUP_OUTPUTDIR/../myrpv1lscripts
SS2Lcut_weight="((n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum\$(lep_passECIDS==0)==0 && (n_el!=2 || Alt\$(dilep_m[0],0)<81e3 || Alt\$(dilep_m[0],0)>101e3))*(sf_el_ECIDS)"
emubcut_weight="(n_el==1 && n_mu==1 && Sum\$(jet_pt>{pt}e3 && jet_bjet)>=1)" #{pt} will be formatted inside

./Vscaling_files.py --sample ttbar --outsample ttbar1LMC --sample-cut "(tt_cat==1 || tt_cat==4)"
./Vscaling_files.py --sample ttbar --outsample ttbar2LMC --sample-cut "(tt_cat==0 || tt_cat==3 || tt_cat==6)" --minjet 2 --maxjet 13
./Vscaling_files.py --sample ttbar --outsample ttbar2LemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample ttbar --outsample ttbar2LemuMC --sample-cut "(n_el==1 && n_mu==1)" --minjet 2 --maxjet 13
./Vscaling_files.py --sample data --outsample emubData --sample-cut  "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample zjets --outsample zjetsMC
./Vscaling_files.py --sample wjets --outsample wjetsMC
./Vscaling_files.py --sample singletop --outsample WtMC --filter-sample Wt
./Vscaling_files.py --sample multibosons --outsample multibosonsMC --sample-cut "n_lep>=3 && dilep_m[0]>81e3 && dilep_m[0]<101e3"
./Vscaling_files.py --sample ttbar_systME --outsample ttbar_amcatnlo
./Vscaling_files.py --sample ttbar_systPS --outsample ttbar_herwig
./Vscaling_files.py --sample wjets_madgraph --outsample wjets_madgraph
./Vscaling_files.py --sample singletop --outsample WtemubMC --filter-sample Wt --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample zjets --outsample zjetsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample multibosons --outsample multibosonsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample ttbar --outsample ttbar2LSSMC --sample-cut "$SS2Lcut_weight"
./Vscaling_files.py --sample ttV_sherpa --outsample ttWMC --filter-sample ttW --sample-cut "$SS2Lcut_weight"

./Vscaling_files_gammajets.py

./Vscaling_plot.py --sample gammajets
./Vscaling_plot.py --sample-group ttbar
./Vscaling_plot.py --sample-group ttbarsyst
./Vscaling_plot.py --sample-group SS3L
./Vscaling_plot.py --sample-group Vjets
./Vscaling_plot.py --sample-group Wt

python acceptanceMC.py --pt 20 --pt 40 --pt 60 --pt 80 --pt 100 --btagger ""
python acceptanceMC.py --pt 20 --pt 40 --pt 60 --pt 80 --pt 100 --btagger "" --pack ttV --cutname 2LSS --cut  '((n_baseel+n_basemu)==2 && n_lep==2 && (el_trigger || mu_trigger) && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))'

python W_charge_asym.py

plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS/ --cut '(lep_pt[1]>15e3 && n_jet>=4)*((n_lep==2 && (n_baseel+n_basemu)==2 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m
plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS_plus_baseline/ --cut '(lep_pt[1]>15e3 && n_jet>=4 &&)*((n_lep==2 && (n_baseel+n_basemu)>=3 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton plus baseline' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m

plot-comp.py n_bjet -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_mc16e/ -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_madgraph_mc16e/ --cut '(n_jet>=4 && lep_pt[0]>27e3)' -n wjets_nbjet  --ratio-fixed-range "0.4,1.6" --log --title-per-sample "W+jets Sherpa" --title-per-sample "W+jets Madgraph" --ratio-title "Ratio to Sherpa" -o figures/WHF

./yields-from-inputs.py

cut="((lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched && (n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*  lep_charge[1]>0 && Sum\$(lep_passECIDS==0)==0 && (n_el!=2 || Alt\$(dilep_m[0],0)<81e3 || Alt\$(dilep_m[0],0)>101e3))*(sf_total * sf_el_trigger * sf_mu_trigger*sf_el_ECIDS ))"
folder='/eos/user/a/atlrpv1l/rpv1l/output/skimexport/ntupleProd_21.2.119_a_SS1b/rpv2l_4j20_shrink/'
dphileplep='fabs(TVector2::Phi_mpi_pi(lep_phi[0]-lep_phi[1]))/TMath::Pi()'

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet==3)' --cut-per-sample '(n_jet>=4 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar #geq 4j 1b' --title-per-sample 'ttV+ttbar #geq 4j 2b' --title-per-sample 'ttV+ttbar #geq 4j 3b' --title-per-sample 'ttV+ttbar #geq 4j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_inclj -b "10,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet==3)' --cut-per-sample '(n_jet>=4 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar #geq 4j 1b' --title-per-sample 'ttV+ttbar #geq 4j 2b' --title-per-sample 'ttV+ttbar #geq 4j 3b' --title-per-sample 'ttV+ttbar #geq 4j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_inclj_coarse -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet==4 && n_bjet>=1)' --cut-per-sample '(n_jet==4 && n_bjet==1)' --cut-per-sample '(n_jet==4 && n_bjet==2)' --cut-per-sample '(n_jet==4 && n_bjet==3)' --cut-per-sample '(n_jet==4 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar 4j incl b' --title-per-sample 'ttV+ttbar 4j 1b' --title-per-sample 'ttV+ttbar 4j 2b' --title-per-sample 'ttV+ttbar 4j 3b' --title-per-sample 'ttV+ttbar 4j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_4j_coarse -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet==5 && n_bjet>=1)' --cut-per-sample '(n_jet==5 && n_bjet==1)' --cut-per-sample '(n_jet==5 && n_bjet==2)' --cut-per-sample '(n_jet==5 && n_bjet==3)' --cut-per-sample '(n_jet==5 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar 5j incl b' --title-per-sample 'ttV+ttbar 5j 1b' --title-per-sample 'ttV+ttbar 5j 2b' --title-per-sample 'ttV+ttbar 5j 3b' --title-per-sample 'ttV+ttbar 5j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_5j_coarse -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet==6 && n_bjet>=1)' --cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet==3)' --cut-per-sample '(n_jet==6 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar 6j incl b' --title-per-sample 'ttV+ttbar 6j 1b' --title-per-sample 'ttV+ttbar 6j 2b' --title-per-sample 'ttV+ttbar 6j 3b' --title-per-sample 'ttV+ttbar 6j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_6j_coarse -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
--cut-per-sample '(n_jet==7 && n_bjet>=1)' --cut-per-sample '(n_jet==7 && n_bjet==1)' --cut-per-sample '(n_jet==7 && n_bjet==2)' --cut-per-sample '(n_jet==7 && n_bjet==3)' --cut-per-sample '(n_jet==7 && n_bjet>=4)' \
--title-per-sample 'ttV+ttbar 7j incl b' --title-per-sample 'ttV+ttbar 7j 1b' --title-per-sample 'ttV+ttbar 7j 2b' --title-per-sample 'ttV+ttbar 7j 3b' --title-per-sample 'ttV+ttbar 7j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_dphileplep_7j_coarse -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar #geq 4j 1b' --title-per-sample 'ttV+ttbar #geq 4j 2b' --title-per-sample 'ttV+ttbar #geq 4j #geq 3b' \
--title-per-sample 'N1N2 250 GeV #geq 4j 1b' --title-per-sample 'N1N2 250 GeV #geq 4j 2b' --title-per-sample 'N1N2 250 GeV #geq 4j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_inclj -b "10,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar #geq 4j 1b' --title-per-sample 'ttV+ttbar #geq 4j 2b' --title-per-sample 'ttV+ttbar #geq 4j #geq 3b' \
--title-per-sample 'N1N2 250 GeV #geq 4j 1b' --title-per-sample 'N1N2 250 GeV #geq 4j 2b' --title-per-sample 'N1N2 250 GeV #geq 4j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse4_inclj -b "4,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet==4 && n_bjet==1)' --cut-per-sample '(n_jet==4 && n_bjet==2)' --cut-per-sample '(n_jet==4 && n_bjet>=3)' \
--cut-per-sample '(n_jet==4 && n_bjet==1)' --cut-per-sample '(n_jet==4 && n_bjet==2)' --cut-per-sample '(n_jet==4 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar 4j 1b' --title-per-sample 'ttV+ttbar 4j 2b' --title-per-sample 'ttV+ttbar 4j #geq 3b' \
--title-per-sample 'N1N2 250 GeV 4j 1b' --title-per-sample 'N1N2 250 GeV 4j 2b' --title-per-sample 'N1N2 250 GeV 4j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse_4j -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet==5 && n_bjet==1)' --cut-per-sample '(n_jet==5 && n_bjet==2)' --cut-per-sample '(n_jet==5 && n_bjet>=3)' \
--cut-per-sample '(n_jet==5 && n_bjet==1)' --cut-per-sample '(n_jet==5 && n_bjet==2)' --cut-per-sample '(n_jet==5 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar 5j 1b' --title-per-sample 'ttV+ttbar 5j 2b' --title-per-sample 'ttV+ttbar 5j #geq 3b' \
--title-per-sample 'N1N2 250 GeV 5j 1b' --title-per-sample 'N1N2 250 GeV 5j 2b' --title-per-sample 'N1N2 250 GeV 5j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse_5j -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet>=3)' \
--cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar 6j 1b' --title-per-sample 'ttV+ttbar 6j 2b' --title-per-sample 'ttV+ttbar 6j #geq 3b' \
--title-per-sample 'N1N2 250 GeV 6j 1b' --title-per-sample 'N1N2 250 GeV 6j 2b' --title-per-sample 'N1N2 250 GeV 6j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse_6j -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet==7 && n_bjet==1)' --cut-per-sample '(n_jet==7 && n_bjet==2)' --cut-per-sample '(n_jet==7 && n_bjet>=3)' \
--cut-per-sample '(n_jet==7 && n_bjet==1)' --cut-per-sample '(n_jet==7 && n_bjet==2)' --cut-per-sample '(n_jet==7 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar 7j 1b' --title-per-sample 'ttV+ttbar 7j 2b' --title-per-sample 'ttV+ttbar 7j #geq 3b' \
--title-per-sample 'N1N2 250 GeV 7j 1b' --title-per-sample 'N1N2 250 GeV 7j 2b' --title-per-sample 'N1N2 250 GeV 7j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse_7j -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged -s $folder/N1N2_higgsino_250_1L20_merged \
--cut-per-sample '(n_jet==4 && n_bjet>=2)' --cut-per-sample '(n_jet==5 && n_bjet>=2)' --cut-per-sample '(n_jet>=6 && n_bjet>=2)' \
--cut-per-sample '(n_jet==4 && n_bjet>=2)' --cut-per-sample '(n_jet==5 && n_bjet>=2)' --cut-per-sample '(n_jet>=6 && n_bjet>=2)' \
--title-per-sample 'ttV+ttbar 4j #geq 2b' --title-per-sample 'ttV+ttbar 5j #geq 2b' --title-per-sample 'ttV+ttbar 6j #geq 2b' \
--title-per-sample 'N1N2 250 GeV 4j #geq 2b' --title-per-sample 'N1N2 250 GeV 5j #geq 2b' --title-per-sample 'N1N2 250 GeV 6j #geq 2b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_signaldphileplep_coarse_2b_vs_jets -b "2,0,1" 

plot-comp.py $dphileplep \
--cut "$cut" \
-s $folder/ttX_merged -s $folder/ttX_merged -s $folder/ttX_merged \
-s $folder/data -s $folder/data -s $folder/data \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--cut-per-sample '(n_jet>=4 && n_bjet==1)' --cut-per-sample '(n_jet>=4 && n_bjet==2)' --cut-per-sample '(n_jet>=4 && n_bjet>=3)' \
--title-per-sample 'ttV+ttbar #geq 4j 1b' --title-per-sample 'ttV+ttbar #geq 4j 2b' --title-per-sample 'ttV+ttbar #geq 4j #geq 3b' \
--title-per-sample 'Data #geq 4j 1b' --title-per-sample 'Data #geq 4j 2b' --title-per-sample 'Data #geq 4j #geq 3b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
-n ttX_vs_datadphileplep_coarse4_inclj -b "4,0,1" 

exportf="/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/export_21.2.119/"
plot-comp.py network_output_2020_06_02_checkpoints_checkpoint_5j \
--cut "(n_jet==5 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==5)' --cut-per-sample '(n_jet==5 && n_bjet==1)' --cut-per-sample '(n_jet==5 && n_bjet==2)' --cut-per-sample '(n_jet==5 && n_bjet==3)' --cut-per-sample '(n_jet==5 && n_bjet>=4)' \
--title-per-sample 'ttbar 5j incl b' --title-per-sample 'ttbar 5j 1b' --title-per-sample 'ttbar 5j 2b' --title-per-sample 'ttbar 5j 3b' --title-per-sample 'ttbar 5j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_5j20_shrink \
-n NN_5j_ttbar_0602 -b "4,0,1" 
plot-comp.py network_output_2020_06_02_checkpoints_checkpoint_6j \
--cut "(n_jet==6 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==6)' --cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet==3)' --cut-per-sample '(n_jet==6 && n_bjet>=4)' \
--title-per-sample 'ttbar 6j incl b' --title-per-sample 'ttbar 6j 1b' --title-per-sample 'ttbar 6j 2b' --title-per-sample 'ttbar 6j 3b' --title-per-sample 'ttbar 6j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_6j20_shrink \
-n NN_6j_ttbar_0602 -b "4,0,1" 
plot-comp.py network_output_2020_06_02_checkpoints_checkpoint_7j \
--cut "(n_jet==7 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==7)' --cut-per-sample '(n_jet==7 && n_bjet==1)' --cut-per-sample '(n_jet==7 && n_bjet==2)' --cut-per-sample '(n_jet==7 && n_bjet==3)' --cut-per-sample '(n_jet==7 && n_bjet>=4)' \
--title-per-sample 'ttbar 7j incl b' --title-per-sample 'ttbar 7j 1b' --title-per-sample 'ttbar 7j 2b' --title-per-sample 'ttbar 7j 3b' --title-per-sample 'ttbar 7j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_7j20_shrink \
-n NN_7j_ttbar_0602 -b "4,0,1" 
plot-comp.py network_output_2020_06_09_checkpoints_checkpoint_5j \
--cut "(n_jet==5 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==5)' --cut-per-sample '(n_jet==5 && n_bjet==1)' --cut-per-sample '(n_jet==5 && n_bjet==2)' --cut-per-sample '(n_jet==5 && n_bjet==3)' --cut-per-sample '(n_jet==5 && n_bjet>=4)' \
--title-per-sample 'ttbar 5j incl b' --title-per-sample 'ttbar 5j 1b' --title-per-sample 'ttbar 5j 2b' --title-per-sample 'ttbar 5j 3b' --title-per-sample 'ttbar 5j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_5j20_shrink \
-n NN_5j_ttbar_0609 -b "4,0,1" 
plot-comp.py network_output_2020_06_09_checkpoints_checkpoint_6j \
--cut "(n_jet==6 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==6)' --cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet==3)' --cut-per-sample '(n_jet==6 && n_bjet>=4)' \
--title-per-sample 'ttbar 6j incl b' --title-per-sample 'ttbar 6j 1b' --title-per-sample 'ttbar 6j 2b' --title-per-sample 'ttbar 6j 3b' --title-per-sample 'ttbar 6j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_6j20_shrink \
-n NN_6j_ttbar_0609 -b "4,0,1" 
plot-comp.py network_output_2020_06_09_checkpoints_checkpoint_7j \
--cut "(n_jet==7 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
--cut-per-sample '(n_jet==7)' --cut-per-sample '(n_jet==7 && n_bjet==1)' --cut-per-sample '(n_jet==7 && n_bjet==2)' --cut-per-sample '(n_jet==7 && n_bjet==3)' --cut-per-sample '(n_jet==7 && n_bjet>=4)' \
--title-per-sample 'ttbar 7j incl b' --title-per-sample 'ttbar 7j 1b' --title-per-sample 'ttbar 7j 2b' --title-per-sample 'ttbar 7j 3b' --title-per-sample 'ttbar 7j #geq 4b' \
--ratio-fixed-range "0.5,1.5" -c rpv2l_7j20_shrink \
-n NN_7j_ttbar_0609 -b "4,0,1" 

exportf="/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/"
for j in 5 6 7; do
    for chk in 1 2 3; do
        plot-comp.py network_output_2020_09_09_checkpoint_${j}j_${chk} \
        --cut "(n_jet==${j} && n_bjet>=1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
        -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
        --cut-per-sample '(1)' --cut-per-sample '(n_bjet==1)' --cut-per-sample '(n_bjet==2)' --cut-per-sample '(n_bjet==3)' --cut-per-sample '(n_bjet>=4)' \
        --title-per-sample "ttbar ${j}j #geq 1b" --title-per-sample "ttbar ${j}j 1b" --title-per-sample "ttbar ${j}j 2b" --title-per-sample "ttbar ${j}j 3b" --title-per-sample "ttbar ${j}j #geq 4b" \
        --ratio-fixed-range "0.7,1.3" -c rpv2l_4j20_shrink \
        -n NN_${j}j_${chk}_0909_ttbar -b "4,0,1"  &

        #plot-comp.py network_output_2020_09_09_checkpoint_${j}j_${chk} \
        #--cut "(n_jet==${j} && n_bjet>=1 && n_lep==2 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
        #-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
        #--cut-per-sample '(1)' --cut-per-sample '(n_bjet==1)' --cut-per-sample '(n_bjet==2)' --cut-per-sample '(n_bjet==3)' --cut-per-sample '(n_bjet>=4)' \
        #--title-per-sample "ttbar 2L ${j}j #geq 1b" --title-per-sample "ttbar 2L ${j}j 1b" --title-per-sample "ttbar 2L ${j}j 2b" --title-per-sample "ttbar 2L ${j}j 3b" --title-per-sample "ttbar 2L ${j}j #geq 4b" \
        #--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
        #-n NN_${j}j_${chk}_0909_ttbar2L -b "4,0,1" &

        #plot-comp.py network_output_2020_09_09_checkpoint_${j}j_${chk} \
        #--cut "(n_jet==${j} && n_bjet>=1 && n_el==1 && n_mu==1 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
        #-s $exportf/data16 -s $exportf/data16 -s $exportf/data16 -s $exportf/data16 -s $exportf/data16 \
        #--cut-per-sample '(1)' --cut-per-sample '(n_bjet==1)' --cut-per-sample '(n_bjet==2)' --cut-per-sample '(n_bjet==3)' --cut-per-sample '(n_bjet>=4)' \
        #--title-per-sample 'emu data 5j #geq 1b' --title-per-sample 'emu data 5j 1b' --title-per-sample 'emu data 5j 2b' --title-per-sample 'emu data 5j 3b' --title-per-sample 'emu data 5j #geq 4b' \
        #--ratio-fixed-range "0.5,1.5" -c rpv2l_4j20_shrink \
        #-n NN_${j}j_${chk}_0909_dataemu -b "4,0,1" &
    done
done

#plot-comp.py network_output_2020_09_09_checkpoint_6j-2_1 \
#--cut "(n_jet==6 && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" \
#-s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a -s $exportf/ttbar_mc16a \
#--cut-per-sample '(n_jet==6)' --cut-per-sample '(n_jet==6 && n_bjet==1)' --cut-per-sample '(n_jet==6 && n_bjet==2)' --cut-per-sample '(n_jet==6 && n_bjet==3)' --cut-per-sample '(n_jet==6 && n_bjet>=4)' \
#--title-per-sample 'ttbar 6j incl b' --title-per-sample 'ttbar 6j 1b' --title-per-sample 'ttbar 6j 2b' --title-per-sample 'ttbar 6j 3b' --title-per-sample 'ttbar 6j #geq 4b' \
#--ratio-fixed-range "0.5,1.5" -c rpv2l_6j20_shrink \
#-n NN_6j-2_1_0909_ttbar -b "4,0,1" 

