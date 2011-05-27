# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

###############################
####### Parameters ############
###############################
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('python')

options.register ('useData',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Run this on real data")

options.register ('hltProcess',
                  'HLT',
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.string,
                  "HLT process name to use.")

options.register ('writeFat',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Output tracks and PF candidates")

options.register ('use41x',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Use the 41x options")

options.register ('forceCheckClosestZVertex',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.int,
                  "Force the check of the closest z vertex")



options.parseArguments()


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])

    if options.use41x:
        process.source.fileNames = [
            '/store/relval/CMSSW_4_1_5/RelValTTbar/GEN-SIM-RECO/START311_V2-v1/0037/20A7B6E4-8F6C-E011-9E6B-003048678FE4.root',
            ]
    else :
        process.source.fileNames = [
            '/store/relval/CMSSW_4_2_2/RelValTTbar/GEN-SIM-RECO/START42_V11-v1/0005/50AC4DBF-746D-E011-8CF9-00248C55CC62.root'
            ]
    
else :
    if options.use41x :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/data/Run2011ASingleElectronPromtReco_v2_run163796_AOD.root'
            ]
    else :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
        process.source.fileNames = [
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FE6792BA-9A70-E011-940A-002618943970.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FE0F23C8-9A70-E011-97A2-002618943821.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/FA7403C3-9A70-E011-BFE1-001A92810AA0.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F4886DC3-9A70-E011-BCD1-003048679000.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F232B0F1-9A70-E011-BA4E-003048678FE4.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/F0969EC4-9A70-E011-AAD9-003048678FC6.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/EEC627FE-9A70-E011-B1EA-0018F3D096C8.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/ECA837F0-9A70-E011-9637-002618943866.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E6E258CD-9A70-E011-A3AB-001A92971B7C.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E6249FB3-9A70-E011-88D9-003048678FB2.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E25FFEE0-9A70-E011-BE2B-0018F3D0968A.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/E0D345D7-9A70-E011-BF5F-002618943957.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/D0EF4AC6-9A70-E011-ACD0-0026189437E8.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/CCFCF4BD-9A70-E011-B72A-0018F3D096B4.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/C68BFCEB-9A70-E011-A4BC-003048678B12.root',
            '/store/data/Run2010A/JetMET/AOD/Apr21ReReco-v1/0000/C04521C3-9A70-E011-9DC8-001A928116BC.root'
            ]


print options

print 'Running jet corrections: '
print inputJetCorrLabel

import sys


###############################
####### Global Setup ##########
###############################


if not options.use41x :
    # 4.2.x configuration
    fileTag = '42x'
    if options.useData :
        process.GlobalTag.globaltag = cms.string( 'GR_R_42_V12::All' )
    else :
        process.GlobalTag.globaltag = cms.string( 'START42_V12::All' )

else :
    # 4.1.x configuration
    fileTag = '41x'
    process.load("CondCore.DBCommon.CondDBCommon_cfi")
    process.jec = cms.ESSource("PoolDBESSource",
                               DBParameters = cms.PSet(
                                   messageLevel = cms.untracked.int32(0)
                                   ),
                               timetype = cms.string('runnumber'),
                               toGet = cms.VPSet(
                                   cms.PSet(
                                       record = cms.string('JetCorrectionsRecord'),
                                       tag    = cms.string('JetCorrectorParametersCollection_Jec10V3_AK5PFchs'),
                                       label  = cms.untracked.string('AK5PFchs')
                                       )
                                   ),
                               ## here you add as many jet types as you need (AK5Calo, AK5JPT, AK7PF, AK7Calo, KT4PF, KT4Calo, KT6PF, KT6Calo)
                               connect = cms.string('sqlite_file:JEC/Jec10V3.db')
                               )
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')


    ## if options.useData :
    ##     process.GlobalTag.globaltag = cms.string('GR_R_311_V2::All')
    ## else :
    ##     process.GlobalTag.globaltag = cms.string('START311_V2::All')



