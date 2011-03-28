useREDIGI = False
runOn_Spring10_Physics_MC = True
runOnMC = True

realData = False
useREDIGI = False
JECSetName = "Spring10"
wantPatTuple = bool( 0 )
doPDFweights = bool( 0 )
outname = "nTuple_data.root"
patname = "pat_data.root"


realData = False
useREDIGI = True
outname = "nTuple_mc.root"
patname = "pat_mc.root"


from BristolAnalysis.NTupleTools.PF2PAT_MC_cfi import *
process = PF2PAtProcess()
###################
#  Add JPT jets
###################
# Ref: https://twiki.cern.ch/twiki/bin/view/CMS/JetPlusTracksCorrections
process.load( "RecoJets.Configuration.RecoJPTJets_cff" )

# Jet Correction (in 3_6_0)
process.load( 'JetMETCorrections.Configuration.DefaultJEC_cff' )
# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")
# to run on 35X input sample
# ref: https://twiki.cern.ch/twiki/bin/view/CMS/SWGuidePATRecipes#CMSSW_3_6_X
from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *

from PhysicsTools.PatAlgos.tools.muonTools import *
addMuonUserIsolation(process)
from PhysicsTools.PatAlgos.tools.electronTools import *
addElectronUserIsolation(process)


process.GlobalTag.globaltag = cms.string( 'START311_V2::All' )

from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.tauTools import *






# set jet corrections
#print "*******************************************************"
#print "Calling switchJECSet() to set jet energy corrections: ", JECSetName
#print "*******************************************************"
#from PhysicsTools.PatAlgos.tools.jetTools import switchJECSet
#switchJECSet( process, JECSetName )

from PhysicsTools.PatAlgos.tools.jetTools import *

# remove the tag infos
# need to keep tag infos to access SV info via pat::jet->tagInfoSecondaryVertex()
process.patJets.addTagInfos = False
# require jet pt > 10 (L2+L3 corrected)
process.selectedPatJets.cut = cms.string( 'pt > 10' )
# look for at least one jet
process.countPatJets.minNumber = 0

from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET( process, 'TC' )

#print process.patJetCorrFactors.corrSample



# add ak5GenJets as they are not in the Spring10 physics MC
# ref: https://hypernews.cern.ch/HyperNews/CMS/get/JetMET/899/1/1/1/1.html

# ak5GenJets are NOT there: First load the needed modules
process.load( "RecoJets.Configuration.GenJetParticles_cff" )
process.load( "RecoJets.JetProducers.ak5GenJets_cfi" )

switchJetCollection( process,
                     jetCollection = cms.InputTag( 'ak5CaloJets' ),
                     jetCorrLabel = ( 'AK5Calo', ['L2Relative', 'L3Absolute'] ),
                     doBTagging = True )

####################################
##
##    Add extra jet collections
##
####################################
# JPT jets
#addJetCollection( process, cms.InputTag( 'JetPlusTrackZSPCorJetAntiKt5' ),
#                 'AK5', 'JPT',
#                 doJTA = True,
#                 doBTagging = True, #off
#                 jetCorrLabel = ( 'AK5JPT', ['L2Relative', 'L3Absolute'] ), #None,
#                 doType1MET = False,
#                 doL1Cleaning = False,
#                 doL1Counters = False,
#                 genJetCollection = cms.InputTag( "ak5GenJets" ),
#                 doJetID = True,
#                 jetIdLabel = "ak5"
#                 )
process.load("RecoJets.JetProducers.ak5PFJets_cfi")
addJetCollection( process, 
                  cms.InputTag( 'ak5PFJets::PAT' ), 
                  'AK5', 'PF', 
                  jetCorrLabel = ( 'AK5PF', ['L2Relative', 'L3Absolute'] ), 
                  doType1MET = False, 
                  doJetID = True,
                  doBTagging = True)
# make sure to run process.ak5PFJets before PAT, for example:
process.patDefaultSequence = cms.Sequence( process.ak5PFJets * process.patDefaultSequence )

