vertexCollection = 'goodOfflinePrimaryVertices'
from PhysicsTools.PatAlgos.tools.pfTools import *

def setup_PF2PAT(process, cms, options, postfix="PFlow", removeTausFromJetCollection=False):
    ###############################
    ########## PF Setup ###########
    ###############################
    print '=' * 60
    print "Setting up PF2PAT"
    print '=' * 60

    # Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff. 
    usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix)
    process.pfPileUpPFlow.Enable = True
    process.pfPileUpPFlow.Vertices = vertexCollection
    process.pfElectronsFromVertexPFlow.vertices = vertexCollection
    process.pfMuonsFromVertexPFlow.vertices = vertexCollection
    
    process.pfJetsPFlow.doAreaFastjet = True
    process.pfJetsPFlow.doRhoFastjet = False
#    process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
#    process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
    process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
    if not options.forceCheckClosestZVertex :
        process.pfPileUpPFlow.checkClosestZVertex = False
        
    #False == taus also in jet collection
    process.pfNoTauPFlow.enable = removeTausFromJetCollection
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    process.patPFJetMETtype1p2Corr.type1JetPtThreshold = cms.double(10.0)
    process.patPFJetMETtype1p2Corr.skipEM = cms.bool(False)
    process.patPFJetMETtype1p2Corr.skipMuons = cms.bool(False)
    process.patPFMet.addGenMET = cms.bool(not options.useData)


def setup_looseLeptons(process, cms, postfix="PFlow", maxLooseLeptonRelIso=999):
    print '=' * 60
    print "Setting up loose leptons"
    print '=' * 60
    
    # In order to have a coherent semileptonic channel also, add
    # some "loose" leptons to do QCD estimates.
    process.pfIsolatedMuonsLoosePFlow = process.pfIsolatedMuonsPFlow.clone(
        isolationCut=cms.double(maxLooseLeptonRelIso) 
        )
    
    process.patMuonsLoosePFlow = process.patMuonsPFlow.clone(
        pfMuonSource=cms.InputTag("pfIsolatedMuonsLoose" + postfix),
         genParticleMatch=cms.InputTag("muonMatchLoose" + postfix)
        )
    tmp = process.muonMatchPFlow.src
    adaptPFMuons(process, process.patMuonsLoosePFlow, postfix)
    process.muonMatchPFlow.src = tmp
    
    process.muonMatchLoosePFlow = process.muonMatchPFlow.clone(
        src=cms.InputTag("pfIsolatedMuonsLoose" + postfix)
        )
    process.muonMatchPFlow.src = "pfIsolatedMuons" + postfix
    
    process.selectedPatMuonsLoosePFlow = process.selectedPatMuonsPFlow.clone(
        src=cms.InputTag("patMuonsLoose" + postfix)
        )
    
    #electrons
    process.pfIsolatedElectronsLoosePFlow = process.pfIsolatedElectronsPFlow.clone(
        isolationCut=cms.double(maxLooseLeptonRelIso) 
        )
    
    process.patElectronsLoosePFlow = process.patElectronsPFlow.clone(
        pfElectronSource=cms.InputTag("pfIsolatedElectronsLoose" + postfix)
        )
    adaptPFElectrons(process, process.patElectronsLoosePFlow, postfix)
    
    process.selectedPatElectronsLoosePFlow = process.selectedPatElectronsPFlow.clone(
        src=cms.InputTag("patElectronsLoose" + postfix)
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
    
    # Use the good primary vertices everywhere. 
    for imod in [process.patMuonsPFlow,
                 process.patMuonsLoosePFlow,
                 process.patElectronsPFlow,
                 process.patElectronsLoosePFlow,
                 process.patMuons,
                 process.patElectrons] :
        imod.pvSrc = vertexCollection
        imod.embedTrack = True
