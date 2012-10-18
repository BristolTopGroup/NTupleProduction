import FWCore.ParameterSet.Config as cms

rootTupleGenEventInfo = cms.EDProducer("BristolNTuple_GenEventInfo",
    GenEventInfoInputTag = cms.InputTag('generator'),
    StorePDFWeights      = cms.bool(True),
    PUWeightsInputTag   = cms.InputTag('eventWeightPU'),
    PDFWeightsInputTag   = cms.InputTag('pdfWeights','cteq66'),
    pileupInfo           = cms.InputTag('addPileupInfo'),
    Prefix               = cms.string('Event.'),
    Suffix               = cms.string(''),
)
