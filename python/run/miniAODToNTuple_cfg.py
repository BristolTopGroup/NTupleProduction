from __future__ import print_function
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from BristolAnalysis.NTupleTools.options import CMSSW_MAJOR_VERSION, registerOptions, is2015, is2016

# register options
options = registerOptions(VarParsing('python'))
isData = options.isData
isMC = not isData
isTTbarMC = options.isTTbarMC
isReHLT = options.isReHLT

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
        8: '80X_dataRun2_Prompt_ICHEP16JEC_v0',
    },
    'MC': {
        7: '76X_mcRun2_asymptotic_RunIIFall15DR76_v1',  # 25ns MC
        8: '80X_mcRun2_asymptotic_2016_miniAODv2_v1',
    }
}

process.load(
    "Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
globaltag = ''
if (isData):
    globaltag = globalTags['data'][CMSSW_MAJOR_VERSION]
else:
    globaltag = globalTags['MC'][CMSSW_MAJOR_VERSION]
process.GlobalTag.globaltag = cms.string(globaltag)
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
# process.load('JetMETCorrections.Configuration.CorrectedJetProducersDefault_cff')
if CMSSW_MAJOR_VERSION == '7':
    print("Running on 2015 Data")
else:
    print("Running on 2016 Data")
print("Using Global Tag:", globaltag)

if isTTbarMC:
    # TT Gen Event configuration
    from BristolAnalysis.NTupleTools.ttGenConfig_cff import setupTTGenEvent
    setupTTGenEvent(process, cms)

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
process.load('BristolAnalysis.NTupleTools.muonSelections_cff')
process.load('BristolAnalysis.NTupleTools.electronSelections_cff')
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

# mapping between MiniAOD collections and our object selections
process.load('BristolAnalysis.NTupleTools.indices_cff')


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
        process.indexSequence *
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
        process.indexSequence *
        process.printEventContent *
        process.nTuples *
        process.nTupleTree
    )

process.nTupleTree.outputCommands.extend(
    [
        'keep uint*_topPairMuPlusJetsSelectionTagging_*_*',
        'keep uint*_topPairMuPlusJetsQCDSelectionTagging1_*_*',
        'keep uint*_topPairMuPlusJetsQCDSelectionTagging2_*_*',
        'keep uint*_topPairEPlusJetsSelectionTagging_*_*',
        'keep uint*_topPairEPlusJetsQCDSelectionTagging_*_*',
        'keep uint*_topPairEPlusJetsConversionSelectionTagging_*_*',
        'keep bool_topPairMuPlusJetsSelectionTagging_*_*',
        'keep bool_topPairMuPlusJetsQCDSelectionTagging1_*FullSelection*_*',
        'keep bool_topPairMuPlusJetsQCDSelectionTagging2_*FullSelection*_*',
        'keep bool_topPairEPlusJetsSelectionTagging_*_*',
        'keep bool_topPairEPlusJetsQCDSelectionTagging_*FullSelection*_*',
        'keep bool_topPairEPlusJetsConversionSelectionTagging_*FullSelection*_*',
        'keep uint*_*Indices*_*_*',
    ]
)

# Remove trigger choices to separate input config???
if is2015:
    process.nTuples.remove(process.triggerSequence2016)
    if isMC:
        # Remove 76X Data 25ns Triggers
        process.triggerSequence2015.remove(
            process.nTupleTriggerEle23WPLooseGsf)
        process.triggerSequence2015.remove(process.nTupleTriggerIsoMu20)
        process.triggerSequence2015.remove(process.nTupleTriggerIsoTkMu20)
        process.triggerSequence2015.remove(process.nTupleTrigger)
        del process.nTupleTriggerEle23WPLooseGsf
        del process.nTupleTriggerIsoMu20, process.nTupleTriggerIsoTkMu20
        del process.nTupleTrigger

    if isData:
        # Remove 76X MC 25ns Triggers
        process.triggerSequence2015.remove(
            process.nTupleTriggerEle23WPLooseGsfMC)
        process.triggerSequence2015.remove(process.nTupleTriggerIsoMu20MC)
        process.triggerSequence2015.remove(process.nTupleTriggerIsoTkMu20MC)
        process.triggerSequence2015.remove(process.nTupleTrigger)
        del process.nTupleTriggerEle23WPLooseGsfMC
        del process.nTupleTriggerIsoMu20MC, process.nTupleTriggerIsoTkMu20MC
        del process.nTupleTrigger

        # Remove PseudoTop and MC Gen Variables
        process.makingNTuples.remove(process.makePseudoTop)
        process.nTuples.remove(process.pseudoTopSequence)
        process.nTuples.remove(process.nTupleGenMET)
        process.nTuples.remove(process.nTupleGenJets)
        process.nTuples.remove(process.nTupleGenEventInfo)
        process.nTuples.remove(process.nTupleGenParticles)
        # Do not keep Gen branches
        process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
        # Delete removed modules and sequences (So they do not run on
        # unscheduled)
        del process.makePseudoTop, process.pseudoTopSequence, process.pseudoTop
        del process.nTuplePseudoTopJets, process.nTuplePseudoTopLeptons, process.nTuplePseudoTopNeutrinos, process.nTuplePseudoTops
        del process.nTupleGenMET, process.nTupleGenJets,  process.nTupleGenEventInfo, process.nTupleGenParticles

