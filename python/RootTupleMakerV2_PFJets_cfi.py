import FWCore.ParameterSet.Config as cms

rootTuplePFJets = cms.EDProducer("RootTupleMakerV2_PFJets",
    InputTag = cms.InputTag('cleanPatJetsAK5PF'),
    Prefix = cms.string('PFJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_Uncertainty_AK5PF.txt'),
    ApplyResidualJEC = cms.bool(False),
    ResidualJEC = cms.string('CondFormats/JetMETObjects/data/Spring10DataV2_L2L3Residual_AK5PF.txt')
)


rootTuplePF2PATJets = rootTuplePFJets.clone(InputTag = cms.InputTag('selectedPatJetsPF'),
    Prefix = cms.string('PF2PATJet.'))

rootTuplePFJetsExtra = cms.EDProducer("RootTupleMakerV2_PFJets_Extra",
    InputTag = cms.InputTag('cleanPatJetsAK5PF'),
    Prefix = cms.string('PFJet.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(99)
)

rootTuplePF2PATJetsExtra = rootTuplePFJetsExtra.clone(InputTag = cms.InputTag('selectedPatJetsPF'),
    Prefix = cms.string('PF2PATJet.'))

rootTuplePFJetSequence = cms.Sequence(rootTuplePFJets + rootTuplePF2PATJets + rootTuplePFJetsExtra + 
                                      rootTuplePF2PATJetsExtra)