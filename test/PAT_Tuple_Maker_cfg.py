# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

#set up analysis
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
GLOBALTAG_DATA = 'GR_R_44_V14::All'
GLOBALTAG_MC = 'START44_V13::All'
FILETAG = '44X'
USE_JEC_FROM_DB = False

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


options.parseArguments()



if USE_JEC_FROM_DB:
    print "Loading JEC from database"
    from BristolAnalysis.NTupleTools.custom_JEC_cff import *
    configureCustomJEC(process, cms)


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
    process.source.fileNames = [
            'file:///storage/TopQuarkGroup/TTJets_TuneZ1_Fall11_44X_AODSIM.root'
            ]
else :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute', 'L2L3Residual'])
    process.source.fileNames = [
            'file:///storage/TopQuarkGroup/ElectronHad_Run2011A_44X_AOD.root'
            ]
        


print options

print 'Running jet corrections: '
print 'Calo Jets'
print caloJetCorrection
print 'PF Jets'
print inputJetCorrLabel
print 'Using Skim:'
print options.skim

import sys


###############################
####### Global Setup ##########
###############################
if options.useData :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_DATA)
else :
        process.GlobalTag.globaltag = cms.string(GLOBALTAG_MC)
        
# HB + HE noise filtering
#values taken from
#https://twiki.cern.ch/twiki/bin/view/CMS/HBHEAnomalousSignals2011
process.HBHENoiseFilterResultProducer = cms.EDProducer(
    'HBHENoiseFilterResultProducer',
    noiselabel=cms.InputTag('hcalnoise', '', 'RECO'),
    minRatio=cms.double(-999),
    maxRatio=cms.double(999),
    minHPDHits=cms.int32(17),
    minRBXHits=cms.int32(999),
    minHPDNoOtherHits=cms.int32(10),
    minZeros=cms.int32(10),
    minHighEHitTime=cms.double(-9999.0),
    maxHighEHitTime=cms.double(9999.0),
    maxRBXEMF=cms.double(-999.0),
    minNumIsolatedNoiseChannels=cms.int32(9999),
    minIsolatedNoiseSumE=cms.double(9999),
    minIsolatedNoiseSumEt=cms.double(9999),
    useTS4TS5=cms.bool(True)
    )
#process.load('CommonTools/RecoAlgos/HBHENoiseFilterResultProducer_cfi')
# Modify defaults setting to avoid an over-efficiency in the presence of OFT PU
#process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumE = cms.double(999999.)
#process.HBHENoiseFilterResultProducer.minNumIsolatedNoiseChannels = cms.int32(999999)
#process.HBHENoiseFilterResultProducer.minIsolatedNoiseSumEt = cms.double(999999.)


process.load("BristolAnalysis.NTupleTools.EventFilter_cfi")
#Event cleaning
process.EventFilter.NumTracks = cms.uint32(10)
process.EventFilter.HPTrackThreshold = cms.double(0.2)
#for DAV vertices, obsolete?
#pvSrc = 'offlinePrimaryVertices'
#at least one good primary vertex
process.EventFilter.VertexInput = cms.InputTag('goodOfflinePrimaryVertices')
process.EventFilter.VertexMinimumNDOF = cms.uint32(4)# this is >= 4
process.EventFilter.VertexMaxAbsZ = cms.double(24)
process.EventFilter.VertexMaxAbsRho = cms.double(2)

#reset to 0 skim
process.EventFilter.minNElectrons = cms.int32(-1)
process.EventFilter.minNMuons = cms.int32(-1)
process.EventFilter.minNJets = cms.int32(-1)
process.EventFilter.counteitherleptontype = cms.untracked.bool(False)