# require scraping filter
process.scrapingVeto = cms.EDFilter("FilterOutScraping",
                                    applyfilter = cms.untracked.bool(True),
                                    debugOn = cms.untracked.bool(False),
                                    numtrack = cms.untracked.uint32(10),
                                    thresh = cms.untracked.double(0.2)
                                    )
# HB + HE noise filtering
process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi')
process.HBHENoiseFilterResultProducer = cms.EDProducer(
    'HBHENoiseFilterResultProducer',
    minRatio = cms.double(-999),
    maxRatio = cms.double(999),
    minHPDHits = cms.int32(17),
    minRBXHits = cms.int32(999),
    minHPDNoOtherHits = cms.int32(10),
    minZeros = cms.int32(10),
    minHighEHitTime = cms.double(-9999.0),
    maxHighEHitTime = cms.double(9999.0),
    maxRBXEMF = cms.double(-999.0),
    minNumIsolatedNoiseChannels = cms.int32(9999),
    minIsolatedNoiseSumE = cms.double(9999),
    minIsolatedNoiseSumEt = cms.double(9999),
    useTS4TS5 = cms.bool(True)
    )


# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess=options.hltProcess )




###############################
####### DAF PV's     ##########
###############################

pvSrc = 'offlinePrimaryVertices'
if options.use41x :
    pvSrc = 'offlinePrimaryVerticesDAF'
    process.offlinePrimaryVerticesDAF = cms.EDProducer("PrimaryVertexProducer",
        verbose = cms.untracked.bool(False),
        algorithm = cms.string('AdaptiveVertexFitter'),
        TrackLabel = cms.InputTag("generalTracks"),
        useBeamConstraint = cms.bool(False),
        beamSpotLabel = cms.InputTag("offlineBeamSpot"),
        minNdof  = cms.double(0.0),
        PVSelParameters = cms.PSet(
            maxDistanceToBeam = cms.double(1.0)
        ),
        TkFilterParameters = cms.PSet(
            algorithm=cms.string('filter'),
            maxNormalizedChi2 = cms.double(20.0),
            minPixelLayersWithHits=cms.int32(2),
            minSiliconLayersWithHits = cms.int32(5),
            maxD0Significance = cms.double(5.0), 
            minPt = cms.double(0.0),
            trackQuality = cms.string("any")
        ),

        TkClusParameters = cms.PSet(
            algorithm   = cms.string("DA"),
            TkDAClusParameters = cms.PSet(
                coolingFactor = cms.double(0.6),  #  moderate annealing speed
                Tmin = cms.double(4.),            #  end of annealing
                vertexSize = cms.double(0.01),    #  ~ resolution / sqrt(Tmin)
                d0CutOff = cms.double(3.),        # downweight high IP tracks 
                dzCutOff = cms.double(4.)         # outlier rejection after freeze-out (T<Tmin)
            )
        )
    )


process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
                                           vertexCollection = cms.InputTag(pvSrc),
                                           minimumNDOF = cms.uint32(7) ,
                                           maxAbsZ = cms.double(24), 
                                           maxd0 = cms.double(2) 
                                           )




from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(7.0)
                                     ),
    src=cms.InputTag(pvSrc)
    )


###############################
########## Gen Setup ##########
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone( rParam = cms.double(0.8),
                                           src = cms.InputTag("genParticlesForJetsNoNu"))

process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")


# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src = cms.InputTag("genParticles"),
                                            select = cms.vstring(
                                                "drop  *",
                                                "keep status = 3", #keeps all particles from the hard matrix element
                                                "+keep (abs(pdgId) = 11 | abs(pdgId) = 13) & status = 1" #keeps all stable muons and electrons and their (direct) mothers.
                                                )
                                            )


###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
from RecoJets.JetProducers.CATopJetParameters_cfi import *
from RecoJets.JetProducers.GenJetParameters_cfi import *


###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process,runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.Vertices = 'goodOfflinePrimaryVertices'
process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False
process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
if not options.use41x and not options.forceCheckClosestZVertex :
    process.pfPileUpPFlow.checkClosestZVertex = False


