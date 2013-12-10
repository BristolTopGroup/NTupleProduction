#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_METcorrections.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"
#include "DataFormats/METReco/interface/CorrMETData.h"

BristolNTuple_METcorrections::BristolNTuple_METcorrections(
		const edm::ParameterSet& iConfig) :
		inputTag(iConfig.getParameter < edm::InputTag > ("InputTag")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")) { //
//		cmsswVersion(iConfig.getParameter < edm::InputTag > ("CMSSWVersion")) {
	produces<double>(prefix + "x" + suffix);
	produces<double>(prefix + "y" + suffix);
	//      produces<double>(prefix + "sumet" + suffix);
}

void BristolNTuple_METcorrections::produce(edm::Event& iEvent,
		const edm::EventSetup& iSetup) {
	edm::Handle < CorrMETData > metCorr;
	iEvent.getByLabel(inputTag, metCorr);

	std::auto_ptr<double> corrx(new double(0));
	std::auto_ptr<double> corry(new double(0));

	if (metCorr.isValid()) {
		*corrx = metCorr->mex;
		*corry = metCorr->mey;

	} else {
		edm::LogError("BristolNTuple_METcorrectionsExtra")
				<< "Error! Can't get the product " << inputTag
				<< "Caution: MET Corrections of 0 will be saved in the event. If running on a 44X dataset, this should be fine.";
	}

	//    std::cout << "Systematic shift corrections, corrx = " << metCorr->mex << ", corry = " << metCorr->mey << std::endl;

//	std::auto_ptr<double> corrx(new double(metCorr->mex));
//	std::auto_ptr<double> corry(new double(metCorr->mey));
	//    std::auto_ptr<double> sumet(new double(metCorr->sumet));

	iEvent.put(corrx, prefix + "x" + suffix);
	iEvent.put(corry, prefix + "y" + suffix);
	//    iEvent.put(sumet, prefix + "sumet" + suffix);
}
