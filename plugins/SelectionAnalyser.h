#ifndef SELECTIONANALYSER
#define SELECTIONANALYSER

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "TH1F.h"
#include "TH2F.h"

class SelectionAnalyser : public edm::EDAnalyzer {
public:
	SelectionAnalyser(const edm::ParameterSet& iConfig);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void beginJob();
	virtual void endJob();

private:
	//non-global event weights (global = i.e. lumi-weight)
	// edm::InputTag PUWeightInput_;//, ZeroBtagWeightInput_, OneBtagWeightInput_, TwoBtagWeightInput_;
	std::vector<edm::InputTag> selectionFlags_;
	std::vector<std::string> selectionNames_;
	unsigned int numberOfCuts_;
	//distributions
	// TH1F* consecutiveCuts_, *individualCuts_;
	TH1F* consecutiveCuts_unweighted_, *individualCuts_unweighted_;

};
#endif