#skim option is not case-sensitive
#skim = options.skim.lower()
#import skim selection
from BristolAnalysis.NTupleTools.Skim_cff import *
createSkim(process, options.skim, cms)
##skim option is not case-sensitive
#skim = options.skim.lower()
#if 'electron' in skim or 'lepton' in skim:
#    process.EventFilter.maxAbsElectronEta   = cms.double(2.5)#within tracker volume
#    #electron multiplicity
#    if 'di' in skim:
#        process.EventFilter.minNElectrons       = cms.int32(2)
#    else:
#        process.EventFilter.minNElectrons       = cms.int32(1)
#        
#    if 'loose' in skim:#loose Pt cut
#        process.EventFilter.minElectronPt       = cms.double(20.)
#        process.EventFilter.electronInput = cms.InputTag("selectedPatElectrons")#GSF electrons
#    else:
#        process.EventFilter.minElectronPt       = cms.double(30.)
#        process.EventFilter.electronInput = cms.InputTag("selectedPatElectronsLoosePFlow")
#    
#if 'muon'  in skim or 'lepton' in skim:
#    #muon multiplicity
#    if 'di' in skim:
#        process.EventFilter.minNMuons       = cms.int32(2)
#    else:
#        process.EventFilter.minNMuons       = cms.int32(1)
#    if 'loose' in skim:#loose Pt cut and eta cut
#        process.EventFilter.maxAbsMuonEta   = cms.double(2.5)#within tracker volume
#        process.EventFilter.minMuonPt       = cms.double(10.)
#        process.EventFilter.muonInput = cms.InputTag("selectedPatMuons")
#    else:
#        process.EventFilter.minMuonPt       = cms.double(20.)#triggers are 17GeV
#        process.EventFilter.maxAbsMuonEta   = cms.double(2.1)#new triggers have this restriction anyway
#        process.EventFilter.muonInput = cms.InputTag("selectedPatMuonsLoosePFlow")
#    
#if 'lepton' in skim:
#    process.EventFilter.counteitherleptontype = cms.untracked.bool(True)
# 
##jet skim
##unprescaled triggers are >=3/>=2 jets for electron/muon triggers
#if 'jet' in skim:
#    find = skim.find('jet')
#    nJets = int(skim[find - 1])
#    process.EventFilter.jetInput = cms.InputTag("selectedPatJetsPFlow")
#    process.EventFilter.minNJets = cms.int32(nJets)
#    process.EventFilter.minJetPt = cms.double(30.)# identical (within JEC) to trigger
#    process.EventFilter.maxAbsJetEta = cms.double(2.6)# identical to trigger
#    
#    
#if not (options.skim == '' or options.skim == 'NoSkim'):
#    print '='*10, 'Skim definition', '='*10
#    print 'Electron skim:'
#    print '\t >=', str(process.EventFilter.minNMuons),' electron with ',
#    print 'p_T > ', str(process.EventFilter.minElectronPt),
#    print '|eta| < ' , str(process.EventFilter.maxAbsElectronEta)
#    print '\t input collection:', str(process.EventFilter.electronInput)
#    print
#    print 'Muon skim:'
#    print '\t >=', str(process.EventFilter.minNElectrons),' muon with ',
#    print 'p_T > ', str(process.EventFilter.minMuonPt),
#    print '|eta| < ' , str(process.EventFilter.maxAbsMuonEta)
#    print '\t input collection:', str(process.EventFilter.muonInput)
#    print
#    print 'Use either lepton type:', str(process.EventFilter.counteitherleptontype)
#    print
#    print 'Jet skim:'
#    print '\t >=', str(process.EventFilter.minNJets),' jet with ',
#    print 'p_T > ', str(process.EventFilter.minJetPt),
#    print '|eta| < ' , str(process.EventFilter.maxAbsJetEta)
#    print '\t input collection:', str(process.EventFilter.jetInput)
#else:
#    print 'No skim used.'

from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams=pvSelector.clone(maxZ=cms.double(24.0),
                                     minNdof=cms.double(4.0) # this is >= 4
                                     ),
    src=cms.InputTag('offlinePrimaryVertices')
    )


###############################
########## Gen Setup ##########
###############################

process.load("RecoJets.Configuration.GenJetParticles_cff")
from RecoJets.JetProducers.ca4GenJets_cfi import ca4GenJets
process.ca8GenJetsNoNu = ca4GenJets.clone(rParam=cms.double(0.8),
                                           src=cms.InputTag("genParticlesForJetsNoNu"))

process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")