# In order to have a coherent semileptonic channel also, add
# some "loose" leptons to do QCD estimates.
process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )

process.patMuonsLoosePFlow = process.patMuonsPFlow.clone(
    pfMuonSource = cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
adaptPFMuons( process, process.patMuonsLoosePFlow, "PFlow")
process.muonMatchLoosePFlow = process.muonMatchPFlow.clone(
    src = cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
process.muonMatchPFlow.src = "pfIsolatedMuonsPFlow"

process.selectedPatMuonsLoosePFlow = process.selectedPatMuonsPFlow.clone(
    src = cms.InputTag("patMuonsLoosePFlow")
    )



process.pfIsolatedElectronsLoosePFlow = process.pfIsolatedElectronsPFlow.clone(
    combinedIsolationCut = cms.double(999.0) 
    )

process.patElectronsLoosePFlow = process.patElectronsPFlow.clone(
    pfElectronSource = cms.InputTag("pfIsolatedElectronsLoosePFlow")
    )
adaptPFElectrons( process, process.patElectronsLoosePFlow, "PFlow")

process.selectedPatElectronsLoosePFlow = process.selectedPatElectronsPFlow.clone(
    src = cms.InputTag("patElectronsLoosePFlow")
    )


process.looseLeptonSequence = cms.Sequence(
    process.pfIsolatedMuonsLoosePFlow +
    process.muonMatchLoosePFlow +
    process.patMuonsLoosePFlow +
    process.selectedPatMuonsLoosePFlow +    
    process.pfIsolatedElectronsLoosePFlow +
    process.patElectronsLoosePFlow +
    process.selectedPatElectronsLoosePFlow
    )


# turn to false when running on data
if options.useData :
    removeMCMatching( process, ['All'] )
    process.looseLeptonSequence.remove( process.muonMatchLoosePFlow )


###############################
###### Electron ID ############
###############################

# NOTE: ADDING THE ELECTRON IDs FROM CiC ----- USED WITH 42X 
    

process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentificationV06_cfi')

process.eidCiCSequence = cms.Sequence(
    process.eidVeryLooseMC *
    process.eidLooseMC *
    process.eidMediumMC*
    process.eidTightMC *
    process.eidSuperTightMC *
    process.eidHyperTight1MC *
    process.eidHyperTight2MC *
    process.eidHyperTight3MC *
    process.eidHyperTight4MC
    )

for iele in [ process.patElectrons,
              process.patElectronsPFlow,
              process.patElectronsLoosePFlow ] :
        iele.electronIDSources = cms.PSet(
            eidVeryLooseMC = cms.InputTag("eidVeryLooseMC"),
            eidLooseMC = cms.InputTag("eidLooseMC"),
            eidMediumMC = cms.InputTag("eidMediumMC"),
            eidTightMC = cms.InputTag("eidTightMC"),
            eidSuperTightMC = cms.InputTag("eidSuperTightMC"),
            eidHyperTight1MC = cms.InputTag("eidHyperTight1MC"),
            eidHyperTight2MC = cms.InputTag("eidHyperTight2MC"),
            eidHyperTight3MC = cms.InputTag("eidHyperTight3MC"),
            eidHyperTight4MC = cms.InputTag("eidHyperTight4MC")        
            )


###############################
###### Bare KT 0.6 jets #######
###############################

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    voronoiRfact = cms.double(0.9)
    )
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    voronoiRfact = cms.double(0.9)
    )


###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

###############################
###### Jet Pruning Setup ######
###############################


# Pruned PF Jets
process.caPrunedPFlow = cms.EDProducer(
    "SubJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False)
                           ),
    AnomalousCellParameters,
    SubJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    jetCollInstanceName=cms.string("subjets")
    )

process.caPrunedPFlow.nSubjets = cms.int32(2)


process.caPrunedGen =  cms.EDProducer(
    "SubJetProducer",
    GenJetParameters.clone(src = cms.InputTag("genParticlesForJetsNoNu"),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False)
                           ),
    AnomalousCellParameters,
    SubJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8),
    jetCollInstanceName=cms.string("subjets")
    )