# no btag for extra jets
#process.patJetsAK5JPT.addTagInfos = True
process.patJetsPF.addTagInfos = True#True
process.patJets.addBTagInfo = True

# Input files
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()



# test real data (copied from PatExample)
readFiles.extend( [
    'file:/storage/top/FED5D572-8DBA-DF11-B636-0030487FA609.root' ##re-reco Sep3 sample
   # 'file:/storage/top/6625EA96-45C7-DF11-860F-001D09F24F65.root' #2010B AOD sample
    ] );



        ## test using Spring10 ttjet: /TTbarJets-madgraph/Spring10_START3X_V26_S09-v1/GEN-SIM-RECO (need run33xOnReReco)
process.source.fileNames = readFiles



# configure HLT
process.load( 'L1TriggerConfig.L1GtConfigProducers.L1GtTriggerMaskTechTrigConfig_cff' )
process.load( 'HLTrigger/HLTfilters/hltLevel1GTSeed_cfi' )
process.hltLevel1GTSeed.L1TechTriggerSeeding = cms.bool( True )
process.hltLevel1GTSeed.L1SeedsLogicalExpression = cms.string( '(40 OR 41) AND NOT (36 OR 37 OR 38 OR 39)' )


#process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
#    HLTriggerResults = cms.InputTag("TriggerResults","","REDIGI")
#)




# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32( 1000 )
#process.MessageLogger.cerr.INFO.limit = 10
#process.MessageLogger.cerr.threshold = "DEBUG"
#process.MessageLogger.categories.append("HLTrigReport")
#process.MessageLogger.hlTrigReport.limit = 1000




# process all the events
process.maxEvents.input = -1 #20000
process.options.wantSummary = False

#process.out.outputCommands += (['keep *_*_*_*'
#                               ])


#from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent

process.out = cms.OutputModule( 
    "PoolOutputModule",
    fileName = cms.untracked.string( 'pat_dataPATLayer1_Output.fromAOD_full.root' ),
    outputCommands = cms.untracked.vstring( 'keep *', #'drop *',
                                           #*patEventContent)
                                           'keep *_patElectrons_*_*',
                                           'keep *_patElectronsToto_*_*',
                                           'keep *_patElectronsPF_*_*',
                                           'keep *_selectedPatElectronsToto_*_*',
                                           'keep *_selectedPatElectronsPF_*_*',
                                           'keep *_selectedPatMuonsPF_*_*',
                                           'keep *_selectedPatJetsPF_*_*',

                                           'keep *_cleanPatElectrons_*_*',
                                           'keep *_cleanPatEle2_*_*',
                                           'keep *_cleanPatEle3_*_*',
                                           'keep *_cleanPatMuons_*_*',
                                           'keep *_cleanPatMu2_*_*',
                                           'keep *_cleanPatMu3_*_*',
                                           'keep *_cleanPatJets_*_*',
                                           'keep *_cleanPatJetsAK5PF_*_*',
                                           'keep *_cleanPatJetsAK5JPT_*_*',
                                           'keep *_patMETs_*_*',
                                           'keep *_patMETsPF_*_*',
                                           'keep *_patMETsTC_*_*',
                                           'keep *_cleanPatPhotons_*_*',
                                           'keep *_cleanPatTaus_*_*',
                                           'keep recoSuperCluster_*_*_*',
                                           'keep recoTracks_generalTracks_*_*',
                                           'keep edmTriggerResults_TriggerResults_*_*',
                                           'keep *_offlinePrimaryVertices_*_*',
                                           'keep *_offlinePrimaryVerticesWithBS_*_*',
                                           'keep *_offlineBeamSpot_*_*'

                                           )
    )

process.out.fileName = patname
################# Above are examples from PhysicsTools ##############################

# add PDFWeightProducer (8-2-2010)

#if doPDFweights:
#    process.pdfWeights = cms.EDProducer(
#        "PdfWeightProducer",
#        PdfInfoTag = cms.untracked.InputTag("generator"),
#        PdfSetNames = cms.untracked.vstring("cteq66.LHgrid"
#                                            #, "MRST2006nnlo.LHgrid"
#                                            #, "MRST2007lomod.LHgrid"
#                                            )
#        )



