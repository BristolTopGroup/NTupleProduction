import FWCore.ParameterSet.Config as cms

rootTupleCaloMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patMETs'),
    Prefix=cms.string('patMETs.'),
    Suffix=cms.string(''),
)

rootTuplePFMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patMETsPFlow'),
    Prefix=cms.string('patMETsPFlow.'),
    Suffix=cms.string(''),
 )

rootTuplePFType1CorrectedMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMet'),
    Prefix=cms.string('patType1CorrectedPFMet.'),
    Suffix=cms.string(''),
 )

rootTuplePFType1p2CorrectedMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMet'),
    Prefix=cms.string('patType1p2CorrectedPFMet.'),
    Suffix=cms.string(''),
 )

#MET systematics

rootTuplePFMetElectronEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetElectronEnUp'),
    Prefix=cms.string('patPFMetElectronEnUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetElectronEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetElectronEnDown'),
    Prefix=cms.string('patPFMetElectronEnDown.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetMuonEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetMuonEnUp'),
    Prefix=cms.string('patPFMetMuonEnUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetMuonEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetMuonEnDown'),
    Prefix=cms.string('patPFMetMuonEnDown.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetTauEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetTauEnUp'),
    Prefix=cms.string('patPFMetTauEnUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetTauEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetTauEnDown'),
    Prefix=cms.string('patPFMetTauEnDown.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetJetResUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetJetResUp'),
    Prefix=cms.string('patPFMetJetResUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetJetResDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetJetResDown'),
    Prefix=cms.string('patPFMetJetResDown.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetJetEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetJetEnUp'),
    Prefix=cms.string('patPFMetJetEnUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetJetEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetJetEnDown'),
    Prefix=cms.string('patPFMetJetEnDown.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetUnclusteredEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetUnclusteredEnUp'),
    Prefix=cms.string('patPFMetUnclusteredEnUp.'),
    Suffix=cms.string(''),
 )

rootTuplePFMetUnclusteredEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patPFMetUnclusteredEnDown'),
    Prefix=cms.string('patPFMetUnclusteredEnDown.'),
    Suffix=cms.string(''),
 )
#Type I MET uncertainties
rootTupleType1pCorrectedPFMetElectronEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetElectronEnUp'),
    Prefix=cms.string('patType1pCorrectedPFMetElectronEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetElectronEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetElectronEnDown'),
    Prefix=cms.string('patType1pCorrectedPFMetElectronEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetMuonEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetMuonEnUp'),
    Prefix=cms.string('patType1pCorrectedPFMetMuonEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetMuonEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetMuonEnDown'),
    Prefix=cms.string('patType1pCorrectedPFMetMuonEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetTauEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetTauEnUp'),
    Prefix=cms.string('patType1pCorrectedPFMetTauEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetTauEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetTauEnDown'),
    Prefix=cms.string('patType1pCorrectedPFMetTauEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetJetResUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetJetResUp'),
    Prefix=cms.string('patType1pCorrectedPFMetJetResUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetJetResDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetJetResDown'),
    Prefix=cms.string('patType1pCorrectedPFMetJetResDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetJetEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetJetEnUp'),
    Prefix=cms.string('patType1pCorrectedPFMetJetEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetJetEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetJetEnDown'),
    Prefix=cms.string('patType1pCorrectedPFMetJetEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetUnclusteredEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetUnclusteredEnUp'),
    Prefix=cms.string('patType1pCorrectedPFMetUnclusteredEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1pCorrectedPFMetUnclusteredEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1pCorrectedPFMetUnclusteredEnDown'),
    Prefix=cms.string('patType1pCorrectedPFMetUnclusteredEnDown.'),
    Suffix=cms.string(''),
 )
#Type 1 + 2 MET uncertainties
rootTupleType1p2CorrectedPFMetElectronEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetElectronEnUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetElectronEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetElectronEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetElectronEnDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetElectronEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetMuonEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetMuonEnUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetMuonEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetMuonEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetMuonEnDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetMuonEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetTauEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetTauEnUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetTauEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetTauEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetTauEnDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetTauEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetJetResUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetJetResUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetJetResUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetJetResDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetJetResDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetJetResDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetJetEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetJetEnUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetJetEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetJetEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetJetEnDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetJetEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetUnclusteredEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetUnclusteredEnUp'),
    Prefix=cms.string('patType1p2CorrectedPFMetUnclusteredEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1p2CorrectedPFMetUnclusteredEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetUnclusteredEnDown'),
    Prefix=cms.string('patType1p2CorrectedPFMetUnclusteredEnDown.'),
    Suffix=cms.string(''),
 )
