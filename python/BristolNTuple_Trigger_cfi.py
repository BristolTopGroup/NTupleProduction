import FWCore.ParameterSet.Config as cms

rootTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    L1InputTag  = cms.InputTag('gtDigis'),
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    Prefix=cms.string('Trigger.'),
    Suffix=cms.string(''),
    HLTPathsOfInterest_Signal = cms.vstring(
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
    #========== 2011 data ==============  
    #ElectronHad PD
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet40_BTagIP_v', #12
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v', #13
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralDiJet30_v', #14
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30_v', #15
    #renaming for 1E33
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_BTagIP_v', #16
    'HLT_Ele25_CaloIdVT_TrkIdT_DiCentralJet30_v',#17
    'HLT_Ele25_CaloIdVT_TrkIdT_TriCentralJet30_v', #18
    'HLT_Ele25_CaloIdVT_TrkIdT_QuadCentralJet30_v', #19
    #new iso triggers:
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_BTagIP_v',#20
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_v',#21
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_DiCentralJet30_v',#22
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_TriCentralJet30_v',#23
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_QuadCentralJet30_v',#24
    #Higgs trigger
    'HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralJet30_CentralJet25_PFMHT20_v',#25
    #EWK triggers
    'HLT_Ele25_WP80_PFMT40_v',#26
    'HLT_Ele27_WP70_PFMT40_PFMHT20_v',#27
    
    
    #SingleElectron PD
    'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v', #28
    'HLT_Ele25_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v',#29
    'HLT_Ele32_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v',#30
    'HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v',#31
    
 ),                              
    HLTPathsOfInterest_Other = cms.vstring(
#ElectronHad
    'HLT_Ele10_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT200_v', #0
    'HLT_Ele10_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT200_v', #1
#HT
    'HLT_DiJet100_PT100_v', #2
    'HLT_DiJet130_PT130_v', #3
    'HLT_DiJet70_PT70_v', #4
    'HLT_HT300_MHT75_v', #5
    'HLT_Meff640_v', #6
#Jet
    'HLT_DiJetAve180U_v', #7
    'HLT_DiJetAve300U_v', #8
    'HLT_Jet240_v', #9
    'HLT_Jet370_NoJetID_v', #10
    'HLT_Jet370_v', #11
#MET BTAG
    'HLT_CentralJet80_MET100_v', #12
    'HLT_CentralJet80_MET160_v', #13
    'HLT_CentralJet80_MET65_v', #14
    'HLT_CentralJet80_MET80_v', #15
    'HLT_MET200_v', #16
    'HLT_PFMHT150_v', #17 
#MuHad
    'HLT_IsoMu17_CentralJet40_BTagIP_v', #18
    'HLT_Mu17_CentralJet30_v', #19
    'HLT_Mu17_CentralJet40_BTagIP_v', #20
    'HLT_Mu17_DiCentralJet30_v', #21
    'HLT_Mu17_TriCentralJet30_v', #22
    'HLT_Mu5_HT200_v', #23
    'HLT_Mu8_HT200_v', #24
#MultiJet
    'HLT_DoubleJet30_ForwardBackward_v', #25
    'HLT_DoubleJet60_ForwardBackward_v', #26
    'HLT_DoubleJet70_ForwardBackward_v', #27
    'HLT_DoubleJet80_ForwardBackward_v', #28
    'HLT_ExclDiJet60_HFAND_v', #29
    'HLT_QuadJet40_IsoPFTau40_v', #30
    'HLT_QuadJet50_BTagIP_v', #31
    'HLT_QuadJet50_Jet40_v', #32
    'HLT_QuadJet60_v', #33
    'HLT_QuadJet70_v', #34
                                     
#Photon
    'HLT_DoublePhoton33_v', #35
    'HLT_DoublePhoton5_IsoVL_CEP_v', #36
    'HLT_Photon125_NoSpikeFilter_v', #37
    'HLT_Photon20_R9Id_Photon18_R9Id_v', #38
    'HLT_Photon26_CaloIdL_IsoVL_Photon18_CaloIdL_IsoVL_v', #39
    'HLT_Photon26_CaloIdL_IsoVL_Photon18_v', #40
    'HLT_Photon26_IsoVL_Photon18_IsoVL_v', #41
    'HLT_Photon26_IsoVL_Photon18_v', #42
    'HLT_Photon26_Photon18_v', #43
    'HLT_Photon30_CaloIdVL_IsoL_v', #44
    'HLT_Photon30_CaloIdVL_v', #45
    'HLT_Photon32_CaloIdL_Photon26_CaloIdL_v', #46
    'HLT_Photon75_CaloIdVL_IsoL_v', #47
    'HLT_Photon75_CaloIdVL_v', #48
        
#PhotonHad
    'HLT_Photon60_CaloIdL_HT200_v', #49
    'HLT_Photon70_CaloIdL_HT200_v', #50
    'HLT_Photon70_CaloIdL_HT300_v', #51
    'HLT_Photon70_CaloIdL_MHT30_v', #52
    'HLT_Photon70_CaloIdL_MHT50_v', #53
#SingleElectron
    'HLT_Ele90_NoSpikeFilter_v', #54
#SingleMu
    'HLT_IsoMu12_v', #55
    'HLT_IsoMu15_v5', #56
    'HLT_IsoMu17_v5', #57
    'HLT_IsoMu24_v', #58
    'HLT_IsoMu30_v', #59
    'HLT_Mu15_v2', #60
    'HLT_Mu20_v', #61
    'HLT_Mu24_v', #62
    'HLT_Mu30_v', #63
#Tau
    'HLT_DoubleIsoPFTau20_Trk5_v', #64
    'HLT_IsoPFTau35_Trk20_MET45_v', #65
#TauPlusX
    'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau15_v', #66
    'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20_v', #67
    'HLT_IsoMu12_LooseIsoPFTau10_v', #68
    'HLT_Mu15_LooseIsoPFTau20_v' #69
))