# prune gen particles
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
                                            src=cms.InputTag("genParticles"),
                                            select=cms.vstring(
                                                "drop  *"
                                                , "keep status = 3" #keeps  particles from the hard matrix element
                                                , "keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
                                                , "keep (abs(pdgId)  = 15) & status = 3" #keeps taus
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
#### Calo Jet Setup    ########
###############################
#this has to run after PF2PAT and before removeMCMatching
#see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookPAT38xChanges#Details_with_PF2PAT
if options.writeFat:
    from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection
    switchJetCollection(process,
                     jetCollection=cms.InputTag('ak5CaloJets'),
                     jetCorrLabel=caloJetCorrection,
                     doBTagging=True,
                     doType1MET=False,)

###############################
########## PF Setup ###########
###############################

# Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
from PhysicsTools.PatAlgos.tools.pfTools import *
postfix = "PFlow"
usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
process.pfPileUpPFlow.Enable = True
process.pfPileUpPFlow.Vertices = 'goodOfflinePrimaryVertices'
process.pfElectronsFromVertexPFlow.vertices = 'goodOfflinePrimaryVertices'
process.pfMuonsFromVertexPFlow.vertices = 'goodOfflinePrimaryVertices'

process.pfJetsPFlow.doAreaFastjet = True
process.pfJetsPFlow.doRhoFastjet = False
process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
if not options.forceCheckClosestZVertex :
    process.pfPileUpPFlow.checkClosestZVertex = False
    
#False == taus also in jet collection
process.pfNoTauPFlow.enable = False

print "setting up loose leptons"
# In order to have a coherent semileptonic channel also, add
# some "loose" leptons to do QCD estimates.
process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
    combinedIsolationCut=cms.double(999.0) 
    )

process.patMuonsLoosePFlow = process.patMuonsPFlow.clone(
    pfMuonSource=cms.InputTag("pfIsolatedMuonsLoosePFlow"),
     genParticleMatch=cms.InputTag("muonMatchLoosePFlow")
    )
tmp = process.muonMatchPFlow.src
adaptPFMuons(process, process.patMuonsLoosePFlow, "PFlow")
process.muonMatchPFlow.src = tmp

process.muonMatchLoosePFlow = process.muonMatchPFlow.clone(
    src=cms.InputTag("pfIsolatedMuonsLoosePFlow")
    )
process.muonMatchPFlow.src = "pfIsolatedMuonsPFlow"

process.selectedPatMuonsLoosePFlow = process.selectedPatMuonsPFlow.clone(
    src=cms.InputTag("patMuonsLoosePFlow")
    )

#electrons
process.pfIsolatedElectronsLoosePFlow = process.pfIsolatedElectronsPFlow.clone(
    combinedIsolationCut=cms.double(999.0) 
    )

process.patElectronsLoosePFlow = process.patElectronsPFlow.clone(
    pfElectronSource=cms.InputTag("pfIsolatedElectronsLoosePFlow")
    )
adaptPFElectrons(process, process.patElectronsLoosePFlow, "PFlow")

