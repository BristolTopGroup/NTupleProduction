import FWCore.ParameterSet.Config as cms

eventWeightPU = cms.EDProducer("EventWeight_Producer_PU",
                               
    PUSource            = cms.InputTag("addPileupInfo"),
    WeightName          = cms.string("eventWeightPU"),                           

    MCSampleTag         = cms.string("Summer12"),  # valid identifier: Fall11, Summer12                               
                               
    MCSampleFile        = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/MC_PUDist_Default2012.root"),
    MCSampleHistoName   = cms.string("puhisto"),
    DataFile            = cms.FileInPath("BristolAnalysis/NTupleTools/data/PileUp/Data_PUDist_2012Full.root"),
    DataHistoName       = cms.string("pileup"),

)
