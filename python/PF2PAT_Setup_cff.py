vertexCollection = 'goodOfflinePrimaryVertices'
from PhysicsTools.PatAlgos.tools.pfTools import *

def setup_PF2PAT(process, cms, options, postfix="PFlow", removeTausFromJetCollection=False):
    ###############################
    ########## PF Setup ###########
    ###############################
    print '=' * 60
    print "Setting up PF2PAT"
    print '=' * 60

    #MC setup
    inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute'])
    
    if options.useData :#data set up
        inputJetCorrLabel = ('AK5PFchs', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])

    # manually adding type0 corrections in the sequence: has to be done before setting up PF2PAT
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    process.producePatPFMETCorrections.replace(process.pfCandMETcorr,
                                               process.type0PFMEtCorrection *
                                               process.patPFMETtype0Corr *
                                               process.pfCandMETcorr
                                               )
    
    # Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff.
    # Separate configs for 44X and 52X (as per different JEC prescriptions)
    # see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections
    if options.CMSSW == '44X':
        usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix, typeIMetCorrections=False)
        process.pfPileUpPFlow.Enable = True
        process.pfPileUpPFlow.Vertices = vertexCollection
        process.pfElectronsFromVertexPFlow.vertices = vertexCollection
        process.pfMuonsFromVertexPFlow.vertices = vertexCollection
        process.pfJetsPFlow.doAreaFastjet = True
        process.pfJetsPFlow.doRhoFastjet = False
        #process.patJetCorrFactorsPFlow.payload = inputJetCorrLabel[0]
        #process.patJetCorrFactorsPFlow.levels = inputJetCorrLabel[1]
        process.patJetCorrFactorsPFlow.rho = cms.InputTag("kt6PFJetsPFlow", "rho")
    else:
        usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix, typeIMetCorrections=not options.setupMETmanually,
                  jetCorrections=inputJetCorrLabel,
                  pvCollection=cms.InputTag('goodOfflinePrimaryVertices')
                  )

    #need to debug loose PF leptons, only introduced as a preliminary switch
    if options.useGSFelectrons:
        useGsfElectrons(process,postfix)
        
    if not options.forceCheckClosestZVertex :
        process.pfPileUpPFlow.checkClosestZVertex = False

    #False == taus also in jet collection
    process.pfNoTauPFlow.enable = removeTausFromJetCollection


def setup_looseLeptons(process, cms, options, postfix="PFlow", maxLooseLeptonRelIso=999):
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
    
    #electrons - need to properly adjust to GSF-electrons case
    if not options.useGSFelectrons:
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
