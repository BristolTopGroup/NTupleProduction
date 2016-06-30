from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from BristolAnalysis.NTupleTools.options import CMSSW_MAJOR_VERSION, registerOptions

# register options
options = registerOptions(VarParsing('python'))
isData = options.isData
isMC = not isData
isTTbarMC = options.isTTbarMC

# Define the CMSSW process
process = cms.Process("Ntuples")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
# process.MessageLogger.cout.FwkReport.reportEvery = 1000
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#process.MessageLogger.detailedInfo.threshold = 'DEBUG'

# Maximum Number of Events
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

# Set the process options -- Display summary at the end, enable
# unscheduled execution
process.options = cms.untracked.PSet(
    allowUnscheduled=cms.untracked.bool(True),
    wantSummary=cms.untracked.bool(False),
)

# print event content
process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")

# Source
process.source = cms.Source("PoolSource",
                            fileNames=cms.untracked.vstring(
                                'root://xrootd.unl.edu//store/data/Run2015C_25ns/SingleMuon/MINIAOD/16Dec2015-v1/00000/002C22D4-E1AF-E511-AE8E-001E673971CA.root',
                            )
                            )

# If you would like to change the Global Tag e.g. for JEC
globalTags = {
    'data': {
        7: '76X_dataRun2_16Dec2015_v0',  # ReReco+Prompt JECv6
        8: '80X_dataRun2_Prompt_v8',
    },
    'MC': {
        7: '76X_mcRun2_asymptotic_RunIIFall15DR76_v1',  # 25ns MC
        8: '80X_mcRun2_asymptotic_2016_v3',
    }
}

process.load(
    "Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
globaltag = ''
if (isData):
    globaltag = globalTags['data'][CMSSW_MAJOR_VERSION]
else:
    globaltag = globalTags['MC'][CMSSW_MAJOR_VERSION]
print("Using Global Tag:", globaltag)
process.GlobalTag.globaltag = cms.string(globaltag)
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
# process.load('JetMETCorrections.Configuration.CorrectedJetProducersDefault_cff')

if isTTbarMC:
    # TT Gen Event configuration
    from BristolAnalysis.NTupleTools.ttGenConfig_cff import setupTTGenEvent
    setupTTGenEvent( process, cms )

# Particle level definitions
from BristolAnalysis.NTupleTools.pseudoTopConfig_cff import setupPseudoTop
setupPseudoTop(process, cms)

# Electron VID
from BristolAnalysis.NTupleTools.ElectronID_cff import setup_electronID
setup_electronID(process, cms)

# Rerun HBHE filter and others
from BristolAnalysis.NTupleTools.metFilters_cfi import setupMETFilters
setupMETFilters(process, cms)

# Rerun MET
from BristolAnalysis.NTupleTools.MET_Setup_cff import setup_MET
setup_MET(process, cms, options)

# Custom JEC
from BristolAnalysis.NTupleTools.Jets_Setup_cff import setup_jets
setup_jets(process, cms, options)

# Load the selection filters and the selection analyzers
process.load('BristolAnalysis.NTupleTools.muonSelection_cff')
process.load('BristolAnalysis.NTupleTools.qcdMuonSelection_cff')
process.load('BristolAnalysis.NTupleTools.qcdElectronSelection_cff')
process.load('BristolAnalysis.NTupleTools.electronSelection_cff')
process.load('BristolAnalysis.NTupleTools.SelectionCriteriaAnalyzer_cfi')

if options.tagAndProbe:
    process.topPairEPlusJetsSelection.tagAndProbeStudies = cms.bool(True)
    process.topPairEPlusJetsSelectionTagging.tagAndProbeStudies = cms.bool(
        True)
    process.topPairEPlusJetsSelection.jetSelectionInTaggingMode = cms.bool(
        True)
    process.topPairEPlusJetsSelectionTagging.jetSelectionInTaggingMode = cms.bool(
        True)

# Maximum Number of Events
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

from BristolAnalysis.NTupleTools.NTupler_cff import setup_ntupler
setup_ntupler(process, cms)

process.nTupleGenEventInfo.isTTbarMC = cms.bool(isTTbarMC)

if isTTbarMC:
    process.makingNTuples = cms.Path(
        # process.metFilters *
        process.egmGsfElectronIDSequence *
        process.reapplyJEC *
        process.electronSelectionAnalyzerSequence *
        process.muonSelectionAnalyzerSequence *
        process.qcdMuonSelectionAnalyzerSequence *
        process.qcdElectronSelectionAnalyzerSequence *
        process.ttGenEvent *
        process.selectionCriteriaAnalyzer *
        process.makePseudoTop *
        process.printEventContent *
        process.nTuples *
        process.nTupleTree
    )
else:
    process.makingNTuples = cms.Path(
        # process.metFilters *
        process.egmGsfElectronIDSequence *
        process.reapplyJEC *
        process.electronSelectionAnalyzerSequence *
        process.muonSelectionAnalyzerSequence *
        process.qcdMuonSelectionAnalyzerSequence *
        process.qcdElectronSelectionAnalyzerSequence *
        process.selectionCriteriaAnalyzer *
        process.printEventContent *
        process.nTuples *
        process.nTupleTree
    )

process.nTupleTree.outputCommands.append(
    'keep uint*_topPairMuPlusJetsSelectionTagging_*_*')
process.nTupleTree.outputCommands.append(
    'keep uint*_topPairMuPlusJetsQCDSelectionTagging1_*_*')
process.nTupleTree.outputCommands.append(
    'keep uint*_topPairMuPlusJetsQCDSelectionTagging2_*_*')
process.nTupleTree.outputCommands.append(
    'keep uint*_topPairEPlusJetsSelectionTagging_*_*')
process.nTupleTree.outputCommands.append(
    'keep uint*_topPairEPlusJetsQCDSelectionTagging_*_*')
process.nTupleTree.outputCommands.append(
    'keep uint*_topPairEPlusJetsConversionSelectionTagging_*_*')

process.nTupleTree.outputCommands.append(
    'keep bool_topPairMuPlusJetsSelectionTagging_*_*')
process.nTupleTree.outputCommands.append(
    'keep bool_topPairMuPlusJetsQCDSelectionTagging1_*FullSelection*_*')
process.nTupleTree.outputCommands.append(
    'keep bool_topPairMuPlusJetsQCDSelectionTagging2_*FullSelection*_*')
process.nTupleTree.outputCommands.append(
    'keep bool_topPairEPlusJetsSelectionTagging_*_*')
process.nTupleTree.outputCommands.append(
    'keep bool_topPairEPlusJetsQCDSelectionTagging_*FullSelection*_*')
process.nTupleTree.outputCommands.append(
    'keep bool_topPairEPlusJetsConversionSelectionTagging_*FullSelection*_*')

if isMC:
    # Remove 76X Data 25ns Triggers
    process.triggerSequence.remove(process.nTupleTriggerEle22erWPLooseGsf)
    process.triggerSequence.remove(process.nTupleTriggerEle23WPLooseGsf)
    process.triggerSequence.remove(process.nTupleTriggerIsoMu18)
    process.triggerSequence.remove(process.nTupleTriggerIsoMu20)
    process.triggerSequence.remove(process.nTupleTriggerIsoTkMu20)
    process.triggerSequence.remove(process.nTupleTrigger)

    # Delete removed modules
    del process.nTupleTriggerEle22erWPLooseGsf, process.nTupleTriggerEle23WPLooseGsf
    del process.nTupleTriggerIsoMu18, process.nTupleTriggerIsoMu20, process.nTupleTriggerIsoTkMu20
    del process.nTupleTrigger

if isData:
    # Remove 76X MC 25ns Triggers
    process.triggerSequence.remove(process.nTupleTriggerEle22erWPLooseGsfMC)
    process.triggerSequence.remove(process.nTupleTriggerEle23WPLooseGsfMC)
    process.triggerSequence.remove(process.nTupleTriggerIsoMu18MC)
    process.triggerSequence.remove(process.nTupleTriggerIsoMu20MC)
    process.triggerSequence.remove(process.nTupleTriggerIsoTkMu20MC)
    process.triggerSequence.remove(process.nTupleTrigger)

    # Remove PseudoTop and MC Gen Variables
    process.makingNTuples.remove(process.makePseudoTop)
    process.nTuples.remove(process.pseudoTopSequence)
    process.nTuples.remove(process.nTupleGenMET)
    process.nTuples.remove(process.nTupleGenJets)
    process.nTuples.remove(process.nTupleGenEventInfo)
    process.nTuples.remove(process.nTupleGenParticles)
    # Do not keep Gen branches
    process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
    # Delete removed modules and sequences (So they do not run on unscheduled)
    del process.makePseudoTop, process.pseudoTopSequence, process.pseudoTop
    del process.nTuplePseudoTopJets, process.nTuplePseudoTopLeptons, process.nTuplePseudoTopNeutrinos, process.nTuplePseudoTops
    del process.nTupleGenMET, process.nTupleGenJets,  process.nTupleGenEventInfo, process.nTupleGenParticles
    del process.nTupleTriggerEle22erWPLooseGsfMC, process.nTupleTriggerEle23WPLooseGsfMC
    del process.nTupleTriggerIsoMu18MC, process.nTupleTriggerIsoMu20MC, process.nTupleTriggerIsoTkMu20MC
    del process.nTupleTrigger

if not options.isTTbarMC:
    print('Not a ttbar MC - removing TTbar specific modules')
    process.selectionCriteriaAnalyzer.genSelectionCriteriaInput = cms.VInputTag()
    
# 76X datasets are all ReReco so far
process.nTupleEvent.metFiltersInputTag = cms.InputTag(
    'TriggerResults', '', 'PAT')

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)

