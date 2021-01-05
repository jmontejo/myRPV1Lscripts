cd $SWUP_OUTPUTDIR/../myrpv1lscripts
SS2Lcut_weight="((n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum\$(lep_passECIDS==0)==0 && (n_el!=2 || Alt\$(dilep_m[0],0)<81e3 || Alt\$(dilep_m[0],0)>101e3))*(sf_el_ECIDS)"
SS2Lmlj155cut_weight="$SS2Lcut_weight*(calc_mlj_pair(lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0],Alt\$(lep_pt[1],0),Alt\$(lep_eta[1],0),Alt\$(lep_phi[1],0),Alt\$(lep_e[1],0),jet_pt[0],jet_eta[0],jet_phi[0],jet_e[0],jet_pt[1],jet_eta[1],jet_phi[1],jet_e[1],jet_pt[2],jet_eta[2],jet_phi[2],jet_e[2],jet_pt[3],jet_eta[3],jet_phi[3],jet_e[3])<155e3)"
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
./Vscaling_files.py --sample ttV_sherpa --outsample ttWMCmlj155 --filter-sample ttW --sample-cut "$SS2Lmlj155cut_weight"
./Vscaling_files.py --sample ttbar --outsample ttbar2LSSMCmlj155 --sample-cut "$SS2Lmlj155cut_weight"

./Vscaling_files_gammajets.py

./Vscaling_plot.py --sample gammajets
./Vscaling_plot.py --sample wjets_madgraph
./Vscaling_plot.py --sample wjetsMC
./Vscaling_plot.py --sample zjetsMC
./Vscaling_plot.py --sample multibosonsMC
./Vscaling_plot.py --sample WtMC
./Vscaling_plot.py --sample WtttbarMC
./Vscaling_plot.py --sample ttbarMC
./Vscaling_plot.py --sample ttbar1LMC
./Vscaling_plot.py --sample ttbar2LMC
./Vscaling_plot.py --sample ttbar_amcatnlo
./Vscaling_plot.py --sample ttbar_herwig
./Vscaling_plot.py --sample emubData
./Vscaling_plot.py --sample ttbar2LemubMC
./Vscaling_plot.py --sample ttbar2LemuMC
./Vscaling_plot.py --sample ttbar2LSSMCmlj155
./Vscaling_plot.py --sample ttWMCmlj155
./Vscaling_plot.py --sample ttWplusttbar2LSSMCmlj155

./Vscaling_plot.py --sample-group gammajets
./Vscaling_plot.py --sample-group ttbar
./Vscaling_plot.py --sample-group ttbar2L
./Vscaling_plot.py --sample-group ttbarsyst
./Vscaling_plot.py --sample-group SS3L
./Vscaling_plot.py --sample-group SS3Lmlj155
./Vscaling_plot.py --sample-group SS3Lmlj155comp --pt 20
./Vscaling_plot.py --sample-group Vjets
./Vscaling_plot.py --sample-group Wt

python acceptanceMC.py --pt 20 --pt 40 --pt 60 --pt 80 --pt 100 --btagger ""
python acceptanceMC.py --pt 20 --pt 40 --pt 60 --pt 80 --pt 100 --btagger "" --pack ttV --cutname 2LSS --cut  '((n_baseel+n_basemu)==2 && n_lep==2 && (el_trigger || mu_trigger) && lep_charge[0]*lep_charge[1]>0 && Sum$(lep_passECIDS==0)==0 && (n_el!=2 || Alt$(dilep_m[0],0)<81e3 || Alt$(dilep_m[0],0)>101e3))'

python W_charge_asym.py

plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS/ --cut '(lep_pt[1]>15e3 && n_jet>=4)*((n_lep==2 && (n_baseel+n_basemu)==2 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m
plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS_plus_baseline/ --cut '(lep_pt[1]>15e3 && n_jet>=4 &&)*((n_lep==2 && (n_baseel+n_basemu)>=3 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton plus baseline' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m

plot-comp.py n_bjet -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_mc16e/ -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_madgraph_mc16e/ --cut '(n_jet>=4 && lep_pt[0]>27e3)' -n wjets_nbjet  --ratio-fixed-range "0.4,1.6" --log --title-per-sample "W+jets Sherpa" --title-per-sample "W+jets Madgraph" --ratio-title "Ratio to Sherpa" -o figures/WHF
plot-comp.py minmax_mass -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/ttbar_merged/ -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/ttbar_merged/ -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/C1N1_higgsino_250_1L20_merged/ -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/N1N2_higgsino_250_1L20_merged/ --cut '(n_jet>=4 && lep_pt[0]>27e3)' -n minmax_mass_comp --cut-per-sample "(n_bjet>=1)" --cut-per-sample "(n_bjet>=3)" --cut-per-sample 1 --cut-per-sample 1 --title-per-sample "ttbar #geq 1 b-tag" --title-per-sample "ttbar #geq 3 b-tag" --title-per-sample "C1N1 higgsino 250 GeV"  --title-per-sample "N1N2 higgsino 250 GeV"  -o figures/ -b "20,0,600e3"

./yields-from-inputs.py

for j in 4 5 6 7 8; do
    lam=15
    plot-var.py "(network_output_2020_11_24_checkpoint_${j}j_dcorr_lam${lam}.ckpt+network_output_2020_11_24_checkpoint_${j}j_syst_lam09.ckpt)/2." --cut "(n_jet==${j} && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" -o figures/ttbar_invariance/  -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/C1N1_higgsino_250_1L20_merged/ --rebin-var 4 -b "10000,0,1"
    #for lam in 10 15 20 30; do
    #plot-var.py "network_output_2020_11_24_checkpoint_${j}j_dcorr_lam${lam}.ckpt" --cut "(n_jet==${j} && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" -o figures/ttbar_invariance/  -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/C1N1_higgsino_250_1L20_merged/ --rebin-var 4 -b "10000,0,1"
    #done
    #plot-var.py "network_output_2020_11_24_checkpoint_${j}j_syst_lam09.ckpt" --cut "(n_jet==${j} && lep_pt[0]>27e3 && (el_trigger || mu_trigger) && lep_trigger_matched)*(sf_total*sf_mu_trigger*sf_el_trigger*sf_el_ECIDS)" -o figures/ttbar_invariance/  -s /eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/C1N1_higgsino_250_1L20_merged/ --rebin-var 4 -b "10000,0,1"
done | grep -v "Environment initialised for data access" > percentil_vars.txt
