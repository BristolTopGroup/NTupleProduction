import sys
import os


jobTemplates = [
	["TTJets_PowhegPythia8_tree.root", [
		"TTJets_PowhegPythia8_central_atOutput_*.root"
	] ],
	["TTJets_PowhegPythia8_isrup_tree.root", [
		"TTJets_PowhegPythia8_isrup_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_isrdown_tree.root", [
		"TTJets_PowhegPythia8_isrdown_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_fsrup_tree.root", [
		"TTJets_PowhegPythia8_fsrup_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_fsrdown_tree.root", [
		"TTJets_PowhegPythia8_fsrdown_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_up_tree.root", [
		"TTJets_PowhegPythia8_up_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_down_tree.root", [
		"TTJets_PowhegPythia8_down_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_hdampup_tree.root", [
		"TTJets_PowhegPythia8_hdampup_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_hdampdown_tree.root", [
		"TTJets_PowhegPythia8_hdampdown_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_erdOn_tree.root", [
		"TTJets_PowhegPythia8_erdOn_central_atOutput_*.root"
	], "C" ],

	["TTJets_PowhegPythia8_mtop1695_tree.root", [
		"TTJets_PowhegPythia8_mtop1695_central_atOutput_*.root"
	], "C" ],
	["TTJets_PowhegPythia8_mtop1755_tree.root", [
		"TTJets_PowhegPythia8_mtop1755_central_atOutput_*.root"
	], "C" ],

	["TTJets_PowhegHerwigpp_tree.root", [
		"TTJets_PowhegHerwigpp_central_atOutput_*.root"
	], "C"],
	["TTJets_amc_tree.root", [
		"TTJets_amcatnloFXFX_central_atOutput_*.root"
	], "C"],
	["TTJets_madgraph_tree.root", [
		"TTJets_madgraphMLM_central_atOutput_*.root"
	], "C"],

	["SingleTop_tree.root", [
		"ST*_central_atOutput_*.root"
	] ],

	 ["VJets_tree.root", [
	 	"DY1JetsToLL_M50_central_atOutput_*", 
	 	"DY2JetsToLL_M50_central_atOutput_*", 
	 	"DY3JetsToLL_M50_central_atOutput_*", 
	 	"DY4JetsToLL_M50_central_atOutput_*", 
	 	"W1JetsToLNu_central_atOutput_*",
	 	"W2JetsToLNu_central_atOutput_*",
	 	"W3JetsToLNu_central_atOutput_*",
	 	"W4JetsToLNu_central_atOutput_*"
	 ] ],

	["QCD_Electron_tree.root", [
		"QCD_bcToE_*_central_atOutput_*", 
		"QCD_EMEnriched_*_central_atOutput_*"
	] ],
	["QCD_Muon_tree.root", [
		"QCD_MuEnriched_*_central_atOutput_*.root"
	] ],

	# ["QCD_Inclusive_tree.root", [
	# 	"QCD_1000to1400_central_atOutput_*.root",
	# 	"QCD_120to170_central_atOutput_*.root",
	# 	"QCD_1400to1800_central_atOutput_*.root",
	# 	"QCD_170to300_central_atOutput_*.root",
	# 	"QCD_1800to2400_central_atOutput_*.root",
	# 	"QCD_2400to3200_central_atOutput_*.root",
	# 	"QCD_300to470_central_atOutput_*.root",
	# 	"QCD_3200toInf_central_atOutput_*.root",
	# 	"QCD_470to600_central_atOutput_*.root",
	# 	"QCD_50to80_central_atOutput_*.root",
	# 	"QCD_600to800_central_atOutput_*.root",
	# 	"QCD_800to1000_central_atOutput_*.root",
	# 	"QCD_80to120_central_atOutput_*.root",
	# ] ],

	["data_muon_tree.root", [
		"SingleMuon_RunB_central_atOutput_*.root",
		"SingleMuon_RunC_central_atOutput_*.root",
		"SingleMuon_RunD_central_atOutput_*.root",
		"SingleMuon_RunE_central_atOutput_*.root",
		"SingleMuon_RunF_central_atOutput_*.root",
		"SingleMuon_RunG_central_atOutput_*.root",
		"SingleMuon_RunH_Prompt_v2_central_atOutput_*.root",
		"SingleMuon_RunH_Prompt_v3_central_atOutput_*.root",
	], "C"],
	["data_electron_tree.root", [
		"SingleElectron_RunB_central_atOutput_*.root",
		"SingleElectron_RunC_central_atOutput_*.root",
		"SingleElectron_RunD_central_atOutput_*.root",
		"SingleElectron_RunE_central_atOutput_*.root",
		"SingleElectron_RunF_central_atOutput_*.root",
		"SingleElectron_RunG_central_atOutput_*.root",
		"SingleElectron_RunH_Prompt_v2_central_atOutput_*.root",
		"SingleElectron_RunH_Prompt_v3_central_atOutput_*.root"
	], "C"],

	# ["data_electron_B_tree.root", [
	# 	"SingleElectron_RunB_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_C_tree.root", [
	# 	"SingleElectron_RunC_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_D_tree.root", [
	# 	"SingleElectron_RunD_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_E_tree.root", [
	# 	"SingleElectron_RunE_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_F_tree.root", [
	# 	"SingleElectron_RunF_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_G_tree.root", [
	# 	"SingleElectron_RunG_central_atOutput_*.root"
	# ], "C"],

	# ["data_electron_H_tree.root", [
	# 	"SingleElectron_RunH_Prompt_v2_central_atOutput_*.root",
	# 	"SingleElectron_RunH_Prompt_v3_central_atOutput_*.root"
	# ], "C"],

]

mergingFiles = []
for job in jobTemplates:
	mergingFiles.append([job[0], job[1],"central"])
	if len(job) == 2:
		mergingFiles.append([job[0].replace("tree","plusJER_tree"),[f.replace("central","JetSmearing_up") for f in job[1] ],"JetSmearing_up"])
		mergingFiles.append([job[0].replace("tree","minusJER_tree"),[f.replace("central","JetSmearing_down") for f in job[1] ],"JetSmearing_down"])
		mergingFiles.append([job[0].replace("tree","plusJES_tree"),[f.replace("central","JES_up") for f in job[1] ],"JES_up"])
		mergingFiles.append([job[0].replace("tree","minusJES_tree"),[f.replace("central","JES_down") for f in job[1] ],"JES_down"])


