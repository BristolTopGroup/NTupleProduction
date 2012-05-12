#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_MET.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/MET.h"

BristolNTuple_MET::BristolNTuple_MET(const edm::ParameterSet& iConfig) :
		inputTag(iConfig.getParameter < edm::InputTag > ("InputTag")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")) {
	produces<double>(prefix + "Ex" + suffix);
	produces<double>(prefix + "Ey" + suffix);
	produces<double>(prefix + "ET" + suffix);
	produces<double>(prefix + "Phi" + suffix);
	produces<double>(prefix + "Significance" + suffix);
}

void BristolNTuple_MET::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < std::vector<pat::MET> > mets;
	iEvent.getByLabel(inputTag, mets);

	if (!mets.isValid())
		edm::LogError("BristolNTuple_METExtraError") << "Error! Can't get the product " << inputTag;

	const pat::MET patMET(mets->at(0));

	std::auto_ptr<double> px(new double(patMET.px()));
	std::auto_ptr<double> py(new double(patMET.py()));
	std::auto_ptr<double> met(new double(patMET.pt()));
	std::auto_ptr<double> phi(new double(patMET.phi()));
	std::auto_ptr<double> significance(new double(patMET.significance()));

	iEvent.put(px, prefix + "Ex" + suffix);
	iEvent.put(py, prefix + "Ey" + suffix);
	iEvent.put(met, prefix + "ET" + suffix);
	iEvent.put(phi, prefix + "Phi" + suffix);
	iEvent.put(significance, prefix + "Significance" + suffix);
}
