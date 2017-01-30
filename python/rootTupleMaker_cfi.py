import FWCore.ParameterSet.Config as cms

rootTupleMaker = cms.EDAnalyzer(
    "RootTupleMakerV2_Tree",
    treeName=cms.string('test'),
    outputCommands=cms.untracked.vstring(
        'drop *',
    )
)
