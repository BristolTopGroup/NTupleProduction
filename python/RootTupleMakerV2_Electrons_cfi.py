import FWCore.ParameterSet.Config as cms

rootTupleElectrons = cms.EDProducer("RootTupleMakerV2_Electrons",
    TracksInputTag = cms.InputTag('generalTracks'),
    DCSInputTag = cms.InputTag('scalersRawToDigi'),
    InputTag = cms.InputTag('cleanPatElectrons'),
    Prefix = cms.string('Electron.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(20),
    ElectronIso = cms.double(0.1),
    MuonPt = cms.double(10.),
    MuonIso = cms.double(0.05),
    MuonID = cms.string('GlobalMuonPromptTight'),
    VertexInputTag = cms.InputTag('offlinePrimaryVertices')
)

rootTuplePFElectrons = rootTupleElectrons.clone(
    InputTag = cms.InputTag('selectedPatElectronsPF'),
    Prefix = cms.string('PFElectron.'))

rootTupleElectronsExtra = cms.EDProducer("RootTupleMakerV2_Electrons_Extra",
    InputTag = cms.InputTag('cleanPatElectrons'),
    InputTagPVWithBS = cms.InputTag('cleanPatEle2'),
    InputTagBS = cms.InputTag('cleanPatEle3'),
    Prefix = cms.string('Electron.'),
    Suffix = cms.string(''),
    MaxSize = cms.uint32(20),
    storePFIsolation = cms.bool(False)
)

rootTuplePFElectronsExtra = rootTupleElectronsExtra.clone(
    InputTag = cms.InputTag('selectedPatElectronsPF'),
    Prefix = cms.string('PFElectron.'),
    storePFIsolation = cms.bool(True))

rootTupleElectronSequence =  cms.Sequence(rootTupleElectrons + rootTuplePFElectrons + rootTupleElectronsExtra + 
                                          rootTuplePFElectronsExtra)