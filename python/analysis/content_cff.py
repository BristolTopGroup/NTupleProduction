import FWCore.ParameterSet.Config as cms

from BristolAnalysis.NTupleTools.rootTupleMaker_cfi import rootTupleMaker
analysisTree = rootTupleMaker.clone(
    treeName='FitVariables',
    outputCommands=[
        'drop *',
        'keep bool_topPairEPlusJetsSelectionTagging_*_*',
        'keep *_globalVariablesElectron_*_*',
    ],
)

from BristolAnalysis.NTupleTools.analysis.variableProducer_cfi import variableProducer
globalVariablesElectron = variableProducer.clone(
    channel='electron',
    prefix='EPlusJets.',
)
