import FWCore.ParameterSet.Config as cms

nTuplePFJets = cms.EDProducer("BristolNTuple_PFJets",
    InputTag = cms.InputTag('patJetsReapplyJEC'),
    Prefix = cms.string('Jets.'),
    Suffix = cms.string(''),
    minJetPtToStore = cms.double(20.),
    MaxSize = cms.uint32(99),
    JECUncertainty = cms.string('AK4PFchs'),
    ReadJECuncertainty = cms.bool(True),
    ReadJEC = cms.bool(False),
    JetCorrectionService = cms.string('ak4PFCHSL1FastL2L3'),    
    DoVertexAssociation = cms.bool(True),
    VertexInputTag = cms.InputTag('offlineSlimmedPrimaryVertices'),
    isRealData = cms.bool(False),
    looseBTagWP = cms.double(0.460),
    mediumBTagWP = cms.double(0.800),
    tightBTagWP = cms.double(0.935),    
    btagCalibrationFile = cms.string('CSVv2.csv')
#     btagCalibrationFile = cms.string)'BristolAnalysis/NTupleTools/data/BTagSF/CSVv2.csv'),
#     btagCalibrationFile = cms.string('/vagrant/data/BTagSF/CSVv2.csv'),
)
