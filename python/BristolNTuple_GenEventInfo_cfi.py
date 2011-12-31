import FWCore.ParameterSet.Config as cms

rootTupleGenEventInfo = cms.EDProducer("BristolNTuple_GenEventInfo",
    GenEventInfoInputTag = cms.InputTag('generator'),
    StorePDFWeights      = cms.bool(False),
    isFall11MC           = cms.bool(False),
    PDFWeightsInputTag   = cms.InputTag('pdfWeights','cteq65'),
    pileupInfo           = cms.InputTag('addPileupInfo'),
    Prefix               = cms.string('Event.'),
    Suffix               = cms.string(''),
    dataPileUpFile       = cms.string('BristolAnalysis/NTupleTools/data/PileUp/PileUp_2011_truth_finebin.root'),
    PossionShiftUp       = cms.double(0.5),
    PossionShiftDown       = cms.double(-0.5),
)
