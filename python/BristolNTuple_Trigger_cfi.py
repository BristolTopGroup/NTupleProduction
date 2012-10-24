import FWCore.ParameterSet.Config as cms

rootTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    L1InputTag  = cms.InputTag('gtDigis'),
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    Prefix=cms.string('Trigger.'),
    Suffix=cms.string(''),
    HLTPathsOfInterest_Signal = cms.vstring(
    #========== 2011 data ==============  
    #ElectronHad PD
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v', 
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralDiJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30_v',
    #renaming for 1E33
    'HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v',
    #new iso triggers:
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v',
    #SingleElectron PD
    'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v',
    'HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v',
    #5E33 change to PF jets @ HLT
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralPFJet30_v',
    #control triggers
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_DiCentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralPFJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralPFJet30_v',
    #Muon Triggers
    #SingleMuon - last unprescaled in 1E33 menu
    'HLT_IsoMu17_v', 
    #MuHad
    'HLT_Mu17_CentralJet30_v', 
    'HLT_Mu17_DiCentralJet30_v',
    'HLT_Mu17_TriCentralJet30_v',
    #2E33
    'HLT_IsoMu17_CentralJet30_v',
    'HLT_IsoMu17_DiCentralJet30_v',
    'HLT_IsoMu17_QuadCentralJet30_v',
    'HLT_IsoMu17_TriCentralJet30_v',
    #3E33 - added eta requirement @ L1
    'HLT_IsoMu17_eta2p1_CentralJet30_BTagIP_v',
    'HLT_IsoMu17_eta2p1_CentralJet30_v',
    'HLT_IsoMu17_eta2p1_DiCentralJet30_v',
    'HLT_IsoMu17_eta2p1_QuadCentralJet30_v',
    'HLT_IsoMu17_eta2p1_TriCentralJet30_v',
    #5E33 change to PF jets @ HLT
    'HLT_IsoMu17_eta2p1_CentralPFJet30_v',
    'HLT_IsoMu17_eta2p1_DiCentralPFJet30_v',
    'HLT_IsoMu17_eta2p1_TriCentralPFJet30_v',
    'HLT_IsoMu17_eta2p1_QuadCentralPFJet30_v',
    #control triggers
    'HLT_Mu17_eta2p1_CentralPFJet30_v',
    'HLT_Mu17_eta2p1_DiCentralPFJet30_v',
    'HLT_Mu17_eta2p1_TriCentralPFJet30_v',
    'HLT_Mu17_eta2p1_QuadCentralPFJet30_v',
    #========== 2012 data ==============
    #data parking
    'HLT_Ele27_WP80_v',
    'HLT_IsoMu20_eta2p1_v',#needed for trigger efficiency
    #5E33 menu new triggers (rest is included in 2011 menu)
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet50_40_30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentrlJet50_40_30_v',#new backup trigger
    #
    'HLT_Mu20_eta2p1_TriCentralPFJet30_v',
    'HLT_Mu20_eta2p1_TriCentralPFJet50_40_30_v',
    'HLT_IsoMu20_eta2p1_CentralPFJet30_v',
    'HLT_IsoMu20_eta2p1_DiCentralPFJet30_v',
    'HLT_IsoMu20_eta2p1_TriCentralPFJet30_v',
    'HLT_IsoMu20_eta2p1_TriCentralPFJet50_40_30_v',
    #7E33 menu
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralPFNoPUJet30_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralPFNoPUJet50_40_30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFNoPUJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralPFNoPUJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFNoPUJet30_v',
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFNoPUJet50_40_30_v',
    #
    'HLT_Ele25_CaloIdVL_CaloIsoT_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet30_v',#anti-ID trigger DEV
    'HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet30_v',#stop signal trigger
    'HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet50_40_30_v',#stop signal trigger (backup)
    'HLT_Ele25_CaloIdVT_CaloIsoVL_TrkIdVL_TrkIsoT_TriCentralPFNoPUJet45_35_25_v',
    #
    'HLT_Mu20_eta2p1_TriCentralPFNoPUJet30_v',
    'HLT_Mu20_eta2p1_TriCentralPFNoPUJet50_40_30_v',
    'HLT_IsoMu20_eta2p1_CentralPFNoPUJet30_v',
    'HLT_IsoMu20_eta2p1_DiCentralPFNoPUJet30_v',
    'HLT_IsoMu20_eta2p1_TriCentralPFNoPUJet30_v',
    'HLT_IsoMu20_eta2p1_TriCentralPFNoPUJet50_40_30_v',
    #
    'HLT_Mu17_eta2p1_TriCentralPFNoPUJet30_v',
    'HLT_Mu17_eta2p1_TriCentralPFNoPUJet50_40_30_v',
    'HLT_IsoMu17_eta2p1_CentralPFNoPUJet30_v',
    'HLT_IsoMu17_eta2p1_DiCentralPFNoPUJet30_v',
    'HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_v',
    'HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet50_40_30_v',
    'HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet45_35_25_v',
    #triggers with lower 3rd jet threshold to combat missing JEC
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralPFNoPUJet30_30_20_v',
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralPFNoPUJet30_30_20_v',
    'HLT_IsoMu17_eta2p1_TriCentralPFNoPUJet30_30_20_v',
    'HLT_Mu17_eta2p1_TriCentralPFNoPUJet30_30_20_v',
    #new for 2011 SingleMu analysis
    'HLT_IsoMu24_v',
    'HLT_IsoMu24_eta2p1_v',
    'HLT_IsoMu30_v',
    'HLT_IsoMu30_eta2p1_v',
 ),                              
    HLTPathsOfInterest_Other = cms.vstring(
                                           #2010 data RunA + RunB
    'HLT_Ele10_LW_L1R', #0
    'HLT_Ele15_SW_L1R', #1
    'HLT_Ele15_SW_CaloEleId_L1R', #2
    'HLT_Ele17_SW_CaloEleId_L1R', #3
    'HLT_Ele17_SW_EleId_L1R', #4
    'HLT_Ele17_SW_LooseEleId_L1R', #5
    'HLT_Ele17_SW_TightEleIdIsol_L1R_v1', #6
    'HLT_Ele17_SW_TightEleId_L1R', #7
    'HLT_Ele17_SW_TighterEleIdIsol_L1R_v1', #8
    'HLT_Ele17_SW_TighterEleId_L1R_v1', #9
    'HLT_Ele22_SW_TighterEleId_L1R_v', #10
    'HLT_Ele27_SW_TightCaloEleIdTrack_L1R_v1', #11
))
