cd $SWUP_OUTPUTDIR/../myrpv1lscripts
SS2Lcut_weight="((n_baseel+n_basemu)==2 && n_lep==2 && lep_charge[0]*lep_charge[1]>0 && Sum\$(el_passECIDS==0)==0 && (n_el!=2 || Alt\$(dilep_m[0],0)<81e3 || Alt\$(dilep_m[0],0)>101e3))*(sf_el_ECIDS)"
emubcut_weight="(n_el==1 && n_mu==1 && Sum\$(jet_pt>{pt}e3 && jet_bjet)>=1)" #{pt} will be formatted inside

#./Vscaling_files.py --sample ttbar --outsample ttbar1LMC --sample-cut "(tt_cat==1 || tt_cat==4)"
#./Vscaling_files.py --sample ttbar --outsample ttbar2LMC --sample-cut "(tt_cat==0 || tt_cat==3 || tt_cat==6)" --minjet 2 --maxjet 13
#./Vscaling_files.py --sample ttbar --outsample ttbar2LemubMC --sample-cut $emubcut_weight --minjet 2 --maxjet 13
#./Vscaling_files.py --sample ttbar --outsample ttbar2LemuMC --sample-cut "(n_el==1 && n_mu==1)" --minjet 2 --maxjet 13
#./Vscaling_files.py --sample data --outsample emubData --sample-cut  $emubcut_weight --minjet 2 --maxjet 13
#./Vscaling_files.py --sample zjets --outsample zjetsMC
#./Vscaling_files.py --sample wjets --outsample wjetsMC
#./Vscaling_files.py --sample singletop --outsample WtMC --filter-sample Wt
#./Vscaling_files.py --sample multibosons --outsample multibosonsMC --sample-cut "n_lep>=3 && dilep_m[0]>81e3 && dilep_m[0]<101e3"
#./Vscaling_files.py --sample ttbar --outsample ttbar2LSSMC --sample-cut $SS2Lcut_weight
#./Vscaling_files.py --sample ttV_sherpa --outsample ttWMC --sample-filter ttW --sample-cut $SS2Lcut_weight

./Vscaling_files.py --sample ttbarAF2 --outsample ttbar_amcatnlo --filter-sample noShWe
./Vscaling_files.py --sample ttbarAF2 --outsample ttbar_herwig --filter-sample H7UE
./Vscaling_files.py --sample wjets_madgraph --outsample wjets_madgraph

#./Vscaling_files.py --sample singletop --outsample WtemubMC --filter-sample Wt --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
#./Vscaling_files.py --sample zjets --outsample zjetsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13
#./Vscaling_files.py --sample multibosons --outsample multibosonsemubMC --sample-cut "$emubcut_weight" --minjet 2 --maxjet 13

#./Vscaling_files_gammajets.py

./Vscaling_plot.py --sample-group ttbar
./Vscaling_plot.py --sample-group ttbarsyst
./Vscaling_plot.py --sample-group SS3L
./Vscaling_plot.py --sample-group Vjets
./Vscaling_plot.py --sample-group Wt
