import FWCore.ParameterSet.Config as cms

indexProducer = cms.EDProducer(
    "IndexProducer",
    # name of the output branch
    outputName=cms.string('example.collectionIndices'),
    # original collection, e.g. slimmedElectrons
    originalCollection=cms.InputTag('originalCollection'),
    # new collection, subset of original, e.g. goodElectrons
    newCollection=cms.InputTag('newCollection'),
)
