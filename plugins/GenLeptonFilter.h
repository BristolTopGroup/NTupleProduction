#ifndef BristolGenLeptonFilter
#define BristolGenLeptonFilter

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/JetReco/interface/GenJetCollection.h"

#include <boost/array.hpp>
#include <string>
#include <vector>

class GenLeptonFilter: public edm::EDFilter {
public:
	explicit GenLeptonFilter(const edm::ParameterSet&);
	virtual ~GenLeptonFilter();

	virtual void beginJob();
	virtual bool filter(edm::Event&, const edm::EventSetup&);
	virtual void endJob();
	virtual void beginRun();

	static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);

private:
	//config
	edm::EDGetTokenT< reco::GenJetCollection > particleLevelLeptonSelectionInput_;
	std::string prefix_;
    double minPt_;
    double maxAbsoluteEta_;
};

#endif