if is2016:
    process.nTuples.remove(process.triggerSequence2015)
    if isMC:
        if isReHLT:
            process.nTupleTriggerEle27WPTightGsfMC.HLTInputTag = cms.InputTag(
                'TriggerResults', '', 'HLT2')
            process.nTupleTriggerIsoMu22MC.HLTInputTag = cms.InputTag(
                'TriggerResults', '', 'HLT2')
            process.nTupleTriggerIsoTkMu22MC.HLTInputTag = cms.InputTag(
                'TriggerResults', '', 'HLT2')
        # Remove 76X Data 25ns Triggers
        process.triggerSequence2016.remove(
            process.nTupleTriggerEle27WPTightGsf)
        process.triggerSequence2016.remove(process.nTupleTriggerIsoMu22)
        process.triggerSequence2016.remove(process.nTupleTriggerIsoTkMu22)
        process.triggerSequence2016.remove(process.nTupleTrigger)
        del process.nTupleTriggerEle27WPTightGsf
        del process.nTupleTriggerIsoMu22, process.nTupleTriggerIsoTkMu22
        del process.nTupleTrigger

    if isData:
        # Remove 76X MC 25ns Triggers
        process.triggerSequence2016.remove(
            process.nTupleTriggerEle27WPTightGsfMC)
        process.triggerSequence2016.remove(process.nTupleTriggerIsoMu22MC)
        process.triggerSequence2016.remove(process.nTupleTriggerIsoTkMu22MC)
        process.triggerSequence2016.remove(process.nTupleTrigger)
        del process.nTupleTriggerEle27WPTightGsfMC
        del process.nTupleTriggerIsoMu22MC, process.nTupleTriggerIsoTkMu22MC
        del process.nTupleTrigger
        # Remove PseudoTop and MC Gen Variables
        process.makingNTuples.remove(process.makePseudoTop)
        process.nTuples.remove(process.pseudoTopSequence)
        process.nTuples.remove(process.nTupleGenMET)
        process.nTuples.remove(process.nTupleGenJets)
        process.nTuples.remove(process.nTupleGenEventInfo)
        process.nTuples.remove(process.nTupleGenParticles)
        # Do not keep Gen branches
        process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
        # Delete removed modules and sequences (So they do not run on
        # unscheduled)
        del process.makePseudoTop, process.pseudoTopSequence, process.pseudoTop
        del process.nTuplePseudoTopJets, process.nTuplePseudoTopLeptons, process.nTuplePseudoTopNeutrinos, process.nTuplePseudoTops
        del process.nTupleGenMET, process.nTupleGenJets,  process.nTupleGenEventInfo, process.nTupleGenParticles

if not isTTbarMC:
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
if is2016:
    if isReHLT:
        process.topPairEPlusJetsSelection.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairEPlusJetsSelectionTagging.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairEPlusJetsConversionSelectionTagging.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairEPlusJetsQCDSelectionTagging.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairMuPlusJetsSelection.HLTInput.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairMuPlusJetsSelectionTagging.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairMuPlusJetsQCDSelectionTagging1.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')
        process.topPairMuPlusJetsQCDSelectionTagging2.HLTInput = cms.InputTag(
            'TriggerResults', '', 'HLT2')

process.load('BristolAnalysis.NTupleTools.userdata.ElectronUserData_cfi')
process.load('BristolAnalysis.NTupleTools.userdata.MuonUserData_cfi')
process.load('BristolAnalysis.NTupleTools.userdata.JetUserData_cfi')

###############################################################################
# Here we define the objects we want to work with. As an example we have
# 3 types of muons:
# - our signal muons with tight isolation
# - our non-isolated muons for control region 1
# - our non-isolated muons for control region 2
# for each muon we have 1 jet collection and therefore 1 b-jet collection
# which leads to a total of 6 jet collections and 3 muon collections.
###############################################################################
cleaningDeltaR = 0.4
from PhysicsTools.PatAlgos.cleaningLayer1.jetCleaner_cfi import cleanPatJets
from PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi import selectedPatMuons
from PhysicsTools.PatAlgos.selectionLayer1.electronSelector_cfi import selectedPatElectrons


process.globalOrTrackerMuons= selectedPatMuons.clone(
    src='muonUserData',
    cut='userInt("isGlobalOrTrackerMuon")',
)

process.goodMuons = selectedPatMuons.clone(
    src='muonUserData',
    cut='userInt("isGood")',
)

process.vetoMuons = selectedPatMuons.clone(
    src='muonUserData',
    cut='userInt("isLoose")',
)

