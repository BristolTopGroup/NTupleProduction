#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_Event.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "DataFormats/METReco/interface/BeamHaloSummary.h"
#include "DataFormats/PatCandidates/interface/MET.h"

BristolNTuple_Event::BristolNTuple_Event(const edm::ParameterSet& iConfig) :
		dcsInputTag(iConfig.getParameter < edm::InputTag > ("DCSInputTag")), //
		hcalLaserFilterInput_(iConfig.getParameter < edm::InputTag > ("HCALLaserFilterInput")), //
		ecalDeadCellFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellFilterInput")), //
		ecalDeadCellTriggerPrimitiveFilterInput_(iConfig.getParameter < edm::InputTag > ("ECALDeadCellTriggerPrimitiveFilterInput")), //
		trackingFailureFilter_(iConfig.getParameter < edm::InputTag > ("TrackingFailureFilterInput")), //
		METInputForSumET_(iConfig.getParameter < edm::InputTag > ("METInputForSumET")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")) {
	produces<double>(prefix + "MagneticField" + suffix);
	produces<unsigned int>(prefix + "Run" + suffix);
	produces<unsigned int>(prefix + "Number" + suffix);
	produces<unsigned int>(prefix + "Bunch" + suffix);
	produces<unsigned int>(prefix + "LumiSection" + suffix);
	produces<unsigned int>(prefix + "Orbit" + suffix);
	produces<double>(prefix + "Time" + suffix);
	produces<bool>(prefix + "isData" + suffix);
	produces<double>(prefix + "rho" + suffix);
	produces<double>(prefix + "SumET" + suffix);

	//optinal MET filter decisions
	produces<bool>(prefix + "HCALLaserFilter" + suffix);
	produces<bool>(prefix + "ECALDeadCellFilter" + suffix);
	produces<bool>(prefix + "ECALDeadCellTriggerPrimitiveFilter" + suffix);
	produces<bool>(prefix + "TrackingFailureFilter" + suffix);
	produces<bool>(prefix + "CSCTightHaloId" + suffix);
}

