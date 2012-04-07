# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

#set up analysis
#https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
GLOBALTAG_DATA_44X = 'GR_R_44_V15::All'
GLOBALTAG_MC_44X = 'START44_V13::All'
FILETAG_44X = '44X'

GLOBALTAG_DATA = 'GR_R_52_V7::All'
GLOBALTAG_MC = 'START52_V9::All'
FILETAG = '52X'

USE_JEC_FROM_DB = False
removeTausFromJetCollection = False
maxLooseLeptonRelIso = 999.0
includeCA08Jets = False
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

options.register ('use52X',
                  True,
                  VarParsing.multiplicity.singleton,
                  VarParsing.varType.bool,
                  "Run this in CMSSW 52X. If false it will use CMSSW 44X")

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


options.parseArguments()

maxLooseLeptonRelIso = options.maxLooseLeptonRelIso

if USE_JEC_FROM_DB:
    print "Loading JEC from database"
    from BristolAnalysis.NTupleTools.custom_JEC_cff import *
    configureCustomJEC(process, cms)

if options.use52X:
    if not options.useData :
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/DYJets_M50_Summer12.root'
            ]
    else:
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/ElectronHad_Run2011A_44X_AOD.root'
            ]
else:
    GLOBALTAG_DATA = GLOBALTAG_DATA_44X
    GLOBALTAG_MC = GLOBALTAG_MC_44X
    FILETAG = FILETAG_44X
    if not options.useData :
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/TTJets_TuneZ1_Fall11_44X_AODSIM.root'
            ]
    else :
        process.source.fileNames = [
            'file:///storage/TopQuarkGroup/ElectronHad_Run2011A_44X_AOD.root'
            ]


if not options.useData :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute'])
else :
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
    caloJetCorrection = ('AK5Calo', ['L1Offset' , 'L2Relative', 'L3Absolute', 'L2L3Residual'])

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

#process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")

# add the flavor history
process.load("PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi")


# prune gen particles
#process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
#process.prunedGenParticles = cms.EDProducer("GenParticlePruner",
#                                            src=cms.InputTag("genParticles"),
#                                            select=cms.vstring(
#                                                "drop  *"
#                                                , "keep status = 3" #keeps  particles from the hard matrix element
#                                                , "keep (abs(pdgId) >= 11 & abs(pdgId) <= 16) & status = 1" #keeps e/mu and nus with status 1
#                                                , "keep (abs(pdgId)  = 15) & status = 3" #keeps taus
#                                                )
#                                            )

###############################
#### Jet RECO includes ########
###############################

from RecoJets.JetProducers.SubJetParameters_cfi import SubJetParameters
from RecoJets.JetProducers.PFJetParameters_cfi import *
from RecoJets.JetProducers.CaloJetParameters_cfi import *
from RecoJets.JetProducers.AnomalousCellParameters_cfi import *
#from RecoJets.JetProducers.CATopJetParameters_cfi import *
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
process.pfNoTauPFlow.enable = removeTausFromJetCollection

print "setting up loose leptons"
# In order to have a coherent semileptonic channel also, add
# some "loose" leptons to do QCD estimates.
process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
    isolationCut=cms.double(maxLooseLeptonRelIso) 
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
    isolationCut=cms.double(maxLooseLeptonRelIso) 
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
#process.kt6PFJetsPFlowVoronoi = kt4PFJets.clone(
#    rParam = cms.double(0.6),
#    src = cms.InputTag('pfNoElectron'+postfix),
#    doAreaFastjet = cms.bool(True),
#    doRhoFastjet = cms.bool(True),
#    Rho_EtaMax = cms.double(6.0),
#    voronoiRfact = cms.double(0.9)
#    )
#process.kt6PFJetsVoronoi = kt4PFJets.clone(
#    rParam = cms.double(0.6),
#    doAreaFastjet = cms.bool(True),
#    doRhoFastjet = cms.bool(True),
#    Rho_EtaMax = cms.double(6.0),
#    voronoiRfact = cms.double(0.9)
#    )

process.kt6PFJets = kt4PFJets.clone(
    rParam=cms.double(0.6),
    doAreaFastjet=cms.bool(True),
    doRhoFastjet=cms.bool(True)
    )