###############################
#### CATopTag Setup ###########
###############################

# CATopJet PF Jets
# with adjacency 
process.caTopTagPFlow = cms.EDProducer(
    "CATopJetProducer",
    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False)                         
                           ),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8)
    )

process.CATopTagInfosPFlow = cms.EDProducer("CATopJetTagger",
                                    src = cms.InputTag("caTopTagPFlow"),
                                    TopMass = cms.double(171),
                                    TopMassMin = cms.double(0.),
                                    TopMassMax = cms.double(250.),
                                    WMass = cms.double(80.4),
                                    WMassMin = cms.double(0.0),
                                    WMassMax = cms.double(200.0),
                                    MinMassMin = cms.double(0.0),
                                    MinMassMax = cms.double(200.0),
                                    verbose = cms.bool(False)
                                    )



process.caTopTagGen = cms.EDProducer(
    "CATopJetProducer",
    GenJetParameters.clone(src = cms.InputTag("genParticlesForJetsNoNu"),
                           doAreaFastjet = cms.bool(True),
                           doRhoFastjet = cms.bool(False)),
    AnomalousCellParameters,
    CATopJetParameters,
    jetAlgorithm = cms.string("CambridgeAachen"),
    rParam = cms.double(0.8)
    )

process.CATopTagInfosGen = cms.EDProducer("CATopJetTagger",
                                          src = cms.InputTag("caTopTagGen"),
                                          TopMass = cms.double(171),
                                          TopMassMin = cms.double(0.),
                                          TopMassMax = cms.double(250.),
                                          WMass = cms.double(80.4),
                                          WMassMin = cms.double(0.0),
                                          WMassMax = cms.double(200.0),
                                          MinMassMin = cms.double(0.0),
                                          MinMassMax = cms.double(200.0),
                                          verbose = cms.bool(False)
                                          )



# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"kt6PFJets"),
        getattr(process,"kt6PFJets" + ipostfix),
        getattr(process,"ca8PFJets" + ipostfix),        
        getattr(process,"CATopTagInfos" + ipostfix),
        getattr(process,"caTopTag" + ipostfix),
        getattr(process,"caPruned" + ipostfix)
        ) :
        getattr(process,"patPF2PATSequence"+ipostfix).replace( getattr(process,"pfNoElectron"+ipostfix), getattr(process,"pfNoElectron"+ipostfix)*module )


# Use the good primary vertices everywhere. 
for imod in [process.patMuonsPFlow,
             process.patMuonsLoosePFlow,
             process.patElectronsPFlow,
             process.patElectronsLoosePFlow,
             process.patMuons,
             process.patElectrons] :
    imod.pvSrc = "goodOfflinePrimaryVertices"
    imod.embedTrack = True
    

