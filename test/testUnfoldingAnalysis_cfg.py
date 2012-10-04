# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *
#set up analysis
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
GLOBALTAG_DATA = 'GR_R_52_V9D::All'
GLOBALTAG_MC = 'START52_V11C::All'
FILETAG = '52X'
TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/SingleElectron_Run2012B_196531_524_PromptReco-v1_AOD.root'
TEST_MC_FILE = 'file:///storage/TopQuarkGroup/test/DYJets_M-50_8TeV_Summer12.root'
#CERN
TEST_DATA_FILE = '/store/data/Run2012A/ElectronHad/AOD/PromptReco-v1/000/193/336/C47F154E-A697-E111-83F5-001D09F24D8A.root'
TEST_MC_FILE = '/store/mc/Summer12/TTJets_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S7_START52_V9-v1/0000/FEDDBC6A-9290-E111-B7FD-0018F3D09628.root'

#use jet energy correction from database (loaded from BristolAnalysis/NTupleTools/python_custom_JEC_cff.py)
#==False -> use JEC from Global Tag 
USE_JEC_FROM_DB = False
#if 'False' taus are included in the jet collections
removeTausFromJetCollection = False
#maximal relative isolation for loose leptons
maxLooseLeptonRelIso = 999.0
#include Cambridge-Aachen jet with cone of DR=0.8
includeCA08Jets = False

makePATTuple = False

postfix = "PFlow"
###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Calo Jets and leptons")

