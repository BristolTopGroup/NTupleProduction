import FWCore.ParameterSet.Config as cms

rootTupleTriggerObjectElectronLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectElectronLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTTrkIdTCaloIsoTTrkIsoTTrackIsolFilter','','HLT'),  # from Ele25+TriJet trigger
)

rootTupleTriggerObjectMuonLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectMuonLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltL3IsoL1sMu14Eta2p1L1f0L2f14QL2IsoL3f24L3IsoFiltered','','HLT'), # from SingleMu24_eta2p1 trigger
)

rootTupleTriggerObjectQuadJets = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectQuadJets.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltQuadJet70','','HLT'), # from QuadJet70 trigger
)