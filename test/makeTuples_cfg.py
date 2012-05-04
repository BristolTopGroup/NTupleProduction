# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *
#set up analysis
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
GLOBALTAG_DATA = 'GR_R_52_V7::All'
GLOBALTAG_MC = 'START52_V9::All'
FILETAG = '52X'
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

options.register ('writeIsolatedPFLeptons',
                  False,
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
                  999.,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.float,
                  "Maximum (PF)relIso value for leptons to be stored.")

options.register ('printEventContent',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Outputs the event content at the end of the path")

options.parseArguments()

maxLooseLeptonRelIso = options.maxLooseLeptonRelIso

if USE_JEC_FROM_DB:
    print "Loading JEC from database"
    from BristolAnalysis.NTupleTools.custom_JEC_cff import *
    configureCustomJEC(process, cms)
    
if not options.useData :
    process.source.fileNames = [
            'file:///storage/TopQuarkGroup/DYJets_M50_Summer12.root'
            ]
else:
    process.source.fileNames = [
            'file:///storage/TopQuarkGroup/ElectronHad_Run2012A_52X_PromptReco-v1_AOD.root'
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
setup_looseLeptons(process, cms, postfix=postfix, maxLooseLeptonRelIso=maxLooseLeptonRelIso)
#Jets
from BristolAnalysis.NTupleTools.Jets_Setup_cff import *
setup_jets(process, cms, options.useData, postfix=postfix)
#electron ID
from BristolAnalysis.NTupleTools.ElectronID_cff import *
setup_electronID(process, cms)
#Object selection
from BristolAnalysis.NTupleTools.ObjectSelection_cff import *
selectObjects(process, cms)

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
    process.EventFilters *
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

process.p0 = cms.Path(
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      process.producePatPFMETCorrections *
                      process.printEventContent *
                      process.rootNTuples
                      )

if not options.printEventContent:
    process.p0.remove(process.printEventContent)

process.out.SelectEvents.SelectEvents = cms.vstring('p0')


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

from BristolAnalysis.NTupleTools.PatTuple_cff import *
setup_pattuple(process, cms, options)

if not makePATTuple:
    #do not write PAT-tuple information
    del process.outpath