process.selectedPatElectronsLoosePFlow = process.selectedPatElectronsPFlow.clone(
    src=cms.InputTag("patElectronsLoosePFlow")
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
    removeMCMatching(process, ['All'])
    process.looseLeptonSequence.remove(process.muonMatchLoosePFlow)

print "setting up electron ID"
###############################
###### Electron ID ############
###############################

# NOTE: ADDING THE ELECTRON IDs FROM CiC ----- USED WITH 42X 
    

process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentificationV06_cfi')
process.load('RecoEgamma.ElectronIdentification.cutsInCategoriesElectronIdentification_cfi')

process.eidCiCSequence = cms.Sequence(
    process.eidVeryLoose * 
    process.eidLoose * 
    process.eidMedium * 
    process.eidTight * 
    process.eidSuperTight * 
    process.eidHyperTight1 * 
    process.eidHyperTight2 * 
    process.eidHyperTight3 * 
    process.eidHyperTight4 * 
    process.eidVeryLooseMC * 
    process.eidLooseMC * 
    process.eidMediumMC * 
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
            eidVeryLooseMC=cms.InputTag("eidVeryLooseMC"),
            eidLooseMC=cms.InputTag("eidLooseMC"),
            eidMediumMC=cms.InputTag("eidMediumMC"),
            eidTightMC=cms.InputTag("eidTightMC"),
            eidSuperTightMC=cms.InputTag("eidSuperTightMC"),
            eidHyperTight1MC=cms.InputTag("eidHyperTight1MC"),
            eidHyperTight2MC=cms.InputTag("eidHyperTight2MC"),
            eidHyperTight3MC=cms.InputTag("eidHyperTight3MC"),
            eidHyperTight4MC=cms.InputTag("eidHyperTight4MC"),
            #other ID
            eidVeryLoose=cms.InputTag("eidVeryLoose"),
            eidLoose=cms.InputTag("eidLoose"),
            eidMedium=cms.InputTag("eidMedium"),
            eidTight=cms.InputTag("eidTight"),
            eidSuperTight=cms.InputTag("eidSuperTight"),
            eidHyperTight1=cms.InputTag("eidHyperTight1"),
            eidHyperTight2=cms.InputTag("eidHyperTight2"),
            eidHyperTight3=cms.InputTag("eidHyperTight3"),
            eidHyperTight4=cms.InputTag("eidHyperTight4")               


            )


###############################
###### Bare KT 0.6 jets #######
###############################

from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets
process.kt6PFJetsPFlowVoronoi = kt4PFJets.clone(
    rParam = cms.double(0.6),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    voronoiRfact = cms.double(0.9)
    )
process.kt6PFJetsVoronoi = kt4PFJets.clone(
    rParam = cms.double(0.6),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True),
    Rho_EtaMax = cms.double(6.0),
    voronoiRfact = cms.double(0.9)
    )

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
process.kt4PFJetsPFlow = kt4PFJets.clone(
    rParam = cms.double(0.4),
    src = cms.InputTag('pfNoElectron'+postfix),
    doAreaFastjet = cms.bool(True),
    doRhoFastjet = cms.bool(True)
    )


###############################
###### Bare CA 0.8 jets #######
###############################
from RecoJets.JetProducers.ca4PFJets_cfi import ca4PFJets
process.ca8PFJetsPFlow = ca4PFJets.clone(
    rParam=cms.double(0.8),
    src=cms.InputTag('pfNoElectron' + postfix),
    doAreaFastjet=cms.bool(True),
    doRhoFastjet=cms.bool(True),
    Rho_EtaMax=cms.double(6.0),
    Ghost_EtaMax=cms.double(7.0)
    )

###############################
###### Jet Pruning Setup ######
###############################


## Pruned PF Jets
#from RecoJets.JetProducers.ak5PFJetsPruned_cfi import ak5PFJetsPruned
#process.caPrunedPFlow = ak5PFJetsPruned.clone(
#    src = cms.InputTag('pfNoElectron'+postfix),
#    jetAlgorithm = cms.string("CambridgeAachen"),
#    rParam       = cms.double(0.8),
#    doAreaFastjet = cms.bool(True)
#)
#
#
#process.caPrunedGen = process.ca8GenJetsNoNu.clone(
#    SubJetParameters,
#    usePruning = cms.bool(True),
#    useExplicitGhosts = cms.bool(True),
#    writeCompound = cms.bool(True),
#    jetCollInstanceName=cms.string("SubJets")
#)
#
#
################################
##### CATopTag Setup ###########
################################
#
## CATopJet PF Jets
## with adjacency 
#process.caTopTagPFlow = cms.EDProducer(
#    "CATopJetProducer",
#    PFJetParameters.clone( src = cms.InputTag('pfNoElectron'+postfix),
#                           doAreaFastjet = cms.bool(True),
#                           doRhoFastjet = cms.bool(False),                       
#                           ),
#    AnomalousCellParameters,
#    CATopJetParameters,
#    jetAlgorithm = cms.string("CambridgeAachen"),
#    rParam = cms.double(0.8),
#    writeCompound = cms.bool(True)
#    )
#
#process.CATopTagInfosPFlow = cms.EDProducer("CATopJetTagger",
#                                    src = cms.InputTag("caTopTagPFlow"),
#                                    TopMass = cms.double(171),
#                                    TopMassMin = cms.double(0.),
#                                    TopMassMax = cms.double(250.),
#                                    WMass = cms.double(80.4),
#                                    WMassMin = cms.double(0.0),
#                                    WMassMax = cms.double(200.0),
#                                    MinMassMin = cms.double(0.0),
#                                    MinMassMax = cms.double(200.0),
#                                    verbose = cms.bool(False)
#                                    )
#
#
#
#process.caTopTagGen = cms.EDProducer(
#    "CATopJetProducer",
#    GenJetParameters.clone(src = cms.InputTag("genParticlesForJetsNoNu"),
#                           doAreaFastjet = cms.bool(False),
#                           doRhoFastjet = cms.bool(False)),
#    AnomalousCellParameters,
#    CATopJetParameters,
#    jetAlgorithm = cms.string("CambridgeAachen"),
#    rParam = cms.double(0.8),
#    writeCompound = cms.bool(True)
#    )
#
#process.CATopTagInfosGen = cms.EDProducer("CATopJetTagger",
#                                          src = cms.InputTag("caTopTagGen"),
#                                          TopMass = cms.double(171),
#                                          TopMassMin = cms.double(0.),
#                                          TopMassMax = cms.double(250.),
#                                          WMass = cms.double(80.4),
#                                          WMassMin = cms.double(0.0),
#                                          WMassMax = cms.double(200.0),
#                                          MinMassMin = cms.double(0.0),
#                                          MinMassMax = cms.double(200.0),
#                                          verbose = cms.bool(False)
#                                          )

