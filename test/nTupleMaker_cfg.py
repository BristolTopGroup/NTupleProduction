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
                  "Output tracks and PF candidates")

options.register ('use41x',
                  False,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Use the 41x options")

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


options.parseArguments()


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    caloJetCorrection = ( 'AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
    if options.use41x:
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/TT_ZuneZ2_Spring11.root',
            ]
    else :
        process.source.fileNames = [
            '/store/relval/CMSSW_4_2_2/RelValTTbar/GEN-SIM-RECO/START42_V11-v1/0005/50AC4DBF-746D-E011-8CF9-00248C55CC62.root'
            ]
    
else :
    if options.use41x :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        caloJetCorrection = ( 'AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute', 'L2L3Residual'])
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/data/Run2011ASingleElectronPromtReco_v2_run163796_AOD.root'
            ]
    else :
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
        caloJetCorrection = ( 'AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/SingleElectronMay10Rereco.root'
            ]


print options

print 'Running jet corrections: '
print 'Calo Jets'
print caloJetCorrection
print 'PF Jets'
print inputJetCorrLabel

import sys


###############################
####### Global Setup ##########
###############################


if not options.use41x :
    # 4.2.x configuration
    fileTag = '42x'
    if options.useData :
        process.GlobalTag.globaltag = cms.string( 'GR_R_42_V14::All' )
    else :
        process.GlobalTag.globaltag = cms.string( 'START42_V12::All' )

else :
    # 4.1.x configuration
    fileTag = '41x'
    if options.useData :
        process.GlobalTag.globaltag = cms.string('GR_R_41_V0::All')
    else :
        process.GlobalTag.globaltag = cms.string('START41_V0::All')
    

# HB + HE noise filtering
#values taken from
#https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
# Modify defaults setting to avoid an over-efficiency in the presence of OFT PU
process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumE = cms.double(999999.)
process.HBHENoiseFilterResultProducer.minNumIsolatedNoiseChannels = cms.int32(999999)
process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumEt = cms.double(999999.)


process.load("BristolAnalysis.NTupleTools.EventFilter_cfi")
process.EventFilter.NumTracks = cms.uint32(10)
process.EventFilter.HPTrackThreshold = cms.double(0.2)
process.EventFilter.minNElectrons = cms.int32(1)
process.EventFilter.minElectronPt = cms.double(25.)
process.EventFilter.maxAbsElectronEta = cms.double(2.6)
#for DAV vertices
pvSrc = 'offlinePrimaryVertices'
process.EventFilter.VertexInput = cms.InputTag('goodOfflinePrimaryVertices')
process.EventFilter.VertexMinimumNDOF = cms.uint32(4)# this is >= 4
process.EventFilter.VertexMaxAbsZ = cms.double(24)
process.EventFilter.VertexMaxAbsRho = cms.double(2)

# switch on PAT trigger
#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
#switchOnTrigger( process, hltProcess=options.hltProcess )




###############################
####### DAF PV's     ##########
###############################


if options.use41x :
    # redo DAF vertices
    process.load("RecoVertex.PrimaryVertexProducer.OfflinePrimaryVertices_cfi")

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( maxZ = cms.double(24.0),
                                     minNdof = cms.double(4.0) # this is >= 4
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


###############################
#### Calo Jet Setup    ########
###############################
#this has to run after PF2PAT and before removeMCMatching
#see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPAT38xChanges#Details_with_PF2PAT
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection
switchJetCollection( process,
                     jetCollection = cms.InputTag( 'ak5CaloJets' ),
                     jetCorrLabel = caloJetCorrection,
                     doBTagging = True,
                     doType1MET=False, )

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
process.kt6PFJets = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )

process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )


###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam = cms.double(0.8),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    Ghost_EtaMax = cms.double(7.0)
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

### AK5 Jets
#calo jets
process.selectedPatJets.cut = cms.string("pt > 20 & abs(eta) < 2.5")
#PF jets
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
#default is version=PURE09, quality=loose ID
#https://twiki.cern.ch/twiki/bin/view/CMS/JetID#Documentation
from PhysicsTools.SelectorUtils.jetIDSelector_cfi import jetIDSelector
process.goodPatJets = cms.EDFilter("JetIDSelectionFunctorFilter",
                                        filterParams = jetIDSelector.clone(),
                                        src = cms.InputTag("selectedPatJets")
                                        )

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
    process.HBHENoiseFilterResultProducer*
    process.goodOfflinePrimaryVertices*
    process.EventFilter*
    process.genParticlesForJetsNoNu*
    process.ca8GenJetsNoNu*
    getattr(process,"patPF2PATSequence"+postfix)*
    process.looseLeptonSequence*
    process.patDefaultSequence*
    process.goodPatJets *
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
                            process.offlinePrimaryVertices *
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

######################################################################################################
################################## nTuple Configuration ##############################################
######################################################################################################
process.load('BristolAnalysis.NTupleTools.Ntuple_cff')
#vertices
process.rootTupleVertex.InputTag = cms.InputTag('goodOfflinePrimaryVertices')
process.rootTupleVertex.Prefix = cms.string('goodOfflinePrimaryVertices.')
#calo jets
process.rootTupleCaloJets.InputTag = cms.InputTag('goodPatJets')
process.rootTupleCaloJets.Prefix = cms.string('goodPatJets.')
process.rootTupleCaloJets.ReadJECuncertainty = cms.bool(options.use41x)
#PF2PAT jets
process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
process.rootTuplePF2PATJets.Prefix = cms.string('goodPatJetsPFlow.')
#no JEC uncertainty available for PF jets yet in 42X
process.rootTuplePF2PATJets.ReadJECuncertainty = cms.bool(options.use41x)