options.register ('useGSFelectrons',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Use GSF instead of PF electrons in PAT")

options.register ('writeIsolatedPFLeptons',
                  True,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Output isolated PF leptons")

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Force the check of the closest z vertex")

options.register ('dataType',
                  '',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "DataType prefix for output file name")

options.register ('skim',
                  'Lepton_2Jets',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "Skim definition")

options.register ('maxLooseLeptonRelIso',
                  5.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Maximum (PF)relIso value for leptons to be stored.")

options.register ('printEventContent',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Outputs the event content at the end of the path")

options.register ('CMSSW',
                  '53X',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "CMSSW version used: 53X (default), 52X or 44X")

options.register ('storePDFWeights',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Will store the PDF weights from cteq6.6")

options.parseArguments()

if options.CMSSW == '44X':
    GLOBALTAG_DATA = 'GR_R_44_V15::All'
    GLOBALTAG_MC = 'START44_V13::All'
    FILETAG = '44X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/ElectronHad_Run2011A_44X_AOD.root'
    TEST_MC_FILE = 'file:///storage/TopQuarkGroup/test/TTJets_TuneZ2_7TeV_Fall11_44X_AODSIM.root'
    #CERN
    #TEST_DATA_FILE = '/store/data/Run2011A/ElectronHad/AOD/08Nov2011-v1/0012/C481C0D4-1D1A-E111-8B01-E0CB4E1A1190.root'
    #TEST_MC_FILE =  '/store/mc/Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S6_START44_V9B-v1/0003/FEE78BEE-0237-E111-9CBC-003048678F06.root'

if options.CMSSW == '52X':
    GLOBALTAG_DATA = 'GR_R_52_V9D::All'
    GLOBALTAG_MC = 'START52_V11C::All'
    FILETAG = '52X'
    TEST_DATA_FILE = 'file:///storage/TopQuarkGroup/test/SingleElectron_Run2012B_196531_524_PromptReco-v1_AOD.root'
    TEST_MC_FILE = 'file:///storage/TopQuarkGroup/test/DYJets_M-50_8TeV_Summer12.root'
    #CERN
    TEST_DATA_FILE = '/store/data/Run2012A/ElectronHad/AOD/PromptReco-v1/000/193/336/C47F154E-A697-E111-83F5-001D09F24D8A.root'
    TEST_MC_FILE = '/store/mc/Summer12/TTJets_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S7_START52_V9-v1/0000/FEDDBC6A-9290-E111-B7FD-0018F3D09628.root'

maxLooseLeptonRelIso = options.maxLooseLeptonRelIso

if USE_JEC_FROM_DB:
    print "Loading JEC from database"
    from BristolAnalysis.NTupleTools.custom_JEC_cff import *
    database = ''
    if options.useData:
        database = 'BristolAnalysis/NTupleTools/data/JEC/Summer12_V3_DATA.db'
        configureCustomJEC_DATA(process, cms, database)
    else:
        database = 'BristolAnalysis/NTupleTools/data/JEC/Summer12_V3_MC.db'
        configureCustomJEC_MC(process, cms, database)
    
if not options.useData :
    process.source.fileNames = [
            TEST_MC_FILE
            ]
else:
    process.source.fileNames = [
            TEST_DATA_FILE
            ]
    
# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")

###############################
####### Global Setup ##########
###############################
if options.useData :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_DATA)
else :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_MC)

        
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
    
process.goodOfflinePrimaryVertices = cms.EDFilter(
  "PrimaryVertexObjectFilter",
  filterParams=cms.PSet(
                        minNdof=cms.double(4.),
                        maxZ=cms.double(24.),
                        maxRho=cms.double(2.)
                        ),
  filter=cms.bool(True),
  src=cms.InputTag('offlinePrimaryVertices')
)

#EventFilters and skim
from BristolAnalysis.NTupleTools.EventFilters_cff import *
process.EventFilters = setup_eventfilters(process, cms, options)
#PF2PAT
from BristolAnalysis.NTupleTools.PF2PAT_Setup_cff import *
setup_PF2PAT(process, cms, options, postfix=postfix, removeTausFromJetCollection=removeTausFromJetCollection)
setup_looseLeptons(process, cms, options, postfix=postfix, maxLooseLeptonRelIso=maxLooseLeptonRelIso)
#Jets
from BristolAnalysis.NTupleTools.Jets_Setup_cff import *
setup_jets(process, cms, options, postfix=postfix)
#electron ID
from BristolAnalysis.NTupleTools.ElectronID_cff import *
setup_electronID(process, cms)
#Object selection
from BristolAnalysis.NTupleTools.ObjectSelection_cff import *
selectObjects(process, cms)

from PhysicsTools.PatUtils.tools.metUncertaintyTools import runMEtUncertainties
runMEtUncertainties(process, doSmearJets=not options.useData, jetCollection='goodPatJetsPFlow', addToPatDefaultSequence=False)

#fix for loose pfIsolatedMuons for the newer tags
process.patMuonsLoosePFlow.pfMuonSource = cms.InputTag("pfIsolatedMuonsLoose" + postfix)
#fix for loose pfIsolatedElectrons for the newer tags
process.patElectronsLoosePFlow.pfElectronSource = cms.InputTag("pfIsolatedElectronsLoose" + postfix)

# turn to false when running on data
if options.useData :
    removeMCMatching(process, ['All'])
    process.looseLeptonSequence.remove(process.muonMatchLoosePFlow)

process.patseq = cms.Sequence(
    process.HBHENoiseFilterResultProducer * 
    process.goodOfflinePrimaryVertices * 
    process.genParticlesForJetsNoNu * 
    process.ca8GenJetsNoNu * 
    getattr(process, "patPF2PATSequence" + postfix) * 
    process.looseLeptonSequence * 
    process.patDefaultSequence * 
    process.goodPatJets * 
    process.goodPatJetsPFlow * 
    process.metUncertaintySequence * 
    process.goodPatJetsCA8PF * 
    process.flavorHistorySeq# * 
    )

process.patseq.replace(process.goodOfflinePrimaryVertices,
                            process.goodOfflinePrimaryVertices * 
                            process.eidCiCSequence)

if not makePATTuple:
    #NTuple content
    from BristolAnalysis.NTupleTools.NTupler_cff import *
    setup_ntupler(process, cms, options, includeCA08Jets)
else:
    from BristolAnalysis.NTupleTools.PatTuple_cff import *
    setup_pattuple(process, cms, options)

if not includeCA08Jets:
    process.patseq.remove(process.goodPatJetsCA8PF)
    
if options.useData:
    process.patseq.remove(process.genParticlesForJetsNoNu)
    process.patseq.remove(process.genJetParticles)    
    process.patseq.remove(process.ca8GenJetsNoNu)
    process.patseq.remove(process.flavorHistorySeq)
    
# HLT Trigger Report
process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
    HLTriggerResults=cms.InputTag("TriggerResults", "", options.hltProcess)
)


process.printEventContent = cms.EDAnalyzer("EventContentAnalyzer")
process.pdfWeights = cms.EDProducer("PdfWeightProducer",
                                    PdfInfoTag = cms.untracked.InputTag("generator"),
                                    PdfSetNames = cms.untracked.vstring(
                                         "cteq66.LHgrid", # 44 members
                                         )
                                    )

process.out.SelectEvents.SelectEvents = cms.vstring('makingNTuples')


process.TFileService = cms.Service("TFileService",
                           fileName=cms.string('ntuple.root')
                           )
# rename output file
outPutFilePrefix = ''
if not options.dataType == '':
    outPutFilePrefix = options.dataType + '_'
if options.useData :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_data_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_data.root')
else :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_mc_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + FILETAG + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
if options.maxEvents:
    process.maxEvents.input = options.maxEvents
else:
    process.maxEvents.input = 100
    
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")
process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")

if not makePATTuple:
    #do not write PAT-tuple information
    del process.outpath

from BristolAnalysis.NTupleTools.UnfoldingAnalysis_cff import *
setup_UnfoldingAnalysis(process, cms, options)

process.unfoldingAnalysis = cms.Path(
                      process.pdfWeights *
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      process.EventFilters * 
                      getattr(process, "producePatPFMETCorrections" + postfix) * 
                      getattr(process, "patMETs" + postfix)*
                      process.unfoldingAnalysisSequence 
                      )

if options.useData or not options.storePDFWeights:
    process.unfoldingAnalysis.remove(process.pdfWeights)