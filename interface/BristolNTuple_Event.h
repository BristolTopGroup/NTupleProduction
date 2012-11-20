#ifndef BristolNTupleEvent
#define BristolNTupleEvent

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

class BristolNTuple_Event: public edm::EDProducer {
public:
	explicit BristolNTuple_Event(const edm::ParameterSet&);

private:
	bool passesFilter(edm::Event& event, edm::InputTag filter);
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag dcsInputTag;
	edm::InputTag hcalLaserFilterInput_, ecalDeadCellFilterInput_, ecalDeadCellTriggerPrimitiveFilterInput_, trackingFailureFilter_, METInputForSumET_;

	const std::string prefix, suffix;

};

#endif
