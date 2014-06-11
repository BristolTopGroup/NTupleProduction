import FWCore.ParameterSet.Config as cms

# electron+jets trigger objects
rootTupleTriggerObjectElectronLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectElectronLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTTrkIdTDphiFilter','','HLT'),  # electron leg of Ele25+TriJet trigger, runs 16404-165633
)

rootTupleTriggerObjectElectronIsoLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectElectronIsoLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTTrkIdTCaloIsoTTrkIsoTTrackIsolFilter','','HLT'),  # electron leg of Ele25+TriJet iso trigger, runs 165970-180252
)

rootTupleTriggerObjectHadronLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectHadronLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTTrkIdTCentralTriJet30Cleaned','','HLT'),  # hadron leg of Ele25+TriJet trigger, runs 16404-165633
)

rootTupleTriggerObjectHadronIsoLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectHadronIsoLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTCaloIsoTTrkIdTTrkIsoTCentralTriJet30EleCleaned','','HLT'),  # hadron leg of Ele25+TriJet iso trigger, runs 165970-178380
)

rootTupleTriggerObjectHadronPFIsoLeg = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectHadronPFIsoLeg.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltEle25CaloIdVTCaloIsoTTrkIdTTrkIsoTTriCentralPFJet30EleCleaned','','HLT'),  # hadron leg of Ele25+TriPFJet iso trigger, runs 178420-180252
)

# single muon trigger objects
rootTupleTriggerObjectMuon1 = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectMuon1.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltSingleMuIsoL3IsoFiltered24','','HLT'), # muon object of SingleMu24 trigger, V1-V7, runs 160404-167913
)

rootTupleTriggerObjectMuon2 = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectMuon2.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltSingleMuL2QualIsoL3IsoFiltered24','','HLT'), # muon object of SingleMu24 trigger, V8, runs 170249-173198
)

rootTupleTriggerObjectMuon2p1 = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectMuon2p1.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltL3IsoL1sMu14Eta2p1L1f0L2f14QL2IsoL3f24L3IsoFiltered','','HLT'), # muon object of SingleMu24_eta2p1 trigger, runs 173236-190456
)

# quad jet trigger objects
rootTupleTriggerObjectQuadJets = cms.EDProducer("BristolNTuple_TriggerObjects",
    HLTObjectsInputTag = cms.InputTag('hltTriggerSummaryAOD','','HLT'),   
    Prefix=cms.string('TriggerObjectQuadJets.'),
    Suffix=cms.string(''),
    HLTObjectOfInterest = cms.InputTag('hltQuadJet70','','HLT'), # from QuadJet70 trigger
)
