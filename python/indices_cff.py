# This is currently a very bad fix for what we are doing.
# Since selections no longer define our physics objects, we need to create
# the whole set of mappings.
# Once we remove AnalysisSoftware from our stack, this will become obsolete.

from BristolAnalysis.NTupleTools.indexProducer_cfi import indexProducer
indexProducers = []
electronIndices = {
    'signalElectronIndices': {
        'original': 'electronUserData',
        'new': {
            'signal': 'goodElectrons',
            'controlRegion1': 'goodConversionElectrons',
            'controlRegion2': 'goodNonIsoElectrons',
        }
    },
    'vetoElectronIndices': {
        'original': 'electronUserData',
        'new': {
            'signal': 'vetoElectrons',
            'controlRegion1': 'vetoElectrons',
            'controlRegion2': 'vetoElectrons',
        }
    },
    'vetoMuonIndices': {
        'original': 'muonUserData',
        'new': {
            'signal': 'vetoMuons',
            'controlRegion1': 'vetoMuons',
            'controlRegion2': 'vetoMuons',
        }
    },
    'cleanedJetIndex': {
        'original': 'electronUserData',
        'new': {
            'signal': 'goodJets',
            'controlRegion1': 'goodJetsEConversionRegion',
            'controlRegion2': 'goodJetsENonIsoRegion',
        }
    },
    'cleanedBJetIndex': {
        'original': 'jetUserData',
        'new': {
            'signal': 'goodBJets',
            'controlRegion1': 'goodBJetsEConversionRegion',
            'controlRegion2': 'goodBJetsENonIsoRegion',
        }
    },
    'cleanedTightBJetIndex': {
        'original': 'electronUserData',
        'new': {
            'signal': 'goodTightBJets',
            'controlRegion1': 'goodTightBJetsEConversionRegion',
            'controlRegion2': 'goodTightBJetsENonIsoRegion',
        }
    }
}
muonIndices = {
    'signalMuonIndices': {
        'original': 'muonUserData',
        'new': {
            'signal': 'goodMuons',
            'controlRegion1': 'goodNonIsoR1Muons',
            'controlRegion2': 'goodNonIsoR2Muons',
        }
    },
    'vetoElectronIndices': {
        'original': 'electronUserData',
        'new': {
            'signal': 'vetoElectrons',
            'controlRegion1': 'vetoElectrons',
            'controlRegion2': 'vetoElectrons',
        }
    },
    'vetoMuonIndices': {
        'original': 'muonUserData',
        'new': {
            'signal': 'vetoMuons',
            'controlRegion1': 'vetoMuons',
            'controlRegion2': 'vetoMuons',
        }
    },
    'cleanedJetIndex': {
        'original': 'electronUserData',
        'new': {
            'signal': 'goodJets',
            'controlRegion1': 'goodJetsMuNonIsoR1Region',
            'controlRegion2': 'goodJetsMuNonIsoR2Region',
        }
    },
    'cleanedBJetIndex': {
        'original': 'jetUserData',
        'new': {
            'signal': 'goodBJets',
            'controlRegion1': 'goodBJetsMuNonIsoR1Region',
            'controlRegion2': 'goodBJetsMuNonIsoR2Region',
        }
    },
    'cleanedTightBJetIndex': {
        'original': 'electronUserData',
        'new': {
            'signal': 'goodTightBJets',
            'controlRegion1': 'goodTightBJetsMuNonIsoR1Region',
            'controlRegion2': 'goodTightBJetsMuNonIsoR2Region',
        }
    }
}
muonRegions = {
    'signal': 'TopPairMuonPlusJetsSelectionFilter',
    'controlRegion1': 'TopPairMuonPlusJetsQCDSelection1p5to3',
    'controlRegion2': 'TopPairMuonPlusJetsQCDSelection3toInf',
}
electronRegions = {
    'signal': 'TopPairElectronPlusJetsSelection',
    'controlRegion1': 'TopPairElectronPlusJetsConversionSelection',
    'controlRegion2': 'TopPairElectronPlusJetsQCDSelection',
}


def create_index_producer(channel, indexName, selection):
    global electronIndices, muonIndices, electronRegions, muonRegions
    indices = electronIndices
    regions = electronRegions
    if channel.lower() == 'mu':
        indices = muonIndices
        regions = muonRegions
    inputs = indices[indexName]
    return indexProducer.clone(
        outputName='{0}.{1}'.format(regions[selection], indexName),
        originalCollection=inputs['original'],
        newCollection=inputs['new'][selection],
    )

###############################################################################
# Signal region
###############################################################################
# signal leptons
region = 'signal'
signalElectronIndices = create_index_producer('e', 'signalElectronIndices', region)
indexProducers.append(signalElectronIndices)

