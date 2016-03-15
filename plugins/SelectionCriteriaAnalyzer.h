#ifndef BristolSelectionCriteriaAnalyzer
#define BristolSelectionCriteriaAnalyzer

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Utilities/interface/InputTag.h"


class SelectionCriteriaAnalyzer: public edm::EDFilter {
public:
	explicit SelectionCriteriaAnalyzer(const edm::ParameterSet&);
	virtual ~SelectionCriteriaAnalyzer();

	virtual void beginJob();
	virtual bool filter(edm::Event&, const edm::EventSetup&);
	virtual void endJob();
	virtual void beginRun(edm::Run &, const edm::EventSetup &);

	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
private:
	//config
	std::vector<edm::EDGetTokenT<bool> > offlineSelectionCriteriaInput_;
	std::vector<edm::EDGetTokenT<bool> > genSelectionCriteriaInput_;
};

#endif

