#ifndef BristolNTupleEvent
#define BristolNTupleEvent

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Vertexing.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include <string>

class BristolNTuple_Event: public edm::EDProducer {
public:
	explicit BristolNTuple_Event(const edm::ParameterSet&);

private:
	void produce(edm::Event &, const edm::EventSetup &);
  	const edm::EDGetTokenT<std::vector<reco::Vertex>> recoVertexInputTag_;
	const edm::EDGetTokenT<edm::TriggerResults> metFiltersToken_;
	std::vector<std::string> metFiltersOfInterest_;
	const edm::EDGetTokenT<bool> badChCandFilterToken_;
    const edm::EDGetTokenT<bool> badPFMuonFilterToken_;

	const bool is2016Regime_;
	const std::string prefix, suffix;

};

#endif