process.kt6PFJetsPFlow = kt4PFJets.clone(
    rParam=cms.double(0.6),
    src=cms.InputTag('pfNoElectron' + postfix),
    doAreaFastjet=cms.bool(True),
    doRhoFastjet=cms.bool(True)
    )
process.kt4PFJetsPFlow = kt4PFJets.clone(
    rParam=cms.double(0.4),
    src=cms.InputTag('pfNoElectron' + postfix),
    doAreaFastjet=cms.bool(True),
    doRhoFastjet=cms.bool(True)
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


for ipostfix in [postfix] :
    for module in (
        getattr(process, "kt6PFJets"),
        getattr(process, "kt6PFJets" + ipostfix),
        getattr(process, "kt4PFJets" + ipostfix),
        getattr(process, "ca8PFJets" + ipostfix),
        ) :
        getattr(process, "patPF2PATSequence" + ipostfix).replace(getattr(process, "pfNoElectron" + ipostfix), getattr(process, "pfNoElectron" + ipostfix) * module)


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
                 cms.InputTag('ca8PFJetsPFlow'), # Jet collection; must be already in the event when patLayer0 sequence is executed
                 'CA8', 'PF',
                 doJTA=True, # Run Jet-Track association & JetCharge
                 doBTagging=True, # Run b-tagging
                 jetCorrLabel=inputJetCorrLabel,
                 doType1MET=False,
                 doL1Cleaning=False,
                 doL1Counters=False,
                 genJetCollection=cms.InputTag("ca8GenJetsNoNu"),
                 doJetID=False
                 )



for icorr in [
              process.patJetCorrFactorsCA8PF 
              ] :
    icorr.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
    

###############################
### TagInfo and Matching Setup#
###############################

# Do some configuration of the jet substructure things
for jetcoll in (process.patJetsPFlow,
                process.patJetsCA8PF,
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
    process.flavorHistorySeq# * 
    )

process.patseq.replace(process.goodOfflinePrimaryVertices,
                            process.goodOfflinePrimaryVertices * 
                            process.eidCiCSequence)

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
#PF2PAT jets
process.rootTuplePF2PATJets.InputTag = cms.InputTag('goodPatJetsPFlow')
process.rootTuplePF2PATJets.Prefix = cms.string('goodPatJetsPFlow.')
#Cambridge-Aachen cone 0.8 jets
process.rootTupleCA8PFJets = process.rootTuplePF2PATJets.clone()
process.rootTupleCA8PFJets.InputTag = cms.InputTag('goodPatJetsCA8PF')
process.rootTupleCA8PFJets.Prefix = cms.string('goodPatJetsCA8PF.')
#selection on GenParticles
process.rootTupleGenParticles.minPt = cms.double(-1)
process.rootTupleGenParticles.maxAbsoluteEta = cms.double(100)

#GSF Electrons
process.rootTupleElectrons.InputTag = cms.InputTag('selectedPatElectrons')
process.rootTupleElectrons.Prefix = cms.string('selectedPatElectrons.')
#isolated PF Electrons
process.rootTuplePFElectrons.InputTag = cms.InputTag('selectedPatElectronsPFlow')
process.rootTuplePFElectrons.Prefix = cms.string('selectedPatElectronsPFlow.')
#non-isolated PF electrons
process.rootTuplePFLooseElectrons.InputTag = cms.InputTag('selectedPatElectronsLoosePFlow')
process.rootTuplePFLooseElectrons.Prefix = cms.string('selectedPatElectronsLoosePFlow.')

#muons
process.nTupleMuons.InputTag = cms.InputTag('selectedPatMuons')
process.nTupleMuons.Prefix = cms.string('selectedPatMuons.')
#standard PF muons
process.nTuplePFMuons.InputTag = cms.InputTag('selectedPatMuonsPFlow')
process.nTuplePFMuons.Prefix = cms.string('selectedPatMuonsPFlow.')
#non isolated PF muons
process.nTuplePFLooseMuons.InputTag = cms.InputTag('selectedPatMuonsLoosePFlow')
process.nTuplePFLooseMuons.Prefix = cms.string('selectedPatMuonsLoosePFlow.')
#PF taus
process.rootTupleTaus.InputTag = cms.InputTag('selectedPatTausPFlow')
process.rootTupleTaus.Prefix = cms.string('selectedPatTausPFlow.')
#PF photons
process.rootTuplePhotons.InputTag = cms.InputTag('patPhotons')
process.rootTuplePhotons.Prefix = cms.string('patPhotons.')
#trigger
process.rootTupleTrigger.HLTInputTag = cms.InputTag('TriggerResults', '', options.hltProcess)