void BristolNTuple_Event::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	edm::Handle < DcsStatusCollection > dcsHandle;
	iEvent.getByLabel(dcsInputTag, dcsHandle);
	double evt_bField = 3.8;
	// need the magnetic field
	//
	// if isRealData then derive bfield using the
	// magnet current from DcsStatus
	// otherwise take it from the IdealMagneticFieldRecord
	if (iEvent.isRealData()) {
		if (dcsHandle.isValid()) {
			edm::LogInfo("BristolNTuple_ElectronsInfo") << "Successfully obtained " << dcsInputTag;
			// scale factor = 3.801/18166.0 which are
			// average values taken over a stable two-week period
			double currentToBFieldScaleFactor = 2.09237036221512717e-04;
			double current = (*dcsHandle)[0].magnetCurrent();
			evt_bField = current * currentToBFieldScaleFactor;
		} else {
			edm::LogError("BristolNTuple_Event") << "Error! Can't get the product " << dcsInputTag;
		}
	} else {
		edm::ESHandle < MagneticField > magneticField;
		iSetup.get<IdealMagneticFieldRecord>().get(magneticField);

		if (magneticField.isValid()) {
			edm::LogInfo("BristolNTuple_EventInfo") << "Successfully obtained IdealMagneticFieldRecord";

			evt_bField = magneticField->inTesla(GlobalPoint(0., 0., 0.)).z();
		} else {
			edm::LogError("BristolNTuple_EventError") << "Error! Can't get IdealMagneticFieldRecord";
		}
	}
	std::auto_ptr<double> magField(new double(evt_bField));

	double sec = iEvent.time().value() >> 32;
	double usec = 0xFFFFFFFF & iEvent.time().value();
	double conv = 1e6;

	edm::Handle<double> rhoH;
	iEvent.getByLabel(edm::InputTag("kt6PFJets", "rho"), rhoH);

	edm::Handle < std::vector<pat::MET> > mets;
	iEvent.getByLabel(METInputForSumET_, mets);

	std::auto_ptr<unsigned int> run(new unsigned int(iEvent.id().run()));
	std::auto_ptr<unsigned int> eventNumber(new unsigned int(iEvent.id().event()));
	std::auto_ptr<unsigned int> ls(new unsigned int(iEvent.luminosityBlock()));
	std::auto_ptr<unsigned int> bunch(new unsigned int(iEvent.bunchCrossing()));
	std::auto_ptr<unsigned int> orbit(new unsigned int(iEvent.orbitNumber()));
	std::auto_ptr<double> time(new double(sec + usec / conv));
	std::auto_ptr<bool> isdata(new bool(iEvent.isRealData()));
	std::auto_ptr<double> rho(new double(*rhoH.product()));
	std::auto_ptr<double> SumET(new double(mets->at(0).sumEt()));

	std::auto_ptr<bool> HCALLaserFilter(new bool(passesFilter(iEvent, hcalLaserFilterInput_)));
	std::auto_ptr<bool> ECALDeadCellFilter(new bool(passesFilter(iEvent, ecalDeadCellFilterInput_)));
	std::auto_ptr<bool> ECALDeadCellTriggerPrimitiveFilter(new bool(passesFilter(iEvent, ecalDeadCellTriggerPrimitiveFilterInput_)));
	std::auto_ptr<bool> TrackingFailureFilter(new bool(passesFilter(iEvent, trackingFailureFilter_)));

	bool cscTightID(false);
	edm::Handle < reco::BeamHaloSummary > TheBeamHaloSummary;
	iEvent.getByLabel("BeamHaloSummary", TheBeamHaloSummary);
	if (TheBeamHaloSummary.isValid()) {
		edm::LogInfo("EventFilter") << "Successfully obtained BeamHaloSummary";
		const reco::BeamHaloSummary TheSummary = (*TheBeamHaloSummary.product());
		cscTightID = TheSummary.CSCTightHaloId();
	} else
		edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product BeamHaloSummary";

	std::auto_ptr<bool> CSCTightHaloId(new bool(cscTightID));

	//-----------------------------------------------------------------
	iEvent.put(magField, prefix + "MagneticField" + suffix);
	iEvent.put(run, prefix + "Run" + suffix);
	iEvent.put(eventNumber, prefix + "Number" + suffix);
	iEvent.put(ls, prefix + "LumiSection" + suffix);
	iEvent.put(bunch, prefix + "Bunch" + suffix);
	iEvent.put(orbit, prefix + "Orbit" + suffix);
	iEvent.put(time, prefix + "Time" + suffix);
	iEvent.put(isdata, prefix + "isData" + suffix);
	iEvent.put(rho, prefix + "rho" + suffix);
	iEvent.put(SumET, prefix + "SumET" + suffix);

	iEvent.put(HCALLaserFilter, prefix + "HCALLaserFilter" + suffix);
	iEvent.put(ECALDeadCellFilter, prefix + "ECALDeadCellFilter" + suffix);
	iEvent.put(ECALDeadCellTriggerPrimitiveFilter, prefix + "ECALDeadCellTriggerPrimitiveFilter" + suffix);
	iEvent.put(TrackingFailureFilter, prefix + "TrackingFailureFilter" + suffix);
	iEvent.put(CSCTightHaloId, prefix + "CSCTightHaloId" + suffix);
}

bool BristolNTuple_Event::passesFilter(edm::Event& event, edm::InputTag filter) {
	bool result(false);
	edm::Handle<bool> filterResult;
	event.getByLabel(filter, filterResult);
	if (filterResult.isValid()) {
		edm::LogInfo("EventFilter") << "Successfully obtained " << filter;
		result = *filterResult;
	} else
		edm::LogError("BristolNTuple_EventSelectionError") << "Error! Can't get the product " << filter;

	return result;
}
