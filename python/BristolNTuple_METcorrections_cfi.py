import FWCore.ParameterSet.Config as cms

rootTupleSysShiftMetCorrections = cms.EDProducer("BristolNTuple_METcorrections",
    InputTag=cms.InputTag('pfMEtSysShiftCorr'),
    Prefix=cms.string('pfMetSysShiftCorrections.'),
    Suffix=cms.string(''),
)

rootTupleType0MetCorrections = cms.EDProducer("BristolNTuple_METcorrections",
    InputTag=cms.InputTag("patPFMETtype0CorrPFlow"),
    Prefix=cms.string('pfMetType0Corrections.'),
    Suffix=cms.string(''),
)

rootTupleType1MetCorrections = cms.EDProducer("BristolNTuple_METcorrections",
    InputTag=cms.InputTag("patPFJetMETtype1p2CorrPFlow","type1"),
    Prefix=cms.string('pfMetType1Corrections.'),
    Suffix=cms.string(''),
)