import PhysicsTools.PatAlgos.producersLayer1.electronProducer_cfi as eleProducer
#process.load("RecoEgamma.ElectronIdentification.simpleEleIdSequence_cff")
#process.patElectronIDs = cms.Sequence(process.simpleEleIdSequence)
#process.patElectrons.addElectronID = cms.bool(True)
#process.patElectrons.electronIDSources = cms.PSet(
#    simpleEleId95relIso= cms.InputTag("simpleEleId95relIso"),
#    simpleEleId90relIso= cms.InputTag("simpleEleId90relIso"),
#    simpleEleId85relIso= cms.InputTag("simpleEleId85relIso"),
#    simpleEleId80relIso= cms.InputTag("simpleEleId80relIso"),
#    simpleEleId70relIso= cms.InputTag("simpleEleId70relIso"),
#    simpleEleId60relIso= cms.InputTag("simpleEleId60relIso"),
#    simpleEleId95cIso= cms.InputTag("simpleEleId95cIso"),
#    simpleEleId90cIso= cms.InputTag("simpleEleId90cIso"),
#    simpleEleId85cIso= cms.InputTag("simpleEleId85cIso"),
#    simpleEleId80cIso= cms.InputTag("simpleEleId80cIso"),
#    simpleEleId70cIso= cms.InputTag("simpleEleId70cIso"),
#    simpleEleId60cIso= cms.InputTag("simpleEleId60cIso"),
#)
process.patEle2 = eleProducer.patElectrons.clone( 
    pvSrc = "offlinePrimaryVerticesWithBS"
    )

process.patEle3 = eleProducer.patElectrons.clone( 
    usePV = False,
    beamLineSrc = "offlineBeamSpot"
    )

import PhysicsTools.PatAlgos.cleaningLayer1.electronCleaner_cfi as eleCleaner
process.cleanPatEle2 = eleCleaner.cleanPatElectrons.clone( 
    src = "patEle2"
    )
process.cleanPatEle3 = eleCleaner.cleanPatElectrons.clone( 
    src = "patEle3"
    )

process.patElectronsPF.pvSrc = "offlinePrimaryVertices"


################
#  muons d0
################
import PhysicsTools.PatAlgos.producersLayer1.muonProducer_cfi as muProducer
process.patMu2 = muProducer.patMuons.clone( 
    pvSrc = "offlinePrimaryVerticesWithBS"
    )
process.patMu3 = muProducer.patMuons.clone( 
    usePV = False,
    beamLineSrc = "offlineBeamSpot"
    )


import PhysicsTools.PatAlgos.cleaningLayer1.muonCleaner_cfi as muCleaner
process.cleanPatMu2 = muCleaner.cleanPatMuons.clone( 
    src = "patMu2"
    )
process.cleanPatMu3 = muCleaner.cleanPatMuons.clone( 
    src = "patMu3"
    )


process.myExtraLepton = cms.Sequence(  
        process.patElectronIsolation *
        process.patEle2 *
        process.patEle3 *
        process.patMu2 *
        process.patMu3 *
        process.cleanPatEle2 *
        process.cleanPatEle3 *
        process.cleanPatMu2 *
        process.cleanPatMu3
#        process.morePFElectron

 )



### put the usual cff fragment here
process.InputTagDistributorService = cms.Service( "InputTagDistributorService" )

process.VariableHelperService = cms.Service( "VariableHelperService" )

process.UpdaterService = cms.Service( "UpdaterService" )

process.TFileService = cms.Service( "TFileService",
                           fileName = cms.string( 'ntuple.root' )
                           )


