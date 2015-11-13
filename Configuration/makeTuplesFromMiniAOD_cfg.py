import FWCore.ParameterSet.Config as cms

# Define the CMSSW process
process = cms.Process("Ntuples")

# Load the standard set of configuration modules
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')

# Message Logger settings
process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.destinations = ['cout', 'cerr']
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

# Set the process options -- Display summary at the end, enable unscheduled execution
process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False),
)

# print event content
process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")


## Source
# process.source = cms.Source("PoolSource",
# #     fileNames = cms.untracked.vstring('file:/hdfs/TopQuarkGroup/run2/miniAOD/TT_amcatnlo_25ns.root')
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        # 'root://xrootd.unl.edu//store/data/Run2015D/SingleElectron/MINIAOD/PromptReco-v3/000/256/675/00000/864628EB-9C5F-E511-AF26-02163E014767.root',
      
        # MC
        # 'root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v3/60000/00181849-176A-E511-8B11-848F69FD4C94.root', # /TT_TuneCUETP8M1_13TeV-powheg-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/
       
        # Data 

        # 05-Oct-2015 Run C
 		    # 'root://xrootd.unl.edu//store/data/Run2015C_25ns/SingleElectron/MINIAOD/05Oct2015-v1/30000/045710AD-C774-E511-9A9A-003048FFD770.root'
        
        # 05-Oct-2015 Run D
        # 'root://xrootd.unl.edu//store/data/Run2015D/SingleElectron/MINIAOD/05Oct2015-v1/10000/00991D45-4E6F-E511-932C-0025905A48F2.root',
        # 'root://xrootd.unl.edu//store/data/Run2015D/SingleMuon/MINIAOD/05Oct2015-v1/10000/021FD3F0-876F-E511-99D2-0025905A6060.root',
        
        # Prompt-Reco
        # 'root://xrootd.unl.edu//store/data/Run2015D/SingleElectron/MINIAOD/PromptReco-v4/000/258/159/00000/0EC56452-186C-E511-8158-02163E0146D5.root',
        # 'root://xrootd.unl.edu//store/data/Run2015D/SingleMuon/MINIAOD/PromptReco-v4/000/258/159/00000/6CA1C627-246C-E511-8A6A-02163E014147.root',
        
        'file:/hdfs/TopQuarkGroup/run2/miniAOD/TTJets_amcanlo_25ns.root',
        # 'root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/TT_TuneEE5C_13TeV-amcatnlo-herwigpp/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/10000/00A9F13F-C66D-E511-A943-0025901895CA.root'
        # 'root://xrootd.unl.edu//store/mc/RunIISpring15MiniAODv2/QCD_Pt-120to170_EMEnriched_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/74X_mcRun2_asymptotic_v2-v1/60000/0005C178-4A71-E511-ACB2-0002C94CD13C.root'
    )
)
# If you want to run with a json file
# import FWCore.PythonUtilities.LumiList as LumiList
# process.source.lumisToProcess = LumiList.LumiList(filename = '/hdfs/TopQuarkGroup/run2/json/Cert_246908-258159_13TeV_PromptReco_Collisions15_25ns_JSON_v3.txt').getVLuminosityBlockRange()

# Use to skip events e.g. to reach a problematic event quickly
# process.source.skipEvents = cms.untracked.uint32(2000)

# Get options from command line
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

from BristolAnalysis.NTupleTools.NTupleOptions_cff import *
getOptions( options )


# If you would like to change the Global Tag e.g. for JEC
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
globaltag = ''
if (options.isData) : 
  	globaltag='74X_dataRun2_Prompt_v4' #  dataset=/*/Run2015D-PromptReco-v4/MINIAOD
	if options.isRunC :
		globaltag='74X_dataRun2_v4' # dataset=/*/Run2015C_25ns*05Oct2015*/MINIAOD,
	if options.isReReco :
  		globaltag='74X_dataRun2_reMiniAOD_v0' #  dataset=/*/Run2015*05Oct2015*/MINIAOD
else :
  globaltag = '74X_mcRun2_asymptotic_v2' # 25ns MC

print "Using Global Tag : ", globaltag
process.GlobalTag.globaltag = cms.string(globaltag)
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')


# TT Gen Event configuration
from BristolAnalysis.NTupleTools.ttGenConfig_cff import * 
setupTTGenEvent( process, cms )

# Particle level definitions
from BristolAnalysis.NTupleTools.pseudoTopConfig_cff import *
setupPseudoTop( process, cms )

# Electron VID
from BristolAnalysis.NTupleTools.ElectronID_cff import *
setup_electronID( process, cms )

# Rerun HBHE filter and others
from BristolAnalysis.NTupleTools.metFilters_cfi import *
setupMETFilters( process, cms )

