from __future__ import print_function

DATASETS = {
    "25ns": {
        "DYJetsToLL_M50": "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "GJets_15toInf": "/GJet_Pt-15ToInf_TuneCUETP8M1_13TeV-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_120to170": "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_15to20": "/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_170to300": "/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_20to30": "/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_300toInf": "/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_30to50": "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_50to80": "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_EMEnriched_80to120": "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_1000toInf": "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_120to170": "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_15to20": "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_170to300": "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_20to30": "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_300to470": "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_30to50": "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
        "QCD_MuEnriched_470to600": "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_50to80": "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_600to800": "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v4/MINIAODSIM",
        "QCD_MuEnriched_800to1000": "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_MuEnriched_80to120": "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_bcToE_15to20": "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_bcToE_170to250": "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_bcToE_20to30": "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_bcToE_250toInf": "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_bcToE_30to80": "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "QCD_bcToE_80to170": "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "SingleElectron_PromptReco_RunD": "/SingleElectron/Run2015D-PromptReco-v4/MINIAOD",
        "SingleElectron_ReReco_RunC": "/SingleElectron/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        "SingleElectron_ReReco_RunD": "/SingleElectron/Run2015D-05Oct2015-v1/MINIAOD",
        "SingleMuon_PromptReco_RunD": "/SingleMuon/Run2015D-PromptReco-v4/MINIAOD",
        "SingleMuon_ReReco_RunC": "/SingleMuon/Run2015C_25ns-05Oct2015-v1/MINIAOD",
        "SingleMuon_ReReco_RunD": "/SingleMuon/Run2015D-05Oct2015-v1/MINIAOD",
        "TTJets_PowhegPythia8": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1695": "/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1755": "/TT_TuneCUETP8M1_mtop1755_13TeV-powheg-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaledown": "/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaleup": "/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v3/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1695": "/TTJets_mtop1695_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1755": "/TTJets_mtop1755_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_amcatnloHerwigpp": "/TT_TuneEE5C_13TeV-amcatnlo-herwigpp/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTJets_madgraphMLM": "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "TTZToLLNUNU_M10": "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
        "TToLeptons_t": "/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "T_tW": "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v2/MINIAODSIM",
        "Tbar_tW": "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM",
        "WJetsToLNu": "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"
    },
    "50ns": {
        "DYJetsToLL_M50": "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "GJets_15to6000": "/GJet_Pt-15To6000_TuneCUETP8M1-Flat_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "QCD_EMEnriched_120to170": "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_15to20": "/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_170to300": "/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_20to30": "/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_300toInf": "/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM",
        "QCD_EMEnriched_30to50": "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_50to80": "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_EMEnriched_80to120": "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v3/MINIAODSIM",
        "QCD_MuEnriched_1000toInf": "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "QCD_MuEnriched_120to170": "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "QCD_MuEnriched_15to20": "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "QCD_MuEnriched_170to300": "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "QCD_MuEnriched_20to30": "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "QCD_MuEnriched_300to470": "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "QCD_MuEnriched_30to50": "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "QCD_MuEnriched_470to600": "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "QCD_MuEnriched_50to80": "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "QCD_MuEnriched_600to800": "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "QCD_MuEnriched_800to1000": "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "QCD_MuEnriched_80to120": "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "QCD_bcToE_15to20": "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_bcToE_170to250": "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_bcToE_20to30": "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v1/MINIAODSIM",
        "QCD_bcToE_250toInf": "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM",
        "QCD_bcToE_30to80": "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM",
        "QCD_bcToE_80to170": "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/MINIAODSIM",
        "TTJets_PowhegHerwigpp": "/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_PowhegPythia6Tauola": "/TT_TuneZ2star_13TeV-powheg-pythia6-tauola/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "TTJets_PowhegPythia8": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v4/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1695": "/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1755": "/TT_TuneCUETP8M1_mtop1755_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaledown": "/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaleup": "/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "TTJets_amcatnloFXFX": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1695": "/TTJets_mtop1695_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v3/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1755": "/TTJets_mtop1755_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_scaledown": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "TTJets_amcatnloFXFX_scaleup": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaleup-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "TTJets_madgraphMLM": "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "TToLeptons_t": "/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "T_tW": "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v1/MINIAODSIM",
        "Tbar_tW": "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring15DR74-Asympt50ns_MCRUN2_74_V9A-v2/MINIAODSIM",
        "WJetsToLNu": "/WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v1/MINIAODSIM"
    },
    "FALL15": {
        "DYJetsToLL_M50": "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "GJets_100to200": "/GJets_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "GJets_200to400": "/GJets_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "GJets_400to600": "/GJets_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "GJets_600toInf": "/GJets_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_120to170": "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_15to20": "/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_170to300": "/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_20to30": "/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_300toInf": "/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_30to50": "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_50to80": "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_EMEnriched_80to120": "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_1000toInf": "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM",
        "QCD_MuEnriched_120to170": "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_170to300": "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_20to30": "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_300to470": "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_30to50": "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_470to600": "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_50to80": "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_600to800": "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v3/MINIAODSIM",
        "QCD_MuEnriched_800to1000": "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_MuEnriched_80to120": "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_bcToE_15to20": "/QCD_Pt_15to20_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_bcToE_170to250": "/QCD_Pt_170to250_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_bcToE_20to30": "/QCD_Pt_20to30_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_bcToE_250toInf": "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "QCD_bcToE_30to80": "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v2/MINIAODSIM",
        "QCD_bcToE_80to170": "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "SingleElectron_16Dec2015_RunC": "/SingleElectron/Run2015C_25ns-16Dec2015-v1/MINIAOD",
        "SingleElectron_16Dec2015_RunD": "/SingleElectron/Run2015D-16Dec2015-v1/MINIAOD",
        "SingleMuon_16Dec2015_RunC": "/SingleMuon/Run2015C_25ns-16Dec2015-v1/MINIAOD",
        "SingleMuon_16Dec2015_RunD": "/SingleMuon/Run2015D-16Dec2015-v1/MINIAOD",
        "TTJets_PowhegHerwigpp": "/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_PowhegPythia8": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext3-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1695": "/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12_ext1-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1755": "/TT_TuneCUETP8M1_mtop1755_13TeV-powheg-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaledown": "/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaleup": "/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1695": "/TTJets_mtop1695_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_mtop1755": "/TTJets_mtop1755_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_scaledown": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaledown-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX_scaleup": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-scaleup-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_amcatnloHerwigpp": "/TT_TuneEE5C_13TeV-amcatnlo-herwigpp/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TTJets_madgraphMLM": "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "TToLeptons_t": "/ST_t-channel_5f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "T_tW": "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "Tbar_tW": "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM",
        "WJetsToLNu": "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/MINIAODSIM"
    },
    "PHYS14": {
        "DYJetsToLL_M50_PU20bx25": "/DYJetsToLL_M-50_13TeV-madgraph-pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "GJets_100to200_PU20bx25": "/GJets_HT-100to200_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "GJets_200to400_PU20bx25": "/GJets_HT-200to400_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "GJets_400to600_PU20bx25": "/GJets_HT-400to600_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "GJets_600toInf_PU20bx25": "/GJets_HT-600toInf_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "QCD_EMEnriched_20to30_PU20bx25": "/QCD_Pt-20to30_EMEnriched_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_castor_PHYS14_25_V1-v2/MINIAODSIM",
        "QCD_EMEnriched_30to80_PU20bx25": "/QCD_Pt-30to80_EMEnriched_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_castor_PHYS14_25_V1-v1/MINIAODSIM",
        "QCD_EMEnriched_80to170_PU20bx25": "/QCD_Pt-80to170_EMEnriched_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_castor_PHYS14_25_V1-v1/MINIAODSIM",
        "QCD_MuEnriched_20toInf_PU20bx25": "/QCD_Pt-20toInf_MuEnrichedPt15_PionKaonDecay_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v3/MINIAODSIM",
        "QCD_MuEnriched_30to50_PU20bx25": "/QCD_Pt-30to50_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_PHYS14_25_V3-v2/MINIAODSIM",
        "QCD_MuEnriched_50to80_PU20bx25": "/QCD_Pt-50to80_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1/MINIAODSIM",
        "QCD_MuEnriched_80to120_PU20bx25": "/QCD_Pt-80to120_MuEnrichedPt5_PionKaonDecay_Tune4C_13TeV_pythia8/Phys14DR-AVE20BX25_tsg_PHYS14_25_V3-v1/MINIAODSIM",
        "QCD_bcToE_170toInf_PU20bx25": "/QCD_Pt_170toInf_bcToE_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "QCD_bcToE_20to30_PU20bx25": "/QCD_Pt_20to30_bcToE_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v2/MINIAODSIM",
        "QCD_bcToE_30to80_PU20bx25": "/QCD_Pt_30to80_bcToE_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v2/MINIAODSIM",
        "QCD_bcToE_80to170_PU20bx25": "/QCD_Pt_80to170_bcToE_Tune4C_13TeV_pythia8/Phys14DR-PU20bx25_PHYS14_25_V1-v2/MINIAODSIM",
        "TBarToLeptons_s_PU20bx25": "/TBarToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TBarToLeptons_t_PU20bx25": "/TBarToLeptons_t-channel_Tune4C_CSA14_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TTJets_Madgraph_PU20bx25": "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TTJets_Madgraph_PU30bx50": "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU30bx50_PHYS14_25_V1-v1/MINIAODSIM",
        "TTJets_Madgraph_PU4bx50": "/TTJets_MSDecaysCKM_central_Tune4C_13TeV-madgraph-tauola/Phys14DR-PU4bx50_PHYS14_25_V1-v1/MINIAODSIM",
        "TT_Pythia8_PU20bx25": "/TT_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM",
        "TT_Pythia8_PU20bx25_mass1755": "/TT_mass1755_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TT_Pythia8_PU20bx25_scaleup": "/TT_scaleup_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TT_Pythia8_PU30bx50": "/TT_Tune4C_13TeV-pythia8-tauola/Phys14DR-AVE30BX50_tsg_PHYS14_ST_V1-v1/MINIAODSIM",
        "TT_Pythia8_PU40bx25": "/TT_Tune4C_13TeV-pythia8-tauola/Phys14DR-PU40bx25_tsg_PHYS14_25_V1-v1/MINIAODSIM",
        "TToLeptons_s_PU20bx25": "/TToLeptons_s-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "TToLeptons_t_PU20bx25": "/TToLeptons_t-channel-CSA14_Tune4C_13TeV-aMCatNLO-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "T_tW_PU20bx25": "/T_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "Tbar_tW_PU20bx25": "/Tbar_tW-channel-DR_Tune4C_13TeV-CSA14-powheg-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM",
        "WJets_PU20bx25": "/WJetsToLNu_13TeV-madgraph-pythia8-tauola/Phys14DR-PU20bx25_PHYS14_25_V1-v1/MINIAODSIM"
    },
    "Spring16": {
        "DYJetsToLL_M50": "/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM",
        "QCD_MuEnriched_15to20": "/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_20to30": "/QCD_Pt-20to30_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_30to50": "/QCD_Pt-30to50_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_50to80": "/QCD_Pt-50to80_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_80to120": "/QCD_Pt-80to120_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_120to170": "/QCD_Pt-120to170_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_170to300": "/QCD_Pt-170to300_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_300to470": "/QCD_Pt-300to470_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_470to600": "/QCD_Pt-470to600_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_600to800": "/QCD_Pt-600to800_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_800to1000": "/QCD_Pt-800to1000_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_MuEnriched_1000toInf": "/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_bcToE_30to80": "/QCD_Pt_30to80_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM",
        "QCD_bcToE_80to170": "/QCD_Pt_80to170_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv1-PUSpring16_80X_mcRun2_asymptotic_2016_v3-v2/MINIAODSIM",
        "QCD_bcToE_250toInf": "/QCD_Pt_250toInf_bcToE_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "QCD_EMEnriched_15to20": "/QCD_Pt-15to20_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_EMEnriched_20to30": "/QCD_Pt-20to30_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_EMEnriched_30to50": "/QCD_Pt-30to50_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_EMEnriched_50to80": "/QCD_Pt-50to80_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_EMEnriched_80to120": "/QCD_Pt-80to120_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "QCD_EMEnriched_120to170": "/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-FlatPU8to37HcalNZSRAW_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "QCD_EMEnriched_170to300": "/QCD_Pt-170to300_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "QCD_EMEnriched_300toInf": "/QCD_Pt-300toInf_EMEnriched_TuneCUETP8M1_13TeV_pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "SingleElectron_Run2016B_PromptReco_v2": "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
        "SingleElectron_Run2016C_PromptReco_v2": "/SingleElectron/Run2016C-PromptReco-v2/MINIAOD",
        "SingleElectron_Run2016D_PromptReco_v2": "/SingleElectron/Run2016D-PromptReco-v2/MINIAOD",
        "SingleElectron_Run2016E_PromptReco_v2": "/SingleElectron/Run2016E-PromptReco-v2/MINIAOD",
        "SingleElectron_Run2016F_PromptReco_v1": "/SingleElectron/Run2016F-PromptReco-v1/MINIAOD",
        "SingleMuon_Run2016B_PromptReco_v2": "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
        "SingleMuon_Run2016C_PromptReco_v2": "/SingleMuon/Run2016C-PromptReco-v2/MINIAOD",
        "SingleMuon_Run2016D_PromptReco_v2": "/SingleMuon/Run2016D-PromptReco-v2/MINIAOD",
        "SingleMuon_Run2016E_PromptReco_v2": "/SingleMuon/Run2016E-PromptReco-v2/MINIAOD",
        "SingleMuon_Run2016F_PromptReco_v1": "/SingleMuon/Run2016F-PromptReco-v1/MINIAOD",
        "TTJets_PowhegPythia8": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaledown": "/TT_TuneCUETP8M1_13TeV-powheg-scaledown-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaleup": "/TT_TuneCUETP8M1_13TeV-powheg-scaleup-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1695": "/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1755": "/TT_TuneCUETP8M1_mtop1755_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/MINIAODSIM",
        "TTJets_PowhegHerwigpp": "/TT_TuneEE5C_13TeV-powheg-herwigpp/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "TTJets_amcatnloFXFX": "/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "TTJets_madgraphMLM": "/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "TTZToLLNUNU_M10": "/TTZToLLNuNu_M-10_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "ST_tW": "/ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "STbar_tW": "/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v2/MINIAODSIM",
        "ST_s": "/ST_s-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "STbar_t": "/ST_t-channel_antitop_4f_leptonDecays_13TeV-powheg-pythia8_TuneCUETP8M1/RunIISpring16MiniAODv2-PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/MINIAODSIM",
        "WJetsToLNu": "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_Moriond17": "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM"
    },
    "Moriond17": {
        "SingleElectron_RunB_Rereco_v3" : "/SingleElectron/Run2016B-23Sep2016-v3/MINIAOD",
        "SingleElectron_RunC_Rereco_v1" : "/SingleElectron/Run2016C-23Sep2016-v1/MINIAOD",
        "SingleElectron_RunD_Rereco_v1" : "/SingleElectron/Run2016D-23Sep2016-v1/MINIAOD",
        "SingleElectron_RunE_Rereco_v1" : "/SingleElectron/Run2016E-23Sep2016-v1/MINIAOD",
        "SingleElectron_RunF_Rereco_v1" : "/SingleElectron/Run2016F-23Sep2016-v1/MINIAOD",
        "SingleElectron_RunG_Rereco_v1" : "/SingleElectron/Run2016G-23Sep2016-v1/MINIAOD",
        "SingleMuon_RunB_Rereco_v3"     : "/SingleMuon/Run2016B-23Sep2016-v3/MINIAOD",
        "SingleMuon_RunC_Rereco_v1"     : "/SingleMuon/Run2016C-23Sep2016-v1/MINIAOD",
        "SingleMuon_RunD_Rereco_v1"     : "/SingleMuon/Run2016D-23Sep2016-v1/MINIAOD",
        "SingleMuon_RunE_Rereco_v1"     : "/SingleMuon/Run2016E-23Sep2016-v1/MINIAOD",
        "SingleMuon_RunF_Rereco_v1"     : "/SingleMuon/Run2016F-23Sep2016-v1/MINIAOD",
        "SingleMuon_RunG_Rereco_v1"     : "/SingleMuon/Run2016G-23Sep2016-v1/MINIAOD",

        "TTJets_PowhegPythia8"          : "/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM"
        "TTJets_PowhegPythia8_mtop1695" : "/TT_TuneCUETP8M1_mtop1695_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_mtop1755" : "/TT_TuneCUETP8M1_mtop1755_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaleup" : "/TT_TuneCUETP8M1up_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "TTJets_PowhegPythia8_scaledown" : "/TT_TuneCUETP8M1down_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",

        # "ST_tW": "",
        # "STbar_tW": "",
        # "ST_s": "",
        # "STbar_t": "",

        "DY1JetsToLL": "/DY1JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "DY2JetsToLL": "/DY2JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "DY3JetsToLL": "/DY3JetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",
        "DYBBJetsToLL": "/DYBBJetsToLL_M-10to70_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring16MiniAODv2-premix_withHLT_80X_mcRun2_asymptotic_v14-v1/MINIAODSIM",

        # "WJetsToLNu": "",


    },
    "Test": {
        "SingleElectron": "/SingleElectron/Run2016B-PromptReco-v2/MINIAOD",
        "SingleMuon": "/SingleMuon/Run2016B-PromptReco-v2/MINIAOD",
        "TTJets_PowhegPythia8": "/TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/MINIAODSIM",
        "WJetsToLNu": "/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISpring16MiniAODv2-PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext1-v1/MINIAODSIM"
    }
}


def get_dataset_name(cfg):
    dataset = '<not found>'
    with open(cfg) as f:
        for line in f.readlines():
            if line.startswith('config.Data.inputDataset'):
                dataset = line.split('=')[-1]
                dataset = dataset.strip()
                dataset = dataset.replace("'", '')
    return dataset


def create_sample_list():
    import os
    import glob
    from ntp import NTPROOT
    CRAB_CFG_DIR = os.path.join(NTPROOT, 'python', 'crab')
    cfgs = glob.glob(CRAB_CFG_DIR + '/*/*.py')

    samples = {}
    for cfg in cfgs:
        if '__init__.py' in cfg:
            continue
        campaign, alias = cfg.split('/')[-2:]
        alias = alias.replace('.py', '')
        dataset = get_dataset_name(cfg)
        if not campaign in samples:
            samples[campaign] = {}
        samples[campaign][alias] = dataset

    return samples


def datasets_to_str(datasets):
    """
        This function prints out all existing datasets in the JSON format.
        The output can then be copied & pasted to set the value of 'DATASETS'
        in crab.datasets.
    """
    import json
    return str(json.dumps(datasets, indent=4, sort_keys=True))

if __name__ == '__main__':
    samples = create_sample_list()
    print(datasets_to_str(samples))