addJetCollection(process, 
                 cms.InputTag('ca8PFJetsPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )


addJetCollection(process, 
                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8Pruned', 'PF',
                 doJTA=True,            # Run Jet-Track association & JetCharge
                 doBTagging=True,       # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )



addJetCollection(process, 
                 cms.InputTag('caTopTagPFlow'),
                 'CATopTag', 'PF',
                 doJTA=True,
                 doBTagging=True,
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
                 doJetID = False
                 )

for icorr in [process.patJetCorrFactorsCATopTagPF,
              process.patJetCorrFactorsCA8PrunedPF,
              process.patJetCorrFactorsCA8PF ] :
    icorr.rho = cms.InputTag("kt6PFJetsPFlow", "rho")


###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
                process.patJetsCA8PF,
                process.patJetsCA8PrunedPF,
                process.patJetsCATopTagPF
                ) :
    if options.useData == False :
        jetcoll.embedGenJetMatch = True
        jetcoll.getJetMCFlavour = True
        jetcoll.addGenPartonMatch = True
    # Add CATopTag info... piggy-backing on b-tag functionality
    jetcoll.addBTagInfo = True
    # Add the calo towers and PFCandidates.
    # I'm being a little tricksy here, because I only
    # actually keep the products if the "writeFat" switch
    # is on. However, this allows for overlap checking
    # with the Refs so satisfies most use cases without
    # having to add to the object size
    jetcoll.embedCaloTowers = True
    jetcoll.embedPFCandidates = True




###############################
#### Selections Setup #########
###############################

# AK5 Jets
process.selectedPatJetsPFlow.cut = cms.string("pt > 20 & abs(eta) < 2.5")
process.patJetsPFlow.addTagInfos = True
process.patJetsPFlow.tagInfoSources = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAODPFlow")
    )
process.patJetsPFlow.userData.userFunctions = cms.vstring( "? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")

# CA8 Pruned jets
process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")

# CA8 TopJets
process.selectedPatJetsCATopTagPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
process.patJetsCATopTagPF.addTagInfos = True
process.patJetsCATopTagPF.tagInfoSources = cms.VInputTag(
    cms.InputTag('CATopTagInfosPFlow')
    )

# electrons
process.selectedPatElectrons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectrons.embedTrack = cms.bool(True)
process.selectedPatElectronsPFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsPFlow.embedTrack = cms.bool(True)
process.selectedPatElectronsLoosePFlow.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patElectronsLoosePFlow.embedTrack = cms.bool(True)
# muons
process.selectedPatMuons.cut = cms.string('pt > 10.0 & abs(eta) < 2.5')
process.patMuons.embedTrack = cms.bool(True)
process.selectedPatMuonsPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsPFlow.embedTrack = cms.bool(True)
process.selectedPatMuonsLoosePFlow.cut = cms.string("pt > 10.0 & abs(eta) < 2.5")
process.patMuonsLoosePFlow.embedTrack = cms.bool(True)
# taus
process.selectedPatTausPFlow.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.selectedPatTaus.cut = cms.string("pt > 10.0 & abs(eta) < 3")
process.patTausPFlow.isoDeposits = cms.PSet()
process.patTaus.isoDeposits = cms.PSet()
# photons
process.patPhotonsPFlow.isoDeposits = cms.PSet()
process.patPhotons.isoDeposits = cms.PSet()


# Apply jet ID to all of the jets upstream. We aren't going to screw around
# with this, most likely. So, we don't really to waste time with it
# at the analysis level. 
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams = pfJetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJetsCA8PF")
                                        )
process.goodPatJetsCA8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                              filterParams = pfJetIDSelector.clone(),
                                              src = cms.InputTag("selectedPatJetsCA8PrunedPF")
                                              )
process.goodPatJetsCATopTagPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                             filterParams = pfJetIDSelector.clone(),
                                             src = cms.InputTag("selectedPatJetsCATopTagPF")
                                             )

# let it run


process.patseq = cms.Sequence(
    process.scrapingVeto*
    process.HBHENoiseFilterResultProducer*
    process.HBHENoiseFilter*
    process.goodOfflinePrimaryVertices*
    process.primaryVertexFilter*
    process.genParticlesForJetsNoNu*
    process.ca8GenJetsNoNu*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.looseLeptonSequence*
    process.patDefaultSequence*
    process.goodPatJetsPFlow*
    process.goodPatJetsCA8PF*
    process.goodPatJetsCA8PrunedPF*
    process.goodPatJetsCATopTagPF*
    process.flavorHistorySeq*
    process.prunedGenParticles*
    process.caPrunedGen*
    process.caTopTagGen*
    process.CATopTagInfosGen
    )

if options.use41x :
    process.patseq.replace( process.goodOfflinePrimaryVertices,
                            process.offlinePrimaryVerticesDAF *
                            process.goodOfflinePrimaryVertices *
                            process.eidCiCSequence )
else :
    process.patseq.replace( process.goodOfflinePrimaryVertices,
                            process.goodOfflinePrimaryVertices *
                            process.eidCiCSequence )

if options.useData == True :
    process.patseq.remove( process.genParticlesForJetsNoNu )
    process.patseq.remove( process.genJetParticles )    
    process.patseq.remove( process.ca8GenJetsNoNu )
    process.patseq.remove( process.flavorHistorySeq )
    process.patseq.remove( process.caPrunedGen )
    process.patseq.remove( process.caTopTagGen )
    process.patseq.remove( process.CATopTagInfosGen )
    process.patseq.remove( process.prunedGenParticles )