#Cambridge-Aachen cone 0.8 jets
process.rootTupleCA8PFJets = process.rootTuplePF2PATJets.clone()
process.rootTupleCA8PFJets.InputTag = cms.InputTag('goodPatJetsCA8PF')
process.rootTupleCA8PFJets.Prefix = cms.string('goodPatJetsCA8PF.')
#selection on GenParticles
process.rootTupleGenParticles.minPt = cms.double(-1)
process.rootTupleGenParticles.maxAbsoluteEta = cms.double(100)

#the following jets need their own producer
#Cambridge-Aachen cone 0.8 jets pruned
#process.rootTupleCA8PFJetsPruned = process.rootTuplePF2PATJets.clone()
#process.rootTupleCA8PFJetsPruned.InputTag = cms.InputTag('goodPatJetsCA8PrunedPF')
#process.rootTupleCA8PFJetsPruned.Prefix = cms.string('goodPatJetsCA8PrunedPF.')
#Cambridge-Aachen cone 0.8 jets top tag
#process.rootTupleCA8PFJetsTopTag = process.rootTuplePF2PATJets.clone()
#process.rootTupleCA8PFJetsTopTag.InputTag = cms.InputTag('goodPatJetsCATopTagPF')
#process.rootTupleCA8PFJetsTopTag.Prefix = cms.string('goodPatJetsCATopTagPF.')



#GSF Electrons
process.rootTupleElectrons.InputTag = cms.InputTag('selectedPatElectrons')
process.rootTupleElectrons.Prefix = cms.string('selectedPatElectrons.')
#non-isolated PF electrons
process.rootTuplePFElectrons.InputTag = cms.InputTag('selectedPatElectronsLoosePFlow')
process.rootTuplePFElectrons.Prefix = cms.string('selectedPatElectronsLoosePFlow.')
#muons
process.nTupleMuons.InputTag = cms.InputTag('selectedPatMuons')
process.nTupleMuons.Prefix = cms.string('selectedPatMuons.')
#non isolated PF muons
process.nTuplePFMuons.InputTag = cms.InputTag('selectedPatMuonsLoosePFlow')
process.nTuplePFMuons.Prefix = cms.string('selectedPatMuonsLoosePFlow.')

#trigger
process.rootTupleTrigger.HLTInputTag = cms.InputTag('TriggerResults','',options.hltProcess)

process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
    outputCommands = cms.untracked.vstring(
       'drop *',
       #beamspot
        'keep *_rootTupleBeamSpot_*_*',
        #EventContent
        'keep *_rootTupleEvent_*_*',
        #CaloJets
        'keep *_rootTupleCaloJets_*_*',
        #PF jets
        'keep *_rootTuplePF2PATJets_*_*',
        'keep *_rootTupleCA8PFJets_*_*',
        #electrons
        'keep *_rootTupleElectrons_*_*',
        'keep *_rootTuplePFElectrons_*_*',
        #MET
        'keep *_rootTupleCaloMET_*_*',
        'keep *_rootTuplePFMET_*_*',
        #muons
        'keep *_nTupleMuons_*_*',
        'keep *_nTuplePFMuons_*_*',
        #trigger
        'keep *_rootTupleTrigger_*_*',
        #vertices (DA)
        'keep *_rootTupleVertex_*_*',
        #tracks
        'keep *_rootTupleTracks_*_*',
        #gen information
        'keep *_rootTupleGenEventInfo_*_*',
        'keep *_rootTupleGenParticles_*_*',
        'keep *_rootTupleGenJets_*_*',
        'keep *_rootTupleGenMETTrue_*_*',
    )
)

process.rootNTuples = cms.Sequence((
    #beamspot
    process.rootTupleBeamSpot +
    #vertices
    process.rootTupleVertex +
    #jets
    process.rootTupleCaloJets +
    process.rootTuplePF2PATJets +
    process.rootTupleCA8PFJets + 
#    process.rootTupleCA8PFJetsPruned +
#    process.rootTupleCA8PFJetsTopTag +
    #electrons
    process.rootTupleElectrons +
    process.rootTuplePFElectrons +
    #muons
    process.nTuplePFMuons + 
    process.nTupleMuons +
    #MET
    process.rootTupleCaloMET + 
    process.rootTuplePFMET +
    #Event
    process.rootTupleEvent +
    #trigger
    process.rootTupleTrigger +
    #genEventInfos
    process.rootTupleGenEventInfo +
    process.rootTupleGenParticles +
    process.rootTupleGenJetSequence +
    process.rootTupleGenMETSequence)*
    process.rootTupleTree)

if options.useData:
    process.rootNTuples.remove( process.rootTupleGenEventInfo )
    process.rootNTuples.remove( process.rootTupleGenParticles )
    process.rootNTuples.remove( process.rootTupleGenJetSequence )
    process.rootNTuples.remove( process.rootTupleGenMETSequence )
    
# HLT Trigger Report
process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
    HLTriggerResults=cms.InputTag("TriggerResults", "", options.hltProcess)
)


process.p0 = cms.Path(
                      process.hlTrigReport*
    process.patseq * process.rootNTuples)




process.out.SelectEvents.SelectEvents = cms.vstring('p0')


process.TFileService = cms.Service( "TFileService",
                           fileName = cms.string( 'ntuple.root' )
                           )
# rename output file
outPutFilePrefix = ''
if not options.dataType == '':
    outPutFilePrefix = options.dataType + '_'
if options.useData :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + fileTag + '_data_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + fileTag + '_data.root')
else :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + fileTag + '_mc_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'nTuple_' + fileTag + '_mc.root')


# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(100)


# process all the events
process.maxEvents.input = 100
process.options.wantSummary = True
process.out.dropMetaData = cms.untracked.string("DROPPED")


del process.outpath
            
open('junk.py','w').write(process.dumpPython())