# Rerun MET
from BristolAnalysis.NTupleTools.MET_Setup_cff import setup_MET
setup_MET(process, cms, options)

# Custom JEC
from BristolAnalysis.NTupleTools.Jets_Setup_cff import setup_jets
setup_jets(process, cms, options)

# Load the selection filters and the selection analyzers
process.load( 'BristolAnalysis.NTupleTools.muonSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.qcdMuonSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.qcdElectronSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.electronSelection_cff')
process.load( 'BristolAnalysis.NTupleTools.SelectionCriteriaAnalyzer_cfi')

if options.tagAndProbe:
  process.topPairEPlusJetsSelection.tagAndProbeStudies = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.tagAndProbeStudies = cms.bool( True )
  process.topPairEPlusJetsSelection.jetSelectionInTaggingMode = cms.bool( True )
  process.topPairEPlusJetsSelectionTagging.jetSelectionInTaggingMode = cms.bool( True )

 
## Maximum Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000) )

from BristolAnalysis.NTupleTools.NTupler_cff import *
setup_ntupler(process, cms )

process.makingNTuples = cms.Path(
  process.metFilters *
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

process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsQCDSelectionTagging1_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairMuPlusJetsQCDSelectionTagging2_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsQCDSelectionTagging_*_*' )
process.nTupleTree.outputCommands.append( 'keep uint*_topPairEPlusJetsConversionSelectionTagging_*_*' )

process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsQCDSelectionTagging1_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairMuPlusJetsQCDSelectionTagging2_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsQCDSelectionTagging_*FullSelection*_*' )
process.nTupleTree.outputCommands.append( 'keep bool_topPairEPlusJetsConversionSelectionTagging_*FullSelection*_*' )

if not options.isData:
  # 25ns Triggers
  process.triggerSequence.remove( process.nTupleTriggerEle27erWPLooseGsf )
  process.triggerSequence.remove( process.nTupleTriggerEle23erWPLooseGsf )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu18er )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu20er )
  process.triggerSequence.remove( process.nTupleTriggerIsoTkMu20er )
  process.triggerSequence.remove( process.nTupleTrigger )
  del process.nTupleTriggerEle27erWPLooseGsf, process.nTupleTriggerEle23erWPLooseGsf, process.nTupleTriggerIsoMu18er, process.nTupleTriggerIsoMu20er, process.nTupleTriggerIsoTkMu20er, process.nTupleTrigger

  process.makingNTuples.remove( process.metFilters )
  del process.metFilters
  pass

else :
  process.makingNTuples.remove( process.makePseudoTop )

  process.nTuples.remove( process.pseudoTopSequence )
  process.nTuples.remove( process.nTupleGenMET )
  process.nTuples.remove( process.nTupleGenJets )
  process.nTuples.remove( process.nTupleGenEventInfo )
  process.nTuples.remove( process.nTupleGenParticles )
  process.nTupleTree.outputCommands.append('drop *_nTuplePFJets_*Gen*_*')
  del process.makePseudoTop, process.pseudoTopSequence, process.nTupleGenMET
  del process.nTupleGenJets,  process.nTupleGenEventInfo, process.nTupleGenParticles

  # 25ns Triggers
  process.triggerSequence.remove( process.nTupleTriggerEle27erWP75GsfMC )
  process.triggerSequence.remove( process.nTupleTriggerEle23erWP75GsfMC )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu18erMC )
  process.triggerSequence.remove( process.nTupleTriggerIsoMu20erMC )
  process.triggerSequence.remove( process.nTupleTriggerIsoTkMu20erMC )
  process.triggerSequence.remove( process.nTupleTrigger )
  del process.nTupleTriggerEle27erWP75GsfMC, process.nTupleTriggerEle23erWP75GsfMC, process.nTupleTriggerIsoMu20erMC, process.nTupleTriggerIsoMu18erMC, process.nTupleTriggerIsoTkMu20erMC, process.nTupleTrigger

# if options.isData and options.isRereco:
#   process.nTupleEvent.metFiltersInputTag = cms.InputTag('TriggerResults','','PAT')


# if options.isData and options.isRunC:
# 	process.triggerSequence.remove( process.nTupleTriggerIsoMu18 )
# 	del process.nTupleTriggerIsoMu18

if not options.isTTbarMC:
  process.makingNTuples.remove( process.ttGenEvent )
  process.selectionCriteriaAnalyzer.genSelectionCriteriaInput = cms.VInputTag()
else:
  process.nTupleGenEventInfo.isTTbarMC = cms.bool( True )

if not options.printEventContent:
    process.makingNTuples.remove(process.printEventContent)

process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )

# process.out = cms.OutputModule("PoolOutputModule",
#                 fileName = cms.untracked.string("testOutput.root")
#         )
# process.outpath = cms.EndPath(process.out)


