#ifndef UNFOLDINGANALYSER
#define UNFOLDINGANALYSER

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TH1F.h"
#include "TH2F.h"

class UnfoldingAnalyser: public edm::EDAnalyzer {
public:
	UnfoldingAnalyser(const edm::ParameterSet& iConfig);
	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

	virtual void analyze(const edm::Event&, const edm::EventSetup&);
	virtual void beginJob();
	virtual void endJob();

private:
	//non-global event weights (global = i.e. lumi-weight)
	edm::InputTag PUWeightInput_, BtagWeightInput_;
	//distributions
	edm::InputTag genMetInput_, recoMetInput_;
	edm::InputTag selectionFlagInput_;
	edm::InputTag isFullyHadronicTtbarFlag_, isDiLeptonicTtbarFlag_;
	edm::InputTag isSemiLeptonicTauFlag_, isSemiLeptonicElectronFlag_, isSemiLeptonicMuonFlag_;
	bool doElectronChannel_; //if false do muon channel
	//in order to be able to create a RooResponse object one needs
	//Does not pass selection
	// - fill truth distribution (1D)
	//passes selection:
	// - fill truth (1D)
	// - fill measured (1D)
	// - fill response (2D): x= measured, y = truth
	//Fake - not really applicable for us and optional for the object creation
	// - fill measured (1D)
	// - fill fake (1D)
	//histograms with 1 GeV binning
	TH1F* truth_, *measured_, *fake_, *contamination_inGenMET_, *contamination_inRecoMET_;
	TH2F* response_, *response_withoutFakes_;
	//histograms with analysis binning: [0,25,45,70,100, inf]
	TH1F* truth_AsymBins_, *measured_AsymBins_, *fake_AsymBins_, *contamination_AsymBins_inGenMET_,
			*contamination_AsymBins_inRecoMET_;
	TH2F* response_AsymBins_, *response_withoutFakes_AsymBins_;

};
#endif

