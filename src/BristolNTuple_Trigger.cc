#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Trigger.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"

unsigned int NmaxL1AlgoBit = 128;
unsigned int NmaxL1TechBit = 64;

BristolNTuple_Trigger::BristolNTuple_Trigger(const edm::ParameterSet& iConfig) :
    l1InputTag(iConfig.getParameter<edm::InputTag> ("L1InputTag")),
    hltInputTag(iConfig.getParameter<edm::InputTag> ("HLTInputTag")),
    hltPathsOfInterest(iConfig.getParameter<std::vector<std::string> > ("HLTPathsOfInterest_Signal")),
    hltPathsOfInterest_other(iConfig.getParameter<std::vector<std::string> > ("HLTPathsOfInterest_Other")),
    prefix(iConfig.getParameter<std::string> ("Prefix")),
    suffix(iConfig.getParameter<std::string> ("Suffix")) {

    produces<std::vector<int> > (prefix + "L1PhysBits" + suffix);
    produces<std::vector<int> > (prefix + "L1TechBits" + suffix);
    produces<std::vector<int> > (prefix + "HLTBits" + suffix);
    produces<std::vector<int> > (prefix + "HLTResults" + suffix);
    produces<std::vector<int> > (prefix + "HLTPrescales" + suffix);
    produces<std::vector<int> > (prefix + "HLTResultsOther" + suffix);
    produces<std::vector<int> > (prefix + "HLTPrescalesOther" + suffix);
}

void BristolNTuple_Trigger::beginRun(edm::Run& iRun, const edm::EventSetup& iSetup) {

    bool changed = true;
    if (hltConfig.init(iRun, iSetup, hltInputTag.process(), changed)) {
        // if init returns TRUE, initialisation has succeeded!
        edm::LogInfo("BristolNTuple_TriggerInfo") << "HLT config with process name " << hltInputTag.process()
                << " successfully extracted";
    } else {
        // if init returns FALSE, initialisation has NOT succeeded, which indicates a problem
        // with the file and/or code and needs to be investigated!
        edm::LogError("BristolNTuple_TriggerError") << "Error! HLT config extraction with process name "
                << hltInputTag.process() << " failed";
        // In this case, all access methods will return empty values!
    }
}

void BristolNTuple_Trigger::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<int> > l1physbits(new std::vector<int>());
    std::auto_ptr < std::vector<int> > l1techbits(new std::vector<int>());
    std::auto_ptr < std::vector<int> > hltbits(new std::vector<int>());
    std::auto_ptr < std::vector<int> > hltresults(new std::vector<int>());
    std::auto_ptr < std::vector<int> > hltprescales(new std::vector<int>());
    std::auto_ptr < std::vector<int> > hltresults_other(new std::vector<int>());
    std::auto_ptr < std::vector<int> > hltprescales_other(new std::vector<int>());

    //-----------------------------------------------------------------
    edm::Handle < L1GlobalTriggerReadoutRecord > l1GtReadoutRecord;
    iEvent.getByLabel(l1InputTag, l1GtReadoutRecord);

    if (l1GtReadoutRecord.isValid()) {
        edm::LogInfo("BristolNTuple_TriggerInfo") << "Successfully obtained " << l1InputTag;

        for (unsigned int i = 0; i < NmaxL1AlgoBit; ++i) {
            l1physbits->push_back(l1GtReadoutRecord->decisionWord()[i] ? 1 : 0);
        }
        for (unsigned int i = 0; i < NmaxL1TechBit; ++i) {
            l1techbits->push_back(l1GtReadoutRecord->technicalTriggerWord()[i] ? 1 : 0);
        }
    } else {
        edm::LogError("BristolNTuple_TriggerError") << "Error! Can't get the product " << l1InputTag;
    }

    edm::Handle < edm::TriggerResults > triggerResults;
    iEvent.getByLabel(hltInputTag, triggerResults);

    if (triggerResults.isValid()) {
        edm::LogInfo("BristolNTuple_TriggerInfo") << "Successfully obtained " << hltInputTag;

        for (unsigned int i = 0; i < triggerResults->size(); i++) {
            hltbits->push_back(triggerResults->at(i).accept() ? 1 : 0);
        }

        for (std::vector<std::string>::const_iterator it = hltPathsOfInterest.begin(); it != hltPathsOfInterest.end(); ++it) {
            int fired = 0;
            unsigned int index = hltConfig.triggerIndex(*it);
            if (index < triggerResults->size()) {
                if (triggerResults->accept(index))
                    fired = 1;
            } else {
                edm::LogInfo("BristolNTuple_TriggerInfo") << "Requested HLT path \"" << (*it) << "\" does not exist";
            }
            hltresults->push_back(fired);

            int prescale = -1;
            if (hltConfig.prescaleSet(iEvent, iSetup) < 0) {
                edm::LogError("BristolNTuple_TriggerError")
                        << "Error! The prescale set index number could not be obtained";
            } else {
                prescale = hltConfig.prescaleValue(iEvent, iSetup, *it);
            }
            hltprescales->push_back(prescale);
        }

        for (std::vector<std::string>::const_iterator it = hltPathsOfInterest_other.begin(); it != hltPathsOfInterest_other.end(); ++it) {
            int fired = 0;
            unsigned int index = hltConfig.triggerIndex(*it);
            if (index < triggerResults->size()) {
                if (triggerResults->accept(index))
                    fired = 1;
            } else {
                edm::LogInfo("BristolNTuple_TriggerInfo") << "Requested HLT path \"" << (*it) << "\" does not exist";
            }
            hltresults_other->push_back(fired);

            int prescale = -1;
            if (hltConfig.prescaleSet(iEvent, iSetup) < 0) {
                edm::LogError("BristolNTuple_TriggerError")
                        << "Error! The prescale set index number could not be obtained";
            } else {
                prescale = hltConfig.prescaleValue(iEvent, iSetup, *it);
            }
            hltprescales_other->push_back(prescale);
        }
    } else {
        edm::LogError("BristolNTuple_TriggerError") << "Error! Can't get the product " << hltInputTag;
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put(l1physbits, prefix + "L1PhysBits" + suffix);
    iEvent.put(l1techbits, prefix + "L1TechBits" + suffix);
    iEvent.put(hltbits, prefix + "HLTBits" + suffix);
    iEvent.put(hltresults, prefix + "HLTResults" + suffix);
    iEvent.put(hltprescales, prefix + "HLTPrescales" + suffix);
    iEvent.put(hltresults_other, prefix + "HLTResultsOther" + suffix);
    iEvent.put(hltprescales_other, prefix + "HLTPrescalesOther" + suffix);
}