signalMuonIndices = create_index_producer('mu', 'signalMuonIndices', region)
indexProducers.append(signalMuonIndices)
# veto leptons
vetoElectronIndicesESel = create_index_producer('e', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesESel)

vetoElectronIndicesMuSel = create_index_producer('mu', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesMuSel)

vetoMuonIndicesESel = create_index_producer('e', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesESel)

vetoMuonIndicesMuSel = create_index_producer('mu', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesMuSel)

# jets for signal selection
goodJetIndicesESel = create_index_producer('e', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesESel)

goodJetIndicesMuSel = create_index_producer('mu', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesMuSel)
# b-tagged jets (medium WP) for signal selection
goodBJetIndicesESel = create_index_producer('e', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesESel)

goodBJetIndicesMuSel = create_index_producer('mu', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesMuSel)
# b-tagged jets (tight WP) for signal selection
goodTightBJetIndicesESel = create_index_producer('e', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesESel)

goodTightBJetIndicesMuSel = create_index_producer('mu', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesMuSel)

###############################################################################
# Control region 1
###############################################################################
region = 'controlRegion1'
# signal leptons
conversionElectronIndices = create_index_producer('e', 'signalElectronIndices', region)
indexProducers.append(conversionElectronIndices)

nonIsoR1MuonIndices = create_index_producer('mu', 'signalMuonIndices', region)
indexProducers.append(nonIsoR1MuonIndices)
# veto leptons
vetoElectronIndicesEConvSel = create_index_producer('e', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesEConvSel)

vetoElectronIndicesMuNonIsoR1Sel = create_index_producer('mu', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesMuNonIsoR1Sel)

vetoMuonIndicesEConvSel = create_index_producer('e', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesEConvSel)

vetoMuonIndicesMuNonIsoR1Sel = create_index_producer('mu', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesMuNonIsoR1Sel)
# jets
goodJetIndicesEConvSel = create_index_producer('e', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesEConvSel)

goodJetIndicesMuNonIsoR1Sel = create_index_producer('mu', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesMuNonIsoR1Sel)
# b-tagged jets (medium WP) for signal selection
goodBJetIndicesEConvSel = create_index_producer('e', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesEConvSel)

goodBJetIndicesMuNonIsoR1Sel = create_index_producer('mu', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesMuNonIsoR1Sel)
# b-tagged jets (tight WP) for signal selection
goodTightBJetIndicesEConvSel = create_index_producer('e', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesEConvSel)

goodTightBJetIndicesMuNonIsoR1Sel = create_index_producer('mu', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesMuNonIsoR1Sel)

###############################################################################
# Control region 2
###############################################################################
region = 'controlRegion2'
# signal leptons
nonIsoElectronIndices = create_index_producer('e', 'signalElectronIndices', region)
indexProducers.append(nonIsoElectronIndices)

nonIsoR2MuonIndices = create_index_producer('mu', 'signalMuonIndices', region)
indexProducers.append(nonIsoR2MuonIndices)
# veto leptons
vetoElectronIndicesENonIsoSel = create_index_producer('e', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesENonIsoSel)

vetoElectronIndicesMuNonIsoR2Sel = create_index_producer('mu', 'vetoElectronIndices', region)
indexProducers.append(vetoElectronIndicesMuNonIsoR2Sel)

vetoMuonIndicesENonIsoSel = create_index_producer('e', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesENonIsoSel)

vetoMuonIndicesMuNonIsoR2Sel = create_index_producer('mu', 'vetoMuonIndices', region)
indexProducers.append(vetoMuonIndicesMuNonIsoR2Sel)
# jets
goodJetIndicesENonIsoSel = create_index_producer('e', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesENonIsoSel)

goodJetIndicesMuNonIsoR2Sel = create_index_producer('mu', 'cleanedJetIndex', region)
indexProducers.append(goodJetIndicesMuNonIsoR2Sel)
# b-tagged jets (medium WP) for signal selection
goodBJetIndicesENonIsoSel = create_index_producer('e', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesENonIsoSel)

goodBJetIndicesMuNonIsoR2Sel = create_index_producer('mu', 'cleanedBJetIndex', region)
indexProducers.append(goodBJetIndicesMuNonIsoR2Sel)
# b-tagged jets (tight WP) for signal selection
goodTightBJetIndicesENonIsoSel = create_index_producer('e', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesENonIsoSel)

goodTightBJetIndicesMuNonIsoR2Sel = create_index_producer('mu', 'cleanedTightBJetIndex', region)
indexProducers.append(goodTightBJetIndicesMuNonIsoR2Sel)

import FWCore.ParameterSet.Config as cms
# indexSequence = cms.Sequence(sum(indexProducers))
# simple sum(indexProducers) does not work as radd (recursive add) is not
# implemented for cms.EDProducer
indexSequence = cms.Sequence(reduce(lambda x, y: x + y, indexProducers))
