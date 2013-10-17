#ifndef TopPTReweightProducer
#define TopPtReweightProducer

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

class TopPtReweight_Producer: public edm::EDProducer {
public:
	TopPtReweight_Producer(const edm::ParameterSet&);
	static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
	void produce (edm::Event&, const edm::EventSetup&);
	const edm::InputTag gen_event_input_;
	const edm::InputTag genParticles_;
	const std::string prefix_;
//	const int TopPtSystematic_;
};

#endif
