import FWCore.ParameterSet.Config as cms

rootTupleCaloJets = cms.EDProducer("BristolNTuple_CaloJets",
    InputTag = cms.InputTag('cleanPatJets'),
    Prefix = cms.string('CaloJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_Uncertainty_AK5Calo.txt'),
#    ApplyResidualJEC = cms.bool(False),
#    ResidualJEC = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_L2L3Residual_AK5Calo.txt')
)

rootTupleCaloJetSequence = cms.Sequence(rootTupleCaloJets)

