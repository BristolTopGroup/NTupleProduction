import FWCore.ParameterSet.Config as cms

rootTupleGenEventInfo = cms.EDProducer("BristolNTuple_GenEventInfo",
    GenEventInfoInputTag = cms.InputTag('generator'),
    StorePDFWeights      = cms.bool(False),
    #TODO: remove Fall11 switch
    isFall11MC           = cms.bool(True),
    PDFWeightsInputTag   = cms.InputTag('pdfWeights','cteq65'),
    pileupInfo           = cms.InputTag('addPileupInfo'),
    Prefix               = cms.string('Event.'),
    Suffix               = cms.string(''),
    dataPileUpFile       = cms.string('PileUp_2011_truth_finebin.root'),
    PossionShiftUp       = cms.double(0.5),
    PossionShiftDown       = cms.double(-0.5),
)
