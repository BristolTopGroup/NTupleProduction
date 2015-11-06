#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Trigger.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

using namespace std;

// Modifications to run on miniAOD based on
// https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD#Trigger

BristolNTuple_Trigger::BristolNTuple_Trigger(const edm::ParameterSet& iConfig) :
		hltInputTag_(iConfig.getParameter < edm::InputTag > ("HLTInputTag")), //
		hltObjectsInputTag_(iConfig.getParameter < edm::InputTag > ("HLTObjectsInputTag")), //
		pathOfInterest_(iConfig.getParameter <std::string> ("PathOfInterest")), //
		tightenTrigger_(iConfig.getParameter<bool>("tightenTrigger")),
	    triggerFilterName_(iConfig.getParameter<std::string>("hltFilter")),
	    minNumber_(iConfig.getParameter<unsigned>("minNumber")),
	    triggerObjectSelector_(iConfig.getParameter<std::string>("cut")),
		prefix_(iConfig.getParameter <std::string> ("Prefix")), //
		suffix_(iConfig.getParameter < std::string > ("Suffix")) {

	produces < bool > (prefix_ + "Fired" + suffix_ );
	// produces < unsigned short > (prefix_ + "Version" + suffix_ );
	// produces < unsigned short > (prefix_ + "Prescale" + suffix_ );

    produces <std::vector<double> > ( prefix_ + "toEnergy" + suffix_ );
	produces <std::vector<float> > ( prefix_ + "toPt" + suffix_ );
	produces <std::vector<float> > ( prefix_ + "toEta" + suffix_ );
	produces <std::vector<float> > ( prefix_ + "toPhi" + suffix_ );
}

void BristolNTuple_Trigger::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {
}

void BristolNTuple_Trigger::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr < bool > fired(new bool(false));
	// std::auto_ptr < unsigned short > version(new unsigned short);
	// std::auto_ptr < unsigned short > prescale(new unsigned short);
	std::auto_ptr <std::vector<double>  > toEnergy(new std::vector<double>());
	std::auto_ptr <std::vector<float>  > toPt(new std::vector<float>());
	std::auto_ptr <std::vector<float>  > toEta(new std::vector<float>());
	std::auto_ptr <std::vector<float>  > toPhi(new std::vector<float>());

	edm::Handle < edm::TriggerResults > triggerResults;
	iEvent.getByLabel(hltInputTag_, triggerResults);

    const edm::TriggerNames &names = iEvent.triggerNames(*triggerResults);
	unsigned int triggerIndex = 9999;
	std::string triggerName="Trigger";
    for (unsigned int i = 0, n = triggerResults->size(); i < n; ++i) {
    	// std::cout << "Trigger " << i << " : " << names.triggerName(i) << std::endl;
    	if ( names.triggerName(i).find(pathOfInterest_) != std::string::npos ) {
    		triggerIndex = i;
    		triggerName = names.triggerName(i);
    	}
	}

	if ( triggerIndex < triggerResults->size() ) {
		*fired = triggerResults->accept(triggerIndex);
	}
	else {
		std::cout << "Looking for : " << pathOfInterest_ << " but failed" << std::endl;
	}

    edm::Handle<pat::TriggerObjectStandAloneCollection> triggerObjects;
	iEvent.getByLabel(hltObjectsInputTag_, triggerObjects);

	unsigned int nPass = 0;
    for (pat::TriggerObjectStandAlone obj : *triggerObjects) {
        
        if ( tightenTrigger_ ) {
			// Consider only those objects that pass the requested filter
			if (obj.hasFilterLabel(triggerFilterName_)) {
				if (triggerObjectSelector_(obj)) {
					++nPass;
				}
			}
        }

        obj.unpackPathNames(names);

        std::vector<std::string> pathNamesAll  = obj.pathNames(true);
        std::vector<std::string> pathNamesLast  = obj.pathNames(false);

        for ( unsigned int trigPath = 0 ; trigPath < pathNamesLast.size(); trigPath++ ) {
        	// Check if this object is associated to this path and that it is associated to the last filter in that path
        	if ( pathNamesLast[trigPath] == triggerName && obj.hasPathName( triggerName, true, true ) ) {
        		toEnergy->push_back( obj.energy() );
        		toPt->push_back( obj.pt() );
        		toEta->push_back( obj.eta() );
        		toPhi->push_back( obj.phi() );
    		}
        }
    }

    if ( tightenTrigger_ && nPass < minNumber_ ) {
    	*fired = false;
    }

	//-----------------------------------------------------------------
	// put vectors in the event

	iEvent.put(fired, prefix_ + "Fired" + suffix_);
	// iEvent.put(version, prefix_ + "Version" + suffix_ );
	// iEvent.put(prescale, prefix_ + "Prescale" + suffix_ );
	iEvent.put(toEnergy,prefix_ + "toEnergy" + suffix_);
	iEvent.put(toPt,prefix_ + "toPt" + suffix_);
	iEvent.put(toEta,prefix_ + "toEta" + suffix_);
	iEvent.put(toPhi,prefix_ + "toPhi" + suffix_);
}
