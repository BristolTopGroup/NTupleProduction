//
// Package:    TopDecayChannelFilter
// Class:      TopDecayChannelFilter
//
/**

 Description: Filter for specific decay modes of a top quark pair

 Implementation:
 Filter allows users to remove specific (run,event) top quark pair decays.
 Original Author:  Roger Wolf (rwolf@cern.ch)
 Modified:  Lukasz Kreczko, 24.09.2012
 */
#include "AnalysisDataFormats/TopObjects/interface/TtGenEvent.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

template<typename S>
class TopDecayChannelFilter: public edm::EDFilter {
public:
	TopDecayChannelFilter(const edm::ParameterSet&);
	~TopDecayChannelFilter();

private:
	virtual bool filter(edm::Event&, const edm::EventSetup&);

	edm::InputTag src_;
	S sel_;
	bool useTtGenEvent_;
	const bool taggingMode_;
};

template<typename S>
TopDecayChannelFilter<S>::TopDecayChannelFilter(const edm::ParameterSet& cfg) :
		src_(cfg.template getParameter < edm::InputTag > ("src")), //
		sel_(cfg), //
		useTtGenEvent_(cfg.getParameter<bool>("useTtGenEvent")), //
		taggingMode_(cfg.getParameter<bool>("taggingMode")) {
	 produces<bool>();
}

template<typename S>
TopDecayChannelFilter<S>::~TopDecayChannelFilter() {
}

template<typename S>
bool TopDecayChannelFilter<S>::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < reco::GenParticleCollection > genParticles;
	edm::Handle < TtGenEvent > ttbarGenEvent;
	bool filterDecision = true;

	if (useTtGenEvent_) {
		iEvent.getByLabel(src_, ttbarGenEvent);
		filterDecision = sel_(ttbarGenEvent->particles(), src_.label());
	} else {
		iEvent.getByLabel(src_, genParticles);
		filterDecision = sel_(*genParticles, src_.label());
	}

	iEvent.put(std::auto_ptr<bool>(new bool(filterDecision)));
	return taggingMode_ || filterDecision;
}

//template<typename S>
//void TopDecayChannelFilter<S>::fillDescriptions(edm::ConfigurationDescriptions & descriptions) {
//	edm::ParameterSetDescription desc;
//	desc.add < InputTag > ("src");
//	desc.add < bool > ("useTtGenEvent", false);
//	desc.add < bool > ("taggingMode", false);
//	descriptions.add("TopDecayChannelFilter", desc);
//}