process.load( 'BristolAnalysis.NTupleTools.Ntuple_cff' )
process.load( "CommonTools.RecoAlgos.HBHENoiseFilter_cfi" )
# RootTupleMakerV2 tree
process.rootTupleTree = cms.EDAnalyzer( "RootTupleMakerV2_Tree",
    outputCommands = cms.untracked.vstring( 
        'drop *',
        'keep *_rootTupleBeamSpot_*_*',
        'keep *_rootTupleEvent_*_*',
#        'keep *_rootTupleEventExtra_*_*',
        'keep *_rootTupleEventSelection_*_*',
        'keep *_rootTupleCaloJets_*_*',
#        'keep *_rootTupleCaloJetsExtra_*_*',
        'keep *_rootTuplePFJets_*_*',
#        'keep *_rootTuplePFJetsExtra_*_*',
        'keep *_rootTuplePF2PATJets_*_*',
#        'keep *_rootTuplePF2PATJetsExtra_*_*',
        'keep *_rootTupleElectrons_*_*',
#        'keep *_rootTupleElectronsExtra_*_*',
        'keep *_rootTuplePFElectrons_*_*',
#        'keep *_rootTuplePFElectronsExtra_*_*',
        'keep *_rootTupleElectronsExtra_*_*',
#        'keep *_rootTuplePFElectronsExtra_*_*',
        'keep *_rootTupleCaloMET_*_*',
        'keep *_rootTupleTCMET_*_*',
        'keep *_rootTuplePFMET_*_*',
#        'keep *_rootTupleCaloMETExtra_*_*',
#        'keep *_rootTupleTCMETExtra_*_*',
#        'keep *_rootTuplePFMETExtra_*_*',
        'keep *_nTupleMuons_*_*',
#        'keep *_rootTupleMuonsExtra_*_*',
        'keep *_nTuplePFMuons_*_*',
#        'keep *_rootTuplePFMuonsExtra_*_*',
        'keep *_rootTupleSuperClusters_*_*',
        'keep *_rootTupleTrigger_*_*',
        'keep *_rootTupleVertex_*_*',
        'keep *_rootTupleVertexWithBS_*_*',
        'keep *_rootTupleGenEventInfo_*_*',
        'keep *_rootTupleGenParticles_*_*',
        'keep *_rootTupleGenJets_*_*',
#        'keep *_rootTupleGenJetsExtra_*_*',
        'keep *_rootTupleGenMETTrue_*_*',
#        'keep *_rootTupleGenMETTrueExtra_*_*',
        'keep *_rootTupleTracks_*_*'
    )
 )
process.TFileService.fileName = outname

#to prevent patTuple output, delete the outpath:
if not wantPatTuple:
    del process.outpath

process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
process.load("Leptoquarks.LeptonJetFilter.leptonjetfilter_cfi")
##################################################################
#### Electron based skim
process.LJFilter.muLabel = 'muons'
process.LJFilter.elecLabel = 'gsfElectrons'
process.LJFilter.jetLabel = 'ak5CaloJets'
process.LJFilter.muonsMin = -1
process.LJFilter.electronsMin = -1
process.LJFilter.elecPT = 25.
process.LJFilter.counteitherleptontype = False


process.p = cms.Path( 
#        process.hlTrigReport *
        process.LJFilter*
        process.HBHENoiseFilter*
        process.HBHENoiseFilterResultProducer*
        process.genParticlesForJets *
        process.ak5GenJets *
        #process.myJPT *
        process.patDefaultSequence *
        process.myExtraLepton *
        getattr( process, "patPF2PATSequence" + postfix )
        )

#    ## add PDF weighs as required
#    if doPDFweights:
#        process.p *= process.pdfWeights

process.p *= ( 
    process.rootTupleBeamSpot +
    process.rootTupleEvent +
    process.rootTupleEventSelection +
    process.rootTupleCaloJetSequence +
#    process.rootTupleJPTJetSequence + 
    process.rootTuplePFJetSequence +
    process.rootTupleElectronSequence +
    process.rootTupleMETSequence +
    process.nTupleMuonSequence +
    process.rootTupleTrigger +
    process.rootTupleVertex +
    process.rootTupleVertexWithBS +
    process.rootTupleGenEventInfo +
    process.rootTupleGenParticles +
    process.rootTupleGenJetSequence +
    process.rootTupleGenMETSequence +
    process.rootTupleTracks
    ) * process.rootTupleTree

process.schedule = cms.Schedule( process.p )
