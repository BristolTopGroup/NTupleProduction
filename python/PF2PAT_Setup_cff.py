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

    # Default PF2PAT with AK5 jets. Make sure to turn ON the L1fastjet stuff.
    # Separate configs for 44X and 52X (as per different JEC prescriptions)
    # see https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    if options.use44X:
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
        usePF2PAT(process, runPF2PAT=True, jetAlgo='AK5', runOnMC=not options.useData, postfix=postfix, typeIMetCorrections=False,
                  jetCorrections=inputJetCorrLabel,
                  pvCollection=cms.InputTag('goodOfflinePrimaryVertices')
                  )

    #need to debug loose PF leptons, only introduced as a preliminary switch
    if options.useGSFelectrons:
        useGsfElectrons(process,postfix)
        
    if not options.forceCheckClosestZVertex :
        process.pfPileUpPFlow.checkClosestZVertex = False

    #PFMET setup: following by-hand recipe from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMetAnalysis#Type_I_II_0_with_PF2PAT
    process.load("PhysicsTools.PatUtils.patPFMETCorrections_cff")
    getattr(process,'patPF2PATSequence'+postfix).remove(getattr(process,'patMETs'+postfix))

    from PhysicsTools.PatAlgos.tools.helpers import cloneProcessingSnippet
    cloneProcessingSnippet(process, process.producePatPFMETCorrections, postfix)

    getattr(process,'selectedPatJetsForMETtype1p2Corr'+postfix).src = cms.InputTag('selectedPatJets'+postfix)
    getattr(process,'selectedPatJetsForMETtype2Corr'+postfix).src = cms.InputTag('selectedPatJets'+postfix)
    getattr(process,'pfCandMETcorr'+postfix).src = cms.InputTag('pfNoJet'+postfix)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).type1JetPtThreshold = cms.double(10.0)
    getattr(process,'patType1CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
    cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
    #cms.InputTag("patPFMETtype0Corr"+postfix) ###uncomment this line to include type-0 corrections
    )
    getattr(process,'patType1p2CorrectedPFMet'+postfix).srcType1Corrections = cms.VInputTag(
        cms.InputTag("patPFJetMETtype1p2Corr"+postfix,"type1"),
        #cms.InputTag("patPFMETtype0Corr"+postfix) ###uncomment this line to include type-0 corrections
        )
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype1p2Corr'+postfix).skipMuons = cms.bool(False)
    getattr(process,'patPFJetMETtype2Corr'+postfix).skipEM = cms.bool(False)
    getattr(process,'patPFJetMETtype2Corr'+postfix).skipMuons = cms.bool(False)

    ##for type I+II corrections, switch this to patType1p2CorrectedPFMet
    getattr(process,'patMETs'+postfix).metSource = cms.InputTag('patType1CorrectedPFMet'+postfix)

    getattr(process,'patDefaultSequence'+postfix).remove(getattr(process,'patMETs'+postfix))

    if options.useData:
        getattr(process,'patPFJetMETtype1p2Corr'+postfix).jetCorrLabel = 'L2L3Residual'
        getattr(process,'patPFJetMETtype2Corr'+postfix).jetCorrLabel = 'L2L3Residual'

    getattr(process,'patPFMet'+postfix).addGenMET = cms.bool(not options.useData)
    process.patPFMet.addGenMET = cms.bool(not options.useData)

    
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
