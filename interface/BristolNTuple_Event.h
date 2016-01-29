#ifndef BristolNTupleEvent
#define BristolNTupleEvent

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Vertexing.h"
#include <string>

class BristolNTuple_Event: public edm::EDProducer {
public:
	explicit BristolNTuple_Event(const edm::ParameterSet&);

private:
	void produce(edm::Event &, const edm::EventSetup &);
  	const edm::EDGetTokenT<std::vector<reco::Vertex>> recoVertexInputTag_;
	// edm::InputTag metFiltersInputTag_;
	// std::vector<std::string> metFiltersOfInterest_;

	const std::string prefix, suffix;

};

#endif