# CATopJet PF Jets

for ipostfix in [postfix] :
    for module in (
        getattr(process,"kt6PFJets"),
#        getattr(process,"kt6PFJetsVoronoi"),
        getattr(process,"kt6PFJets" + ipostfix),
        getattr(process,"kt4PFJets" + ipostfix),
#        getattr(process,"kt6PFJets" + ipostfix + "Voronoi"),
        getattr(process,"ca8PFJets" + ipostfix),        
#        getattr(process,"CATopTagInfos" + ipostfix),
#        getattr(process,"caTopTag" + ipostfix),
#        getattr(process,"caPruned" + ipostfix)
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


#addJetCollection(process, 
#                 cms.InputTag('caPrunedPFlow'),         # Jet collection; must be already in the event when patLayer0 sequence is executed
#                 'CA8Pruned', 'PF',
#                 doJTA=True,            # Run Jet-Track association & JetCharge
#                 doBTagging=True,       # Run b-tagging
#                 jetCorrLabel=inputJetCorrLabel,
#                 doType1MET=False,
#                 doL1Cleaning=False,
#                 doL1Counters=False,
#                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
#                 doJetID = False
#                 )
#
#
#
#addJetCollection(process, 
#                 cms.InputTag('caTopTagPFlow'),
#                 'CATopTag', 'PF',
#                 doJTA=True,
#                 doBTagging=True,
#                 jetCorrLabel=inputJetCorrLabel,
#                 doType1MET=False,
#                 doL1Cleaning=False,
#                 doL1Counters=False,
#                 genJetCollection = cms.InputTag("ca8GenJetsNoNu"),
#                 doJetID = False
#                 )

for icorr in [
#              process.patJetCorrFactorsCATopTagPF,
#              process.patJetCorrFactorsCA8PrunedPF,
              process.patJetCorrFactorsCA8PF 
              ] :
    icorr.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
    

###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
                process.patJetsCA8PF,
#                process.patJetsCA8PrunedPF,
#                process.patJetsCATopTagPF
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


# LikelihoodEle
process.load('RecoEgamma.ElectronIdentification.electronIdLikelihoodExt_cfi')
process.egammaIDLikelihood = process.eidLikelihoodExt.clone()

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
process.patJetsPFlow.userData.userFunctions = cms.vstring("? hasTagInfo('secondaryVertex') && tagInfoSecondaryVertex('secondaryVertex').nVertices() > 0 ? "
                                                      "tagInfoSecondaryVertex('secondaryVertex').secondaryVertex(0).p4().mass() : 0")
process.patJetsPFlow.userData.userFunctionLabels = cms.vstring('secvtxMass')

# CA8 jets
process.selectedPatJetsCA8PF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")

# CA8 Pruned jets
#process.selectedPatJetsCA8PrunedPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")

# CA8 TopJets
#process.selectedPatJetsCATopTagPF.cut = cms.string("pt > 20 & abs(rapidity) < 2.5")
#process.patJetsCATopTagPF.addTagInfos = True
#process.patJetsCATopTagPF.tagInfoSources = cms.VInputTag(
#    cms.InputTag('CATopTagInfosPFlow')
#    )

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
                                        filterParams=jetIDSelector.clone(),
                                        src=cms.InputTag("selectedPatJets")
                                        )

