cd $SWUP_OUTPUTDIR/../myrpv1lscripts
SS2Lcut_weight="((n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum\$(el_passECIDS==0)==0 && (n_el!=2 || Alt\$(dilep_m[0],0)<81e3 || Alt\$(dilep_m[0],0)>101e3))*(sf_el_ECIDS)"
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
./Vscaling_files.py --sample ttbar --outsample ttbar2LSSMC --sample-cut "$SS2Lcut_weight"
./Vscaling_files.py --sample ttV_sherpa --outsample ttWMC --sample-filter ttW --sample-cut "$SS2Lcut_weight"
./Vscaling_files.py --sample ttbarAF2 --outsample ttbar_amcatnlo --filter-sample noShWe
./Vscaling_files.py --sample ttbarAF2 --outsample ttbar_herwig --filter-sample H7UE
./Vscaling_files.py --sample wjets_madgraph --outsample wjets_madgraph
./Vscaling_files.py --sample singletop --outsample WtemubMC --filter-sample Wt --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample zjets --outsample zjetsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
./Vscaling_files.py --sample multibosons --outsample multibosonsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13

./Vscaling_files_gammajets.py

./Vscaling_plot.py --sample gammajets
./Vscaling_plot.py --sample-group ttbar
./Vscaling_plot.py --sample-group ttbarsyst
./Vscaling_plot.py --sample-group SS3L
./Vscaling_plot.py --sample-group Vjets
./Vscaling_plot.py --sample-group Wt

python acceptanceMC.py --pt 20 --btagger ""
python acceptanceMC.py --pt 40 --btagger ""
python acceptanceMC.py --pt 60 --btagger ""
python acceptanceMC.py --pt 80 --btagger ""

python W_charge_asym.py

plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS/ --cut '(lep_pt[1]>15e3 && n_jet>=4 && jet_pt[1]>30e3)*((n_lep==2 && (n_baseel+n_basemu)==2 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m
plot.py -c rpv2l_4j20_shrink --no-overlay -o figures/data_mc/2015_2018/2LOS_plus_baseline/ --cut '(lep_pt[1]>15e3 && n_jet>=4 && jet_pt[1]>30e3)*((n_lep==2 && (n_baseel+n_basemu)>=3 && lep_pt[0]>27e3 && lep_charge[0]!=lep_charge[1] && (el_trigger || mu_trigger) )*(sf_total*sf_mu_trigger*sf_el_trigger))' --sample-cut 'Fakes#0'  --label 'Dilepton plus baseline' -p ../Analysis/RPV1L/plotcfg/plotconfig_2015_2018_SS.py dilep_m

plot-comp.py n_bjet -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_mc16e/ -s /eos/user/a/atlrpv1l/rpv1l/output/export/ntupleProd_21.2.114_a/rpv2l_4j20_shrink/wjets_madgraph_mc16e/ --cut '(n_jet>=4 && lep_pt[0]>27e3)' -n wjets_nbjet  --ratio-fixed-range "0.4,1.6" --log --title-per-sample "W+jets Sherpa" --title-per-sample "W+jets Madgraph" --ratio-title "Ratio to Sherpa" -o figures/WHF