process.goodNonIsoR1Muons = process.goodMuons.clone(
    cut='userInt("isGoodNonIsoR1")',
)

process.goodNonIsoR2Muons = process.goodMuons.clone(
    cut='userInt("isGoodNonIsoR2")',
)

process.goodElectrons = selectedPatElectrons.clone(
    src='electronUserData',
    cut=cms.string('userInt("isGood")'),
    lazyParser=cms.untracked.bool(True),
)

process.vetoElectrons = process.goodElectrons.clone(
    cut=cms.string('userInt("isLoose")'),
)

process.goodConversionElectrons = process.goodElectrons.clone(
    cut='userInt("isGoodConversion")',
)
process.goodNonIsoElectrons = process.goodElectrons.clone(
    cut='userInt("isGoodNonIso")',
)

process.goodJets = cleanPatJets.clone(
    src=cms.InputTag("jetUserData"),
    preselection='userInt("passesPt") && userInt("isGood")',
    checkOverlaps=cms.PSet(
        electrons=cms.PSet(
            src=cms.InputTag("goodElectrons"),
            algorithm=cms.string("byDeltaR"),
            preselection=cms.string(""),
            deltaR=cms.double(cleaningDeltaR),
            # don't check if they share some AOD object ref
            checkRecoComponents=cms.bool(False),
            pairCut=cms.string(""),
            requireNoOverlaps=cms.bool(True),
        ),
        muons=cms.PSet(
            src=cms.InputTag("goodMuons"),
            algorithm=cms.string("byDeltaR"),
            preselection=cms.string(""),
            deltaR=cms.double(cleaningDeltaR),
            # don't check if they share some AOD object ref
            checkRecoComponents=cms.bool(False),
            pairCut=cms.string(""),
            requireNoOverlaps=cms.bool(True),
        ),
    )
)

process.goodJetsEConversionRegion = process.goodJets.clone()
process.goodJetsEConversionRegion.checkOverlaps.electrons.src = 'goodConversionElectrons'

process.goodJetsENonIsoRegion = process.goodJets.clone()
process.goodJetsENonIsoRegion.checkOverlaps.electrons.src = 'goodNonIsoElectrons'

process.goodJetsMuNonIsoR1Region = process.goodJets.clone()
process.goodJetsMuNonIsoR1Region.checkOverlaps.muons.src = 'goodNonIsoR1Muons'

process.goodJetsMuNonIsoR2Region = process.goodJets.clone()
process.goodJetsMuNonIsoR2Region.checkOverlaps.muons.src = 'goodNonIsoR2Muons'

# goodBJets = goodJets + Btag
process.goodBJets = cms.EDFilter(
    "PATJetSelector",
    src=cms.InputTag('goodJets'),
    cut=cms.string('userInt("passesMediumBtagWP")')
)

process.goodTightBJets = cms.EDFilter(
    "PATJetSelector",
    src=cms.InputTag('goodJets'),
    cut=cms.string('userInt("passesTightBtagWP")')
)

process.goodBJetsEConversionRegion = process.goodBJets.clone(
    src='goodJetsEConversionRegion')

process.goodBJetsENonIsoRegion = process.goodBJets.clone(
    src='goodJetsENonIsoRegion')

process.goodBJetsMuNonIsoR1Region = process.goodBJets.clone(
    src='goodJetsMuNonIsoR1Region')

process.goodBJetsMuNonIsoR2Region = process.goodBJets.clone(
    src='goodJetsMuNonIsoR2Region')
# tight b-tag WP
process.goodTightBJetsEConversionRegion = process.goodTightBJets.clone(
    src='goodJetsEConversionRegion')

process.goodTightBJetsENonIsoRegion = process.goodTightBJets.clone(
    src='goodJetsENonIsoRegion')

process.goodTightBJetsMuNonIsoR1Region = process.goodTightBJets.clone(
    src='goodJetsMuNonIsoR1Region')

process.goodTightBJetsMuNonIsoR2Region = process.goodTightBJets.clone(
    src='goodJetsMuNonIsoR2Region')

###############################################################################
# End of analysis object definition
###############################################################################


###############################################################################
# Begin selection
###############################################################################

# steps from
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPATExampleTopQuarks
from PhysicsTools.PatAlgos.selectionLayer1.jetCountFilter_cfi import countPatJets
process.step6a = countPatJets.clone(src='goodJets', minNumber=1)
process.step6b = countPatJets.clone(src='goodJets', minNumber=2)
process.step6c = countPatJets.clone(src='goodJets', minNumber=3)
process.step7 = countPatJets.clone(src='goodJets', minNumber=4)
process.step8a = countPatJets.clone(src='goodBJets', minNumber=1)
process.step8b = countPatJets.clone(src='goodBJets', minNumber=2)
###############################################################################
# end selection
###############################################################################


# ntuple output
process.nTupleElectrons.InputTag = 'electronUserData'
process.nTupleMuons.InputTag = 'muonUserData'
process.nTuplePFJets.InputTag = 'jetUserData'

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
