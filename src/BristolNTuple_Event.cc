#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Event.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

using namespace std;

BristolNTuple_Event::BristolNTuple_Event(const edm::ParameterSet& iConfig) :
		recoVertexInputTag_(iConfig.getParameter < edm::InputTag > ("recoVertexInputTag")), //
		metFiltersInputTag_(iConfig.getParameter < edm::InputTag > ("metFiltersInputTag")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")) {
	produces<unsigned int>(prefix + "Run" + suffix);
	produces<unsigned int>(prefix + "Number" + suffix);
	produces<unsigned int>(prefix + "Bunch" + suffix);
	produces<unsigned int>(prefix + "LumiSection" + suffix);
	produces<double>(prefix + "Time" + suffix);
	produces<bool>(prefix + "isData" + suffix);
	produces<std::vector<bool> >(prefix + "metFilters" + suffix);
	produces<unsigned int>(prefix + "NRecoVertices" + suffix);
}

void BristolNTuple_Event::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	double sec = iEvent.time().value() >> 32;
	double usec = 0xFFFFFFFF & iEvent.time().value();
	double conv = 1e6;

 	edm::Handle<reco::VertexCollection> primaryVertices;
 	iEvent.getByLabel(recoVertexInputTag_,primaryVertices);

	std::auto_ptr<unsigned int> run(new unsigned int(iEvent.id().run()));
	std::auto_ptr<unsigned int> eventNumber(new unsigned int(iEvent.id().event()));
	std::auto_ptr<unsigned int> ls(new unsigned int(iEvent.luminosityBlock()));
	std::auto_ptr<unsigned int> bunch(new unsigned int(iEvent.bunchCrossing()));
	std::auto_ptr<double> time(new double(sec + usec / conv));
	std::auto_ptr<bool> isdata(new bool(iEvent.isRealData()));
	std::auto_ptr<unsigned int> nv(new unsigned int(primaryVertices->size()));

	// MET Filters
	std::auto_ptr<std::vector<bool> > metFilters(new std::vector<bool>() );

	if ( iEvent.isRealData() ) {
		edm::Handle < edm::TriggerResults > metFiltersResults;
		iEvent.getByLabel(metFiltersInputTag_, metFiltersResults);

		const edm::TriggerNames &names = iEvent.triggerNames(*metFiltersResults);
		for ( unsigned int i = 0; i < metFiltersResults->size(); ++i) {
			metFilters->push_back( metFiltersResults->accept( i ) );
		}
	}


	//-----------------------------------------------------------------
	iEvent.put(run, prefix + "Run" + suffix);
	iEvent.put(eventNumber, prefix + "Number" + suffix);
	iEvent.put(ls, prefix + "LumiSection" + suffix);
	iEvent.put(bunch, prefix + "Bunch" + suffix);
	iEvent.put(time, prefix + "Time" + suffix);
	iEvent.put(isdata, prefix + "isData" + suffix);
	iEvent.put(nv, prefix + "NRecoVertices" + suffix);
	iEvent.put( metFilters, prefix + "metFilters" + suffix);
}