#ifndef BTagWeightProducer
#define BTagWeightProducer

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

class BTagWeight_Producer: public edm::EDProducer {
public:
	BTagWeight_Producer(const edm::ParameterSet&);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

private:
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::EDGetTokenT<unsigned int> numberOfTagsInput_;
	const edm::EDGetTokenT< pat::JetCollection > jetInput_;
	const std::string prefix_, MCSampleTag_;
	const unsigned int targetBtagMultiplicity_;//0 means >= 0, 1: >=1 etc
	const int BTagSystematic_;

};

#endif

