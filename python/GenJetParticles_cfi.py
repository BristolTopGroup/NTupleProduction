import FWCore.ParameterSet.Config as cms

#
# $Id: GenJetParticles_cfi.py,v 1.2 2013/03/15 14:41:39 nbartosi Exp $
#
# ShR 27 Mar 07: move modules producing candidates for Jets from RecoGenJets.cff
# 
#
genParticlesForJetsPlusHadron = cms.EDProducer("myInputGenJetsParticleSelector",
    src = cms.InputTag("genParticles"),
    ignoreParticleIDs = cms.vuint32(
         1000022,
         1000012, 1000014, 1000016,
         2000012, 2000014, 2000016,
         1000039, 5100039,
         4000012, 4000014, 4000016,
         9900012, 9900014, 9900016,
         39),
    partonicFinalState = cms.bool(False),
    excludeResonances = cms.bool(True),
    excludeFromResonancePids = cms.vuint32(12, 13, 14, 16),
    tausAsJets = cms.bool(False),
    flavour = cms.int32(5)
)

hiGenParticlesForJetsPlusHadron = genParticlesForJetsPlusHadron.clone()
hiGenParticlesForJetsPlusHadron.src = cms.InputTag("hiGenParticles")

genParticlesForJetsNoNuPlusHadron = genParticlesForJetsPlusHadron.clone()
genParticlesForJetsNoNuPlusHadron.ignoreParticleIDs += cms.vuint32( 12,14,16)

genParticlesForJetsNoMuNoNuPlusHadron = genParticlesForJetsPlusHadron.clone()
genParticlesForJetsNoMuNoNuPlusHadron.ignoreParticleIDs += cms.vuint32( 12,13,14,16)