from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams=pfJetIDSelector.clone(),
                                        src=cms.InputTag("selectedPatJetsPFlow")
                                        )
process.goodPatJetsCA8PF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                        filterParams=pfJetIDSelector.clone(),
                                        src=cms.InputTag("selectedPatJetsCA8PF")
                                        )
#process.goodPatJetsCA8PrunedPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
#                                              filterParams=pfJetIDSelector.clone(),
#                                              src=cms.InputTag("selectedPatJetsCA8PrunedPF")
#                                              )
#process.goodPatJetsCATopTagPF = cms.EDFilter("PFJetIDSelectionFunctorFilter",
#                                             filterParams=pfJetIDSelector.clone(),
#                                             src=cms.InputTag("selectedPatJetsCATopTagPF")
#                                             )

# let it run


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
    process.EventFilter * 
    process.goodPatJetsCA8PF * 
#    process.goodPatJetsCA8PrunedPF * 
#    process.goodPatJetsCATopTagPF * 
    process.flavorHistorySeq# * 
#    process.prunedGenParticles * 
#    process.caPrunedGen * 
#    process.caTopTagGen * 
#    process.CATopTagInfosGen
    )

process.patseq.replace(process.goodOfflinePrimaryVertices,
                            process.goodOfflinePrimaryVertices * 
                            process.eidCiCSequence)

if options.useData == True :
    process.patseq.remove(process.genParticlesForJetsNoNu)
    process.patseq.remove(process.genJetParticles)    
    process.patseq.remove(process.ca8GenJetsNoNu)
    process.patseq.remove(process.flavorHistorySeq)
#    process.patseq.remove(process.caPrunedGen)
#    process.patseq.remove(process.caTopTagGen)
#    process.patseq.remove(process.CATopTagInfosGen)
#    process.patseq.remove(process.prunedGenParticles)

# HLT Trigger Report
process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
    HLTriggerResults=cms.InputTag("TriggerResults", "", options.hltProcess)
)

process.p0 = cms.Path(
    process.hlTrigReport * 
    process.egammaIDLikelihood *
    process.patseq
)

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
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_data_fat.root')
        process.out.fileName = cms.untracked.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_data_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_data.root')
        process.out.fileName = cms.untracked.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_data.root')
else :
    if options.writeFat :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_mc_fat.root')
        process.out.fileName = cms.untracked.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_mc_fat.root')
    else :
        process.TFileService.fileName = cms.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_mc.root')
        process.out.fileName = cms.untracked.string(outPutFilePrefix + 'PAT_Tuple_' + FILETAG + '_mc.root')


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
process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'keep *_goodPatJets_*_*',
    'drop patJets_selectedPat*_*_*',
    'drop *_selectedPatJets_*_*',
    'drop *_selectedPatElectrons*_*_*',
    'keep *_selectedPatElectronsLoosePFlow*_*_*',
    'keep *_patMETsPFlow*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
#    'keep *_kt6PFJets*_*_*',
    'keep *_goodOfflinePrimaryVertices*_*_*',
    'drop patPFParticles_*_*_*',
    'drop patTaus_*_*_*',
#    'keep recoPFJets_caPruned*_*_*',
#    'keep recoPFJets_caTopTag*_*_*',
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
    'keep double_*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJetsNoNu_*_*',
    'keep *_ca8GenJetsNoNu_*_*',
#    'keep *_caPrunedGen_*_*',
#    'keep *_caTopTagPFlow_*_*',
#    'keep *_caPrunedPFlow_*_*',
#    'keep *_CATopTagInfosPFlow_*_*',
#    'keep *_prunedGenParticles_*_*',
    'drop recoPFCandidates_selectedPatJets*_*_*',
    'drop CaloTowers_selectedPatJets*_*_*'
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
    
#open('junk.py','w').write(process.dumpPython())