process.load('BristolAnalysis.NTupleTools.BristolNTuple_PFJets_cfi')
process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
    outputCommands = cms.untracked.vstring(
       'drop *',
        'keep *_rootTuplePF2PATJets_*_*',
    )
)

process.p0 = cms.Path(
    process.patseq * process.rootTuplePF2PATJets* process.rootTupleTree
    )

process.TFileService = cms.Service( "TFileService",
                           fileName = cms.string( 'ntuple.root' )
                           )

process.out.SelectEvents.SelectEvents = cms.vstring('p0')

# rename output file
if options.useData :
    if options.writeFat :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_data_fat.root')
    else :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_data.root')
else :
    if options.writeFat :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_mc_fat.root')
    else :
        process.out.fileName = cms.untracked.string('ttbsm_' + fileTag + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 100
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")


process.source.inputCommands = cms.untracked.vstring("keep *", "drop *_MEtoEDMConverter_*_*")



process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'drop *_selectedPatJets_*_*',    
    'keep *_patMETs*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',    
    'drop patPFParticles_*_*_*',
    'drop patTaus_*_*_*',
    'keep recoPFJets_caPruned*_*_*',
    'keep recoPFJets_caTopTag*_*_*',
    'keep patTriggerObjects_patTriggerPFlow_*_*',
    'keep patTriggerFilters_patTriggerPFlow_*_*',
    'keep patTriggerPaths_patTriggerPFlow_*_*',
    'keep patTriggerEvent_patTriggerEventPFlow_*_*',
    'keep *_cleanPatPhotonsTriggerMatch*_*_*',
    'keep *_cleanPatElectronsTriggerMatch*_*_*',
    'keep *_cleanPatMuonsTriggerMatch*_*_*',
    'keep *_cleanPatTausTriggerMatch*_*_*',
    'keep *_cleanPatJetsTriggerMatch*_*_*',
    'keep *_patMETsTriggerMatch*_*_*',
    'keep double_*PFlow*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJetsNoNu_*_*',
    'keep *_ca8GenJetsNoNu_*_*',
    'keep *_caPrunedGen_*_*',
    'keep *_caTopTagPFlow_*_*',
    'keep *_CATopTagInfosPFlow_*_*',
    'keep *_prunedGenParticles_*_*',
    'drop recoPFCandidates_selectedPatJets*_*_*',
    'drop CaloTowers_selectedPatJets*_*_*',
    'keep *_rootTuplePF2PATJets_*_*',
    'keep *_rootTupleElectrons_*_*',
    #'keep recoTracks_generalTracks_*_*'
    ]

if options.useData :
    process.out.outputCommands += ['drop *_MEtoEDMConverter_*_*',
                                   'keep LumiSummary_lumiProducer_*_*'
                                   ]
else :
    process.out.outputCommands += ['keep *_ca8GenJetsNoNu_*_*',
                                   'keep *_ak5GenJetsNoNu_*_*',                                   
                                   'keep GenRunInfoProduct_generator_*_*',
                                   'keep GenEventInfoProduct_generator_*_*',
                                   'keep *_flavorHistoryFilter_*_*',
                                   'keep PileupSummaryInfos_*_*_*'
                                   ]

if options.writeFat :

    process.out.outputCommands += [
        'keep *_pfNoElectron*_*_*',
        'keep recoTracks_generalTracks_*_*',
        'keep recoPFCandidates_selectedPatJets*_*_*',
        'keep recoBaseTagInfosOwned_selectedPatJets*_*_*',
        'keep CaloTowers_selectedPatJets*_*_*'
        ]
    
    if options.useData == False :
        process.out.outputCommands += [
            'keep *_genParticles_*_*'
            ]
            
#process.schedule = cms.Schedule( process.p0 )
open('junk.py','w').write(process.dumpPython())