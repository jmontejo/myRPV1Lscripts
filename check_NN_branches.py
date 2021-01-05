from ROOT import *
import glob
files = glob.glob("/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/*/*root")
files = glob.glob("/eos/atlas/atlaslocalgroupdisk/susy/jmontejo/ntupleProd_21.2.126_a/rpv2l_4j20_shrink/*/*/*root")

branches = [
# "network_output_2020_11_24_checkpoint_4j_dcorr_lam10.ckpt",
# "network_output_2020_11_24_checkpoint_4j_dcorr_lam15.ckpt",
 "network_output_2020_11_24_checkpoint_4j_dilep_lam15.ckpt",
# "network_output_2020_11_24_checkpoint_4j_dcorr_lam20.ckpt",
# "network_output_2020_11_24_checkpoint_4j_dcorr_lam30.ckpt",
# "network_output_2020_11_24_checkpoint_4j_syst_lam09.ckpt",
# "network_output_2020_11_24_checkpoint_5j_dcorr_lam10.ckpt",
# "network_output_2020_11_24_checkpoint_5j_dcorr_lam15.ckpt",
# "network_output_2020_11_24_checkpoint_5j_dcorr_lam20.ckpt",
# "network_output_2020_11_24_checkpoint_5j_dcorr_lam30.ckpt",
# "network_output_2020_11_24_checkpoint_5j_syst_lam09.ckpt",
# "network_output_2020_11_24_checkpoint_6j_dcorr_lam10.ckpt",
# "network_output_2020_11_24_checkpoint_6j_dcorr_lam15.ckpt",
# "network_output_2020_11_24_checkpoint_6j_dcorr_lam20.ckpt",
# "network_output_2020_11_24_checkpoint_6j_dcorr_lam30.ckpt",
# "network_output_2020_11_24_checkpoint_6j_syst_lam09.ckpt",
# "network_output_2020_11_24_checkpoint_7j_dcorr_lam10.ckpt",
# "network_output_2020_11_24_checkpoint_7j_dcorr_lam15.ckpt",
# "network_output_2020_11_24_checkpoint_7j_dcorr_lam20.ckpt",
# "network_output_2020_11_24_checkpoint_7j_dcorr_lam30.ckpt",
# "network_output_2020_11_24_checkpoint_7j_syst_lam09.ckpt",
# "network_output_2020_11_24_checkpoint_8j_dcorr_lam10.ckpt",
# "network_output_2020_11_24_checkpoint_8j_dcorr_lam15.ckpt",
# "network_output_2020_11_24_checkpoint_8j_dcorr_lam20.ckpt",
# "network_output_2020_11_24_checkpoint_8j_dcorr_lam30.ckpt",
# "network_output_2020_11_24_checkpoint_8j_syst_lam09.ckpt",
]

for f in files:
    if "merged" in f: continue
    tname = f.split("/")[-2]
    if "data" in tname and tname!="data": continue
    if not "data" in tname:
        sys = f.split("/")[-3]
        if sys == "rpv2l_4j20_shrink":
            sys = "Nom"
        tname += "_"+sys
    rfile = TFile.Open(f)
    if not rfile:
        print "WTF",f
        continue
    tree = rfile.Get(tname)
    if not tree: 
        print "WTF",f, tname
        continue

    #print tname, f
    for bname in branches:
        b = tree.GetBranch(bname)
        if not b:  print "/".join(f.split("/")[-2:]), bname
    rfile.Close()
