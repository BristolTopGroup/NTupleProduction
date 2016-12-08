import sys
import os


jobTemplates = [
	# ["TTJets_PowhegPythia8_tree.root", [
	# 	"TTJets_PowhegPythia8_central_atOutput_*.root"
	# ] ],
	# ["TTJets_PowhegPythia8_scaleup_tree.root", [
	# 	"TTJets_PowhegPythia8_scaleup_central_atOutput_*.root"
	# ], "C" ],
	# ["TTJets_PowhegPythia8_scaledown_tree.root", [
	# 	"TTJets_PowhegPythia8_scaledown_central_atOutput_*.root"
	# ], "C" ],
	# ["TTJets_PowhegPythia8_mtop1695_tree.root", [
	# 	"TTJets_PowhegPythia8_mtop1695_central_atOutput_*.root"
	# ], "C" ],
	# ["TTJets_PowhegPythia8_mtop1755_tree.root", [
	# 	"TTJets_PowhegPythia8_mtop1755_central_atOutput_*.root"
	# ], "C" ],
	# ["TTJets_amc_tree.root", [
	# 	"TTJets_amcatnloFXFX_central_atOutput_*.root"
	# ], "C"],
	# ["TTJets_madgraph_tree.root", [
	# 	"TTJets_madgraphMLM_central_atOutput_*.root"
	# ], "C"],
	# ["TTJets_powhegHerwigpp_tree.root", [
	# 	"TTJets_PowhegHerwigpp_central_atOutput_*.root"
	# ], "C"],
	# # ["TTJets_PowhegPythia8_Moriond17_tree.root", [
	# # 	"TTJets_PowhegPythia8_Moriond17_central_atOutput_*.root"
	# # ] ],

	# ["SingleTop_tree.root", [
	# 	"ST_tW_central_atOutput_*.root"
	# ] ],
	# ["VJets_tree.root", [
	# 	"DYJetsToLL_M50_central_atOutput_*", 
	# 	"WJetsToLNu_central_atOutput_*"
	# ] ],
	# ["QCD_Electron_tree.root", [
	# 	"QCD_bcToE_*_central_atOutput_*", 
	# 	"QCD_EMEnriched_*_central_atOutput_*"
	# ] ],
	# ["QCD_Muon_tree.root", [
	# 	"QCD_MuEnriched_*_central_atOutput_*.root"
	# ] ],

	["data_muon_tree.root", [
		"SingleMuon_RunB_central_atOutput_*.root",
		"SingleMuon_RunC_central_atOutput_*.root",
		"SingleMuon_RunD_central_atOutput_*.root",
		"SingleMuon_RunE_central_atOutput_*.root",
		"SingleMuon_RunF_central_atOutput_*.root",
		"SingleMuon_RunG_central_atOutput_*.root",
		"SingleMuon_RunH_central_atOutput_*.root"
	], "C"],
	["data_electron_tree.root", [
		"SingleElectron_RunB_central_atOutput_*.root",
		"SingleElectron_RunC_central_atOutput_*.root",
		"SingleElectron_RunD_central_atOutput_*.root",
		"SingleElectron_RunE_central_atOutput_*.root",
		"SingleElectron_RunF_central_atOutput_*.root",
		"SingleElectron_RunG_central_atOutput_*.root",
		"SingleElectron_RunH_central_atOutput_*.root"
	], "C"],
]

mergingFiles = []
for job in jobTemplates:
	mergingFiles.append([job[0], job[1],"central"])
	if len(job) == 2:
		mergingFiles.append([job[0].replace("tree","plusJER_tree"),[f.replace("central","JetSmearing_up") for f in job[1] ],"JetSmearing_up"])
		mergingFiles.append([job[0].replace("tree","minusJER_tree"),[f.replace("central","JetSmearing_down") for f in job[1] ],"JetSmearing_down"])
		mergingFiles.append([job[0].replace("tree","plusJES_tree"),[f.replace("central","JES_up") for f in job[1] ],"JES_up"])
		mergingFiles.append([job[0].replace("tree","minusJES_tree"),[f.replace("central","JES_down") for f in job[1] ],"JES_down"])


