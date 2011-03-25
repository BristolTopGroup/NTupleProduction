import FWCore.ParameterSet.Config as cms

rootTupleJPTJets = cms.EDProducer("BristolNTuple_CaloJets",
    InputTag = cms.InputTag('patJetsAK5JPT'),
    Prefix = cms.string('JPTJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    ElectronPt = cms.double(30.),
    ElectronIso = cms.double(0.1),
    MuonPt = cms.double(10.),
    MuonIso = cms.double(0.05),
    JECUncertainty = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_Uncertainty_AK5JPT.txt'),
    ApplyResidualJEC = cms.bool(False),
    ResidualJEC = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_L2L3Residual_AK5JPT.txt')
)

#rootTupleJPTJetsExtra = cms.EDProducer("BristolNTuple_CaloJets_Extra",
#    InputTag = cms.InputTag('patJetsAK5JPT'),
#    Prefix = cms.string('JPTJet.'),
#    Suffix = cms.string(''),
#    MaxSize = cms.uint32(99),
#    JECUncertainty = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_Uncertainty_AK5JPT.txt'),
#    ApplyResidualJEC = cms.bool(False),
#    ResidualJEC = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_L2L3Residual_AK5JPT.txt')
#)

rootTupleJPTJetSequence = cms.Sequence(rootTupleJPTJets)# + rootTupleJPTJetsExtra)