process.rootTupleTree = cms.EDAnalyzer("RootTupleMakerV2_Tree",
    outputCommands=cms.untracked.vstring(
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
        'keep *_rootTuplePFLooseElectrons_*_*',
        #MET
        'keep *_rootTupleCaloMET_*_*',
        'keep *_rootTuplePFMET_*_*',
        #muons
        'keep *_nTupleMuons_*_*',
        'keep *_nTuplePFMuons_*_*',
        'keep *_nTuplePFLooseMuons_*_*',
        #taus
        'keep *_rootTupleTaus_*_*',
        #photons
        'keep *_rootTuplePhotons_*_*',
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
    process.rootTuplePFLooseElectrons + 
    #muons
    process.nTuplePFMuons + 
    process.nTuplePFLooseMuons + 
    process.nTupleMuons + 
    #taus
    process.rootTupleTaus + 
    #photons
    process.rootTuplePhotons + 
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
    process.rootTupleGenMETTrue) * 
    process.rootTupleTree)

if not includeCA08Jets:
    process.patseq.remove(process.goodPatJetsCA8PF)
    process.rootNTuples.remove(process.rootTupleCA8PFJets)
    
    
if options.useData:
    process.patseq.remove(process.genParticlesForJetsNoNu)
    process.patseq.remove(process.genJetParticles)    
    process.patseq.remove(process.ca8GenJetsNoNu)
    process.patseq.remove(process.flavorHistorySeq)
    process.rootNTuples.remove(process.rootTupleGenEventInfo)
    process.rootNTuples.remove(process.rootTupleGenParticles)
    process.rootNTuples.remove(process.rootTupleGenJetSequence)
    process.rootNTuples.remove(process.rootTupleGenMETTrue)
    
if not options.writeFat:#write only PF particles
    process.rootNTuples.remove(process.rootTupleCaloJets)
    process.rootNTuples.remove(process.rootTupleCaloMET)
    process.rootNTuples.remove(process.rootTupleElectrons)
    process.rootNTuples.remove(process.nTupleMuons)

if not options.writeFat and not options.writeIsolatedPFLeptons:#write only PF particles
    #isolated leptons
    process.rootNTuples.remove(process.rootTuplePFElectrons)
    process.rootNTuples.remove(process.nTuplePFMuons)
    
# HLT Trigger Report
process.hlTrigReport = cms.EDAnalyzer("HLTrigReport",
    HLTriggerResults=cms.InputTag("TriggerResults", "", options.hltProcess)
)


process.p0 = cms.Path(
                      process.hlTrigReport * 
                      process.egammaIDLikelihood * 
                      process.patseq * 
                      process.rootNTuples
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
process.out.outputCommands = [
    'drop *_cleanPat*_*_*',
    'keep *_selectedPat*_*_*',
    'keep *_goodPat*_*_*',
    'drop patJets_selectedPat*_*_*',
    'drop *_selectedPatJets_*_*',
    'keep *_patMETs*_*_*',
#    'keep *_offlinePrimaryVertices*_*_*',
#    'keep *_kt6PFJets*_*_*',
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
    'keep double_*_*_PAT',
    'keep *_TriggerResults_*_*',
    'keep *_hltTriggerSummaryAOD_*_*',
    'keep *_ak5GenJetsNoNu_*_*',
    'keep *_ca8GenJetsNoNu_*_*',
    'keep *_caPrunedGen_*_*',
    'keep *_caTopTagPFlow_*_*',
    'keep *_caPrunedPFlow_*_*',
    'keep *_CATopTagInfosPFlow_*_*',
    'keep *_prunedGenParticles_*_*',
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
    
#do not write PAT-tuple information
del process.outpath
