import FWCore.ParameterSet.Config as cms

nTuplePseudoTopJets = cms.EDProducer("BristolNTuple_GenJets",
    InputTag = cms.InputTag('pseudoTop','jets','Ntuples'),
    Prefix = cms.string('PseudoTopJets.'),
    Suffix = cms.string(''),
    minPt = cms.double(15),
    maxAbsoluteEta = cms.double(999),
    MaxSize = cms.uint32(99)
)

nTuplePseudoTopLeptons = cms.EDProducer("BristolNTuple_GenJets",
    InputTag = cms.InputTag('pseudoTop','leptons','Ntuples'),
    Prefix = cms.string('PseudoTopLeptons.'),
    Suffix = cms.string(''),
    minPt = cms.double(15),
    maxAbsoluteEta = cms.double(999),
    MaxSize = cms.uint32(99)
)

nTuplePseudoTopNeutrinos = cms.EDProducer("BristolNTuple_GenParticles",
    InputTag = cms.InputTag('pseudoTop','neutrinos','Ntuples'),
    Prefix = cms.string('PseudoTopNeutrinos.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(25)
)

nTuplePseudoTopMETs = cms.EDProducer("BristolNTuple_RecoMET",
    InputTag = cms.InputTag('pseudoTop','mets','Ntuples'),
    Prefix = cms.string('PseudoTopMETs.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(25)
)

nTuplePseudoTops = cms.EDProducer("BristolNTuple_GenParticles",
    InputTag = cms.InputTag('pseudoTop','','Ntuples'),
    Prefix = cms.string('PseudoTops.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(25)
)

pseudoTopSequence = cms.Sequence(
    nTuplePseudoTopJets *
    nTuplePseudoTopLeptons *
    nTuplePseudoTopNeutrinos *
    nTuplePseudoTopMETs *
    nTuplePseudoTops
)
