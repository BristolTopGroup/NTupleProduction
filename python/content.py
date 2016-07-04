import FWCore.ParameterSet.Config as cms

particle = cms.EDProducer(
    "CandViewNtpProducer",
    src=cms.InputTag("skimmedPatMuons"),
    lazyParser=cms.untracked.bool(True),
    prefix=cms.untracked.string("basic"),
    eventInfo=cms.untracked.bool(False),
    variables=cms.VPSet(
        cms.PSet(
            tag=cms.untracked.string("Mass"),
            quantity=cms.untracked.string("mass")
        ),
        cms.PSet(
            tag=cms.untracked.string("Pt"),
            quantity=cms.untracked.string("pt")
        ),
        cms.PSet(
            tag=cms.untracked.string("Eta"),
            quantity=cms.untracked.string("eta")
        ),
        cms.PSet(
            tag=cms.untracked.string("Y"),
            quantity=cms.untracked.string("rapidity")
        ),
        cms.PSet(
            tag=cms.untracked.string("Phi"),
            quantity=cms.untracked.string("phi")
        ),
        cms.PSet(
            tag=cms.untracked.string("E"),
            quantity=cms.untracked.string("energy")
        ),
        cms.PSet(
            tag=cms.untracked.string("Charge"),
            quantity=cms.untracked.string("charge")
        ),
    )
)

###electrons
electronVars = (
   cms.PSet(
      tag = cms.untracked.string("isLoose"),
      quantity = cms.untracked.string("userInt('isLoose')")
),
                )

electrons  = particle.clone()
electrons.variables += electronVars
electrons.prefix = cms.untracked.string("el")
electrons.src = cms.InputTag("electronUserData")