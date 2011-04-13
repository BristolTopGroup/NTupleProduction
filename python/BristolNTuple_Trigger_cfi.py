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
    'HLT_Ele22_SW_TighterEleId_L1R_v2', #10
    'HLT_Ele22_SW_TighterEleId_L1R_v3', #11
    'HLT_Ele27_SW_TightCaloEleIdTrack_L1R_v1', #12   
    #2011 data  
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralDiJet30_v1', #13
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v1', #14
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet40_BTagIP_v1', #15
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30_v1', #16
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralDiJet30_v2', #17
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v2', #18
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet40_BTagIP_v2', #19
    'HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30_v2', #20
    #additional triggers to recover boosted top
    'HLT_Ele10_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT200_v2', #21
    'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', #22
    'HLT_Ele45_CaloIdVT_TrkIdT_v1', #23
    'HLT_Ele10_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT200_v3', #24
    'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v2', #25
    'HLT_Ele45_CaloIdVT_TrkIdT_v2', #26
 ),                              
    HLTPathsOfInterest_Other = cms.vstring(
#ElectronHad
        'HLT_Ele10_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT200_v2', #0
        'HLT_Ele10_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT200_v3', #1
        
#HT
    'HLT_DiJet100_PT100_v1', #2
    'HLT_DiJet130_PT130_v1', #3
    'HLT_DiJet70_PT70_v1', #4
    'HLT_HT300_MHT75_v2', #5
    'HLT_Meff640_v2', #6
#Jet
    'HLT_DiJetAve180U_v4', #7
    'HLT_DiJetAve300U_v4', #8
    'HLT_Jet240_v1', #9
    'HLT_Jet370_NoJetID_v1', #10
    'HLT_Jet370_v1', #11
#MET BTAG
    'HLT_CentralJet80_MET100_v1', #12
    'HLT_CentralJet80_MET160_v1', #13
    'HLT_CentralJet80_MET65_v1', #14
    'HLT_CentralJet80_MET80_v1', #15
    'HLT_MET200_v1', #16
    'HLT_PFMHT150_v1', #17 
#MuHad
        'HLT_IsoMu17_CentralJet40_BTagIP_v1', #18
        'HLT_Mu17_CentralJet30_v1', #19
        'HLT_Mu17_CentralJet40_BTagIP_v1', #20
        'HLT_Mu17_DiCentralJet30_v1', #21
        'HLT_Mu17_TriCentralJet30_v1', #22
        'HLT_Mu5_HT200_v3', #23
        'HLT_Mu8_HT200_v2', #24
#MultiJet
        'HLT_DoubleJet30_ForwardBackward_v1', #25
        'HLT_DoubleJet60_ForwardBackward_v1', #26
        'HLT_DoubleJet70_ForwardBackward_v1', #27
        'HLT_DoubleJet80_ForwardBackward_v1', #28
        'HLT_ExclDiJet60_HFAND_v1', #29
        'HLT_QuadJet40_IsoPFTau40_v1', #30
        'HLT_QuadJet50_BTagIP_v1', #31
        'HLT_QuadJet50_Jet40_v1', #32
        'HLT_QuadJet60_v1', #33
        'HLT_QuadJet70_v1', #34
                                     
#Photon
    'HLT_DoublePhoton33_v1', #35
        'HLT_DoublePhoton5_IsoVL_CEP_v1', #36
        'HLT_Photon125_NoSpikeFilter_v1', #37
        'HLT_Photon20_R9Id_Photon18_R9Id_v1', #38
        'HLT_Photon26_CaloIdL_IsoVL_Photon18_CaloIdL_IsoVL_v1', #39
        'HLT_Photon26_CaloIdL_IsoVL_Photon18_v1', #40
        'HLT_Photon26_IsoVL_Photon18_IsoVL_v1', #41
        'HLT_Photon26_IsoVL_Photon18_v1', #42
        'HLT_Photon26_Photon18_v1', #43
        'HLT_Photon30_CaloIdVL_IsoL_v1', #44
        'HLT_Photon30_CaloIdVL_v1', #45
        'HLT_Photon32_CaloIdL_Photon26_CaloIdL_v1', #46
        'HLT_Photon75_CaloIdVL_IsoL_v1', #47
        'HLT_Photon75_CaloIdVL_v1', #48
        
#PhotonHad
        'HLT_Photon60_CaloIdL_HT200_v1', #49
        'HLT_Photon70_CaloIdL_HT200_v1', #50
        'HLT_Photon70_CaloIdL_HT300_v1', #51
        'HLT_Photon70_CaloIdL_MHT30_v1', #52
        'HLT_Photon70_CaloIdL_MHT50_v1', #53
#SingleElectron
        'HLT_Ele90_NoSpikeFilter_v1', #54
#SingleMu
        'HLT_IsoMu12_v1', #55
        'HLT_IsoMu15_v5', #56
        'HLT_IsoMu17_v5', #57
        'HLT_IsoMu24_v1', #58
        'HLT_IsoMu30_v1', #59
        'HLT_Mu15_v2', #60
        'HLT_Mu20_v1', #61
        'HLT_Mu24_v1', #62
        'HLT_Mu30_v1', #63
#Tau
    'HLT_DoubleIsoPFTau20_Trk5_v1', #64
        'HLT_IsoPFTau35_Trk20_MET45_v1', #65
#TauPlusX
    'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau15_v1', #66
        'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20_v1', #67
        'HLT_IsoMu12_LooseIsoPFTau10_v1', #68
        'HLT_Mu15_LooseIsoPFTau20_v1' #69
))
