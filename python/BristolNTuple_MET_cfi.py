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