process.TFileService = cms.Service(
    "TFileService",
    fileName=cms.string('ntuple.root')
)

# new
# potential pre-skimming on objects
# process.skimmedPatElectrons = cms.EDFilter(
#     "PATElectronSelector",
#     src=cms.InputTag('slimmedElectrons'),
#     cut=cms.string("pt > 10 && abs(eta) < 2.5")
# )

process.load('BristolAnalysis.NTupleTools.userdata.ElectronUserData_cfi')
process.nTupleElectrons.InputTag = 'electronUserData'
process.topPairEPlusJetsSelection.electronInput = 'electronUserData'
process.topPairEPlusJetsSelectionTagging.electronInput = 'electronUserData'
process.topPairEPlusJetsConversionSelectionTagging.electronInput = 'electronUserData'
process.topPairEPlusJetsQCDSelectionTagging.electronInput = 'electronUserData'
process.topPairMuPlusJetsSelectionTagging.electronInput = 'electronUserData'
process.topPairMuPlusJetsQCDSelectionTagging1.electronInput = 'electronUserData'
process.topPairMuPlusJetsQCDSelectionTagging2.electronInput = 'electronUserData'

# EDM NTuples
# process.load('BristolAnalysis.NTupleTools.content')
#
# process.ntuples = cms.OutputModule(
#     "PoolOutputModule",
#     fileName=cms.untracked.string('ntuple.root'),
#     outputCommands=cms.untracked.vstring(
#         "drop *",
#         "keep *_electrons_*_*",
#     ),
#     dropMetaData=cms.untracked.string('ALL'),
# )
#
# process.endPath = cms.EndPath(process.ntuples)
