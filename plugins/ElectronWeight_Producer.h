#ifndef ElectronWeightProducer
#define ElectronWeightProducer

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include <boost/scoped_ptr.hpp>
#include <boost/shared_ptr.hpp>
#include <TH1F.h>
#include <TH2F.h>
#include <TEfficiency.h>

class ElectronWeight_Producer: public edm::EDProducer {
public:
	ElectronWeight_Producer(const edm::ParameterSet&);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

private:
	void produce(edm::Event &, const edm::EventSetup &);
	const edm::InputTag electronInput_;
	const edm::InputTag jetInput_;
	const std::string prefix_, MCSampleTag_;
	const int Systematic_;

	edm::FileInPath electronIDScaleFactorsFile_;
	edm::FileInPath electronTriggerEfficiencyFile_;
	edm::FileInPath hadronLegEfficiencyFileName_;

	boost::shared_ptr<TH1F> hadronLegEfficiencyHistogram_;
	boost::shared_ptr<TEfficiency> hadronLegEfficiencyHistogram_1_;
	boost::shared_ptr<TEfficiency> hadronLegEfficiencyHistogram_2_;
	boost::shared_ptr<TEfficiency> hadronLegEfficiencyHistogram_3_;
	boost::shared_ptr<TH2F> electronIdIsoScaleFactorsHistogram_;
	boost::shared_ptr<TEfficiency> electronTriggerEfficiencyHistogram_;

};

#endif

