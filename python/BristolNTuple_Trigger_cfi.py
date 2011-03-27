import FWCore.ParameterSet.Config as cms

rootTupleTrigger = cms.EDProducer("BristolNTuple_Trigger",
    L1InputTag  = cms.InputTag('gtDigis'),
    HLTInputTag = cms.InputTag('TriggerResults','','HLT'),
    Prefix=cms.string('Trigger.'),
    Suffix=cms.string(''),                              
    HLTPathsOfInterest = cms.vstring(
#Double Electron
        'HLT_DoubleEle10_CaloIdL_TrkIdVL_Ele10_v1', #1
        'HLT_Ele17_CaloIdL_CaloIsoVL_Ele15_HFL_v1', #2
        'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v1', #3
        'HLT_Ele17_CaloIdL_CaloIsoVL_v1', #4
        'HLT_Ele17_CaloIdVT_CaloIsoVT_TrkIdT_TrkIsoVT_SC8_Mass30_v2', #5
        'HLT_Ele32_CaloIdL_CaloIsoVL_SC17_v1', #6
        'HLT_Ele8_CaloIdL_CaloIsoVL_Jet40_v1', #7
        'HLT_Ele8_CaloIdL_CaloIsoVL_v1', #8
        'HLT_Ele8_CaloIdL_TrkIdVL_v1', #9
        'HLT_Ele8_v1', #10
        'HLT_Photon20_CaloIdVT_IsoT_Ele8_CaloIdL_CaloIsoVL_v1', #11
        'HLT_TripleEle10_CaloIdL_TrkIdVL_v1', #12
#Double Muon
        'HLT_DoubleMu3_v3', #13
        'HLT_DoubleMu4_Acoplanarity03_v1', #14
        'HLT_DoubleMu6_v1', #15
        'HLT_DoubleMu7_v1', #16
        'HLT_L1DoubleMu0_v1', #17
        'HLT_L2DoubleMu0_v2', #18
        'HLT_L2DoubleMu35_NoVertex_v1', #19
        'HLT_Mu8_Jet40_v2', #20
        'HLT_TripleMu5_v2', #21
#ElectronHad
        'HLT_DoubleEle8_CaloIdL_TrkIdVL_HT160_v2', #22
        'HLT_DoubleEle8_CaloIdT_TrkIdVL_HT160_v2', #23
        'HLT_Ele10_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_HT200_v2', #24
        'HLT_Ele10_CaloIdT_CaloIsoVL_TrkIdT_TrkIsoVL_HT200_v2', #25
        'HLT_Ele25_CaloIdVT_TrkIdT_CentralDiJet30_v1', #26
        'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet30_v1', #27
        'HLT_Ele25_CaloIdVT_TrkIdT_CentralJet40_BTagIP_v1', #28
        'HLT_Ele25_CaloIdVT_TrkIdT_CentralTriJet30_v1', #29
#HT
        'HLT_DiJet100_PT100_v1', #30
        'HLT_DiJet130_PT130_v1', #31
        'HLT_DiJet70_PT70_v1', #32
        'HLT_HT160_v2', #33
        'HLT_HT240_v2', #34
        'HLT_HT260_MHT60_v2', #35
        'HLT_HT260_v2', #36
        'HLT_HT300_MHT75_v2', #37
        'HLT_HT300_v2', #38
        'HLT_HT360_v2', #39
        'HLT_HT440_v2', #40
        'HLT_HT520_v2', #41
        'HLT_MR100_v1', #42
        'HLT_Meff440_v2', #43
        'HLT_Meff520_v2', #44
        'HLT_Meff640_v2', #45
        'HLT_R032_MR100_v1', #46
        'HLT_R032_v1', #47
        'HLT_R035_MR100_v1', #48
#Jet
        'HLT_DiJetAve100U_v4', #49
        'HLT_DiJetAve140U_v4', #50
        'HLT_DiJetAve15U_v4', #51
        'HLT_DiJetAve180U_v4', #52
        'HLT_DiJetAve300U_v4', #53
        'HLT_DiJetAve30U_v4', #54
        'HLT_DiJetAve50U_v4', #55
        'HLT_DiJetAve70U_v4', #56
        'HLT_Jet110_v1', #57
        'HLT_Jet150_v1', #58
        'HLT_Jet190_v1', #59
        'HLT_Jet240_v1', #60
        'HLT_Jet30_v1', #61
        'HLT_Jet370_NoJetID_v1', #62
        'HLT_Jet370_v1', #63
        'HLT_Jet60_v1', #64
        'HLT_Jet80_v1', #65
#MET BTAG
        'HLT_BTagMu_DiJet20_Mu5_v1', #66
        'HLT_BTagMu_DiJet60_Mu7_v1', #67
        'HLT_BTagMu_DiJet80_Mu9_v1', #68
        'HLT_CentralJet80_MET100_v1', #69
        'HLT_CentralJet80_MET160_v1', #70
        'HLT_CentralJet80_MET65_v1', #71
        'HLT_CentralJet80_MET80_v1', #72
        'HLT_DiJet60_MET45_v1', #73
        'HLT_MET100_v1', #74
        'HLT_MET120_v1', #75
        'HLT_MET200_v1', #76
        'HLT_PFMHT150_v1', #77
        
#MuEG
        'HLT_DoubleMu5_Ele8_CaloIdL_TrkIdVL_v2', #78
        'HLT_DoubleMu5_Ele8_v2', #79
        'HLT_Mu10_Ele10_CaloIdL_v2', #80
        'HLT_Mu15_DoublePhoton15_CaloIdL_v2', #01
        'HLT_Mu15_Photon20_CaloIdL_v2', #82
        'HLT_Mu17_Ele8_CaloIdL_v1', #83
        'HLT_Mu5_DoubleEle8_v2', #84
        'HLT_Mu5_Ele8_CaloIdL_TrkIdVL_Ele8_v2', #85
        'HLT_Mu8_Ele17_CaloIdL_v1', #86
        'HLT_Mu8_Photon20_CaloIdVT_IsoT_v2', #87
        
#MuHad
        'HLT_DoubleMu3_HT160_v2', #88
        'HLT_DoubleMu3_HT200_v2', #89
        'HLT_IsoMu17_CentralJet40_BTagIP_v1', #90
        'HLT_Mu17_CentralJet30_v1', #91
        'HLT_Mu17_CentralJet40_BTagIP_v1', #92
        'HLT_Mu17_DiCentralJet30_v1', #93
        'HLT_Mu17_TriCentralJet30_v1', #94
        'HLT_Mu3_Ele8_CaloIdL_TrkIdVL_HT160_v2', #95
        'HLT_Mu3_Ele8_CaloIdT_TrkIdVL_HT160_v2', #96
        'HLT_Mu5_HT200_v3', #97
        'HLT_Mu8_HT200_v2', #98
#Muonia
        'HLT_DoubleMu3_Bs_v1', #99
        'HLT_DoubleMu3_Jpsi_v1', #100
        'HLT_DoubleMu3_Quarkonium_v1', #101
        'HLT_Mu3_Track3_Jpsi_v4', #102
        'HLT_Mu5_L2Mu2_Jpsi_v1', #103
        'HLT_Mu5_L2Mu2_v1', #104
        'HLT_Mu7_Track5_Jpsi_v1', #105
        'HLT_Mu7_Track7_Jpsi_v1', #106
#MultiJet
        'HLT_DoubleJet30_ForwardBackward_v1', #107
        'HLT_DoubleJet60_ForwardBackward_v1', #108
        'HLT_DoubleJet70_ForwardBackward_v1', #109
        'HLT_DoubleJet80_ForwardBackward_v1', #110
        'HLT_ExclDiJet60_HFAND_v1', #111
        'HLT_ExclDiJet60_HFOR_v1', #112
        'HLT_QuadJet40_IsoPFTau40_v1', #113
        'HLT_QuadJet40_v1', #114
        'HLT_QuadJet50_BTagIP_v1', #115
        'HLT_QuadJet50_Jet40_v1', #116
        'HLT_QuadJet60_v1', #117
        'HLT_QuadJet70_v1', #118
                                     
#Photon
    'HLT_DoublePhoton33_v1', #119
        'HLT_DoublePhoton5_IsoVL_CEP_v1', #120
        'HLT_Photon125_NoSpikeFilter_v1', #121
        'HLT_Photon20_R9Id_Photon18_R9Id_v1', #122
        'HLT_Photon26_CaloIdL_IsoVL_Photon18_CaloIdL_IsoVL_v1', #123
        'HLT_Photon26_CaloIdL_IsoVL_Photon18_v1', #124
        'HLT_Photon26_IsoVL_Photon18_IsoVL_v1', #125
        'HLT_Photon26_IsoVL_Photon18_v1', #126
        'HLT_Photon26_Photon18_v1', #127
        'HLT_Photon30_CaloIdVL_IsoL_v1', #128
        'HLT_Photon30_CaloIdVL_v1', #129
        'HLT_Photon32_CaloIdL_Photon26_CaloIdL_v1', #130
        'HLT_Photon75_CaloIdVL_IsoL_v1', #131
        'HLT_Photon75_CaloIdVL_v1', #132
        
#PhotonHad
        'HLT_Photon60_CaloIdL_HT200_v1', #133
        'HLT_Photon70_CaloIdL_HT200_v1', #134
        'HLT_Photon70_CaloIdL_HT300_v1', #135
        'HLT_Photon70_CaloIdL_MHT30_v1', #136
        'HLT_Photon70_CaloIdL_MHT50_v1', #137
#SingleElectron
    'HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', #138
        'HLT_Ele45_CaloIdVT_TrkIdT_v1', #139
        'HLT_Ele90_NoSpikeFilter_v1', #140
#SingleMu
        'HLT_IsoMu12_v1', #141
        'HLT_IsoMu15_v5', #142
        'HLT_IsoMu17_v5', #143
        'HLT_IsoMu24_v1', #144
        'HLT_IsoMu30_v1', #145
        'HLT_L1SingleMu10_v1', #146
        'HLT_L1SingleMu20_v1', #147
        'HLT_L2Mu10_v1', #148
        'HLT_L2Mu20_v1', #149
        'HLT_Mu12_v1', #150
        'HLT_Mu15_v2', #151
        'HLT_Mu20_v1', #152
        'HLT_Mu24_v1', #153
        'HLT_Mu30_v1', #154
        'HLT_Mu3_v3', #155
        'HLT_Mu5_v3', #156
        'HLT_Mu8_v1', #157
#Tau
    'HLT_DoubleIsoPFTau20_Trk5_v1', #158
        'HLT_IsoPFTau35_Trk20_MET45_v1', #159
#TauPlusX
    'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau15_v1', #160
        'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_LooseIsoPFTau20_v1', #161
        'HLT_Ele15_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v1', #162
        'HLT_Ele15_CaloIdVT_TrkIdT_LooseIsoPFTau15_v1', #163
        'HLT_IsoMu12_LooseIsoPFTau10_v1', #164
        'HLT_Mu15_LooseIsoPFTau20_v1' #165
))
