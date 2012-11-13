import FWCore.ParameterSet.Config as cms

#Calo MET
rootTupleCaloMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patMETs'),
    Prefix=cms.string('patMETs.'),
    Suffix=cms.string(''),
)

#Type1 (by default) corrected PFMET from PAT - default to use. Identical to patType1CorrectedPFMetPFlow
#Jets collection used: pfJetsPFlow (anti-kt)
rootTuplePFMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patMETsPFlow'),
    Prefix=cms.string('patMETsPFlow.'),
    Suffix=cms.string(''),
 )

#Type1 corrected PFMET coming from PAT MET uncertainty sequence
#Jets collection used: ak5PFJets
rootTuplePFType1CorrectedMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMet'),
    Prefix=cms.string('patType1CorrectedPFMet.'),
    Suffix=cms.string(''),
 )

#Type1p2 corrected PFMET coming from PAT MET uncertainty sequence
#Jets collection used: ak5PFJets
rootTuplePFType1p2CorrectedMET = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMet'),
    Prefix=cms.string('patType1p2CorrectedPFMet.'),
    Suffix=cms.string(''),
 )

#Type1p2 corrected PFMET from PAT
#Jets collection used: pfJetsPFlow (anti-kt)
rootTuplePFType1p2CorrectedMetPFlow = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1p2CorrectedPFMetPFlow'),
    Prefix=cms.string('patType1p2CorrectedPFMetPFlow.'),
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
rootTupleType1CorrectedPFMetElectronEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetElectronEnUp'),
    Prefix=cms.string('patType1CorrectedPFMetElectronEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetElectronEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetElectronEnDown'),
    Prefix=cms.string('patType1CorrectedPFMetElectronEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetMuonEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetMuonEnUp'),
    Prefix=cms.string('patType1CorrectedPFMetMuonEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetMuonEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetMuonEnDown'),
    Prefix=cms.string('patType1CorrectedPFMetMuonEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetTauEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetTauEnUp'),
    Prefix=cms.string('patType1CorrectedPFMetTauEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetTauEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetTauEnDown'),
    Prefix=cms.string('patType1CorrectedPFMetTauEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetJetResUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetJetResUp'),
    Prefix=cms.string('patType1CorrectedPFMetJetResUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetJetResDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetJetResDown'),
    Prefix=cms.string('patType1CorrectedPFMetJetResDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetJetEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetJetEnUp'),
    Prefix=cms.string('patType1CorrectedPFMetJetEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetJetEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetJetEnDown'),
    Prefix=cms.string('patType1CorrectedPFMetJetEnDown.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetUnclusteredEnUp = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetUnclusteredEnUp'),
    Prefix=cms.string('patType1CorrectedPFMetUnclusteredEnUp.'),
    Suffix=cms.string(''),
 )

rootTupleType1CorrectedPFMetUnclusteredEnDown = cms.EDProducer("BristolNTuple_MET",
    InputTag=cms.InputTag('patType1CorrectedPFMetUnclusteredEnDown'),
    Prefix=cms.string('patType1CorrectedPFMetUnclusteredEnDown.'),
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
