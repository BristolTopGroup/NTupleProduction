import FWCore.ParameterSet.Config as cms

eventWeightPU = cms.EDProducer("EventWeightPU",
                               
    PUSource            = cms.InputTag("addPileupInfo"),
    WeightName          = cms.string("eventWeightPU"),                           

    MCSampleTag         = cms.string("Fall11"),  # valid identifier: Fall11, Summer12                               
                               
    MCSampleFile        = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2011.root"),
    MCSampleHistoName   = cms.string("histo_Fall11_true"),
    DataFile            = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2011Full.root"),
    DataHistoName       = cms.string("histoData_true"),

)
