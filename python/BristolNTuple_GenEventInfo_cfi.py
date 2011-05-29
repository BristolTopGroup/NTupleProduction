import FWCore.ParameterSet.Config as cms

rootTupleGenEventInfo = cms.EDProducer("BristolNTuple_GenEventInfo",
    GenEventInfoInputTag = cms.InputTag('generator'),
    StorePDFWeights      = cms.bool(False),
    PDFWeightsInputTag   = cms.InputTag('pdfWeights','cteq65'),
    pileupInfo           = cms.InputTag('addPileupInfo'),
    Prefix=cms.string('Event.'),
    Suffix=cms.string('')
)
