def setup_eventfilters(process, cms, options):
    print '=' * 60
    print "Setting up Event Filters"
    print '=' * 60
    setup_HBHENoiseFilter(process, cms)
    setup_skim(process, cms, options)
    
def setup_HBHENoiseFilter(process, cms):
    print '=' * 60
    print "Setting up HBHE Noise Filter"
    print '=' * 60
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
    
def setup_skim(process, cms, options):
    print '=' * 60
    print "Setting up skim"
    print '=' * 60
    skim = options.skim
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
    
    skim = skim.lower()
    if 'electron' in skim or 'lepton' in skim:
        process.EventFilter.maxAbsElectronEta   = cms.double(2.5)#within tracker volume
        #electron multiplicity
        if 'di' in skim:
            process.EventFilter.minNElectrons       = cms.int32(2)
        else:
            process.EventFilter.minNElectrons       = cms.int32(1)
        
        if 'loose' in skim:#loose Pt cut
            process.EventFilter.minElectronPt       = cms.double(20.)
            process.EventFilter.electronInput = cms.InputTag("selectedPatElectrons")#GSF electrons
        else:
            process.EventFilter.minElectronPt       = cms.double(30.)
            process.EventFilter.electronInput = cms.InputTag("selectedPatElectronsLoosePFlow")
    
    if 'muon'  in skim or 'lepton' in skim:
        #muon multiplicity
        if 'di' in skim:
            process.EventFilter.minNMuons       = cms.int32(2)
        else:
            process.EventFilter.minNMuons       = cms.int32(1)
        if 'loose' in skim:#loose Pt cut and eta cut
            process.EventFilter.maxAbsMuonEta   = cms.double(2.5)#within tracker volume
            process.EventFilter.minMuonPt       = cms.double(10.)
            process.EventFilter.muonInput = cms.InputTag("selectedPatMuons")
        else:
            process.EventFilter.minMuonPt       = cms.double(20.)#triggers are 17GeV
            process.EventFilter.maxAbsMuonEta   = cms.double(2.1)#new triggers have this restriction anyway
            process.EventFilter.muonInput = cms.InputTag("selectedPatMuonsLoosePFlow")
    
    if 'lepton' in skim:
        process.EventFilter.counteitherleptontype = cms.untracked.bool(True)
 
    #jet skim
    #unprescaled triggers are >=3/>=2 jets for electron/muon triggers
    if 'jet' in skim:
        find = skim.find('jet')
        nJets = int(skim[find - 1])
        process.EventFilter.jetInput = cms.InputTag("selectedPatJetsPFlow")
        process.EventFilter.minNJets = cms.int32(nJets)
        process.EventFilter.minJetPt = cms.double(30.)# identical (within JEC) to trigger
        process.EventFilter.maxAbsJetEta = cms.double(2.6)# identical to trigger
    
    
    if not (skim == '' or skim == 'noskim'):
        print '='*10, 'Skim definition', '='*10
        print 'Electron skim:'
        print '\t >=', str(process.EventFilter.minNMuons),' electron with ',
        print 'p_T > ', str(process.EventFilter.minElectronPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsElectronEta)
        print '\t input collection:', str(process.EventFilter.electronInput)
        print
        print 'Muon skim:'
        print '\t >=', str(process.EventFilter.minNElectrons),' muon with ',
        print 'p_T > ', str(process.EventFilter.minMuonPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsMuonEta)
        print '\t input collection:', str(process.EventFilter.muonInput)
        print
        print 'Use either lepton type:', str(process.EventFilter.counteitherleptontype)
        print
        print 'Jet skim:'
        print '\t >=', str(process.EventFilter.minNJets),' jet with ',
        print 'p_T > ', str(process.EventFilter.minJetPt),
        print '|eta| < ' , str(process.EventFilter.maxAbsJetEta)
        print '\t input collection:', str(process.EventFilter.jetInput)
    else:
        print 'No skim used.'