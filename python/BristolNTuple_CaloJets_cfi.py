import FWCore.ParameterSet.Config as cms

rootTupleCaloJets = cms.EDProducer("BristolNTuple_CaloJets",
    InputTag = cms.InputTag('cleanPatJets'),
    Prefix = cms.string('CaloJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    ElectronPt = cms.double(30.),
    ElectronIso = cms.double(0.1),
    MuonPt = cms.double(10.),
    MuonIso = cms.double(0.05),
    JECUncertainty = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_Uncertainty_AK5Calo.txt'),
    ApplyResidualJEC = cms.bool(False),
    ResidualJEC = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_L2L3Residual_AK5Calo.txt')
)

#rootTupleCaloJetsExtra = cms.EDProducer("BristolNTuple_CaloJets_Extra",
#    InputTag = cms.InputTag('cleanPatJets'),
#    Prefix = cms.string('CaloJet.'),
#    Suffix = cms.string(''),
#    MaxSize = cms.uint32(99)
#)

rootTupleCaloJetSequence = cms.Sequence(rootTupleCaloJets)# + rootTupleCaloJetsExtra)

