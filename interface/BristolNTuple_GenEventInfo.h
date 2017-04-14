#ifndef BristolNTupleGenEventInfo
#define BristolNTupleGenEventInfo

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include <boost/array.hpp>

#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "TopQuarkAnalysis/TopTools/interface/JetPartonMatching.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/LHERunInfoProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/LHEEventProduct.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"

namespace TTbarDecay {
enum value {
	NotTtbar,
	FullHadronic,
	SemiLeptonicElectron,
	SemiLeptonicMuon,
	SemiLeptonicTau,
	FullLeptonicEE,
	FullLeptonicMuMu,
	FullLeptonicTauTau,
	FullLeptonicETau,
	FullLeptonicEMu,
	FullLeptonicMuTau,
	NumberOfDecayModes
};
}

namespace ZDecay {
enum value {
  NoZFound,
  ZToEE,
  ZToMuMu,
  ZToTauTau,
  ZTo2NuE,
  ZTo2NuMu,
  ZTo2NuTau,
  NotInterestingZDecay,
  NumberOfDecayModes
};
}

class BristolNTuple_GenEventInfo: public edm::EDProducer {

public:
	explicit BristolNTuple_GenEventInfo(const edm::ParameterSet&);
private:
	virtual void beginRun(edm::Run const& /* iR */, edm::EventSetup const& /* iE */);

private:
	void initLumiWeights();
	void produce(edm::Event &, const edm::EventSetup &);
  	const edm::EDGetTokenT<GenEventInfoProduct > genEvtInfoInputTag;
  	const edm::EDGetTokenT<LHEEventProduct> lheEventProductToken_;
	const edm::EDGetTokenT<reco::GenJetCollection > genJetsInputTag_;
	std::vector<edm::EDGetTokenT<bool> > ttbarDecayFlags_;
	const edm::InputTag puWeightsInputTag_;
	const bool storePDFWeights_, isTTbarMC_;
	const edm::InputTag pdfWeightsInputTag_;
	const edm::EDGetTokenT<std::vector<PileupSummaryInfo> > pileupInfoSrc_;
	const edm::EDGetTokenT<TtGenEvent >  tt_gen_event_input_;
	const double minGenJetPt_, maxGenJetAbsoluteEta_;
	const std::string prefix_, suffix_;
	edm::EDGetTokenT<edm::View<reco::GenParticle> > prunedGenToken_;
	edm::EDGetTokenT<edm::View<pat::PackedGenParticle> > packedGenToken_;

  bool isAncestor(const reco::Candidate * ancestor, const reco::Candidate * particle) const;
  std::vector<const pat::PackedGenParticle*> getZDecayParticles(const reco::Candidate* zBoson,
      const edm::Handle<edm::View<pat::PackedGenParticle> >& packed) const;
  ZDecay::value getZDecay(const std::vector<const pat::PackedGenParticle*>& decayParticles) const;
  void addTTZContent(edm::Event &, const edm::EventSetup &);
};

#endif

