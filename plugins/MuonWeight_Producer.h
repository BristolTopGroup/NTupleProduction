#ifndef MuonWeightProducer
#define MuonWeightProducer

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"

#include <boost/scoped_ptr.hpp>
#include <boost/shared_ptr.hpp>
#include <TH2F.h>
#include <TH3F.h>

class MuonWeight_Producer: public edm::EDProducer {
public:
	MuonWeight_Producer(const edm::ParameterSet&);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

private:
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag muonInput_;
	const std::string prefix_, MCSampleTag_;
	const int Systematic_;

	edm::FileInPath muonScaleFactorsFile_;
	boost::shared_ptr<TH2F> muonIdIsoScaleFactorsHistogram_;
	boost::shared_ptr<TH3F> muonTriggerScaleFactorsHistogram_;

};

#endif

