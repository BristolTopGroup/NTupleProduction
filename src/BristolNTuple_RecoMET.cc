#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_RecoMET.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


BristolNTuple_RecoMET::BristolNTuple_RecoMET(const edm::ParameterSet& iConfig) :
	inputTag(consumes< std::vector<reco::PFMET> > (iConfig.getParameter < edm::InputTag > ("InputTag"))), //
	prefix(iConfig.getParameter < std::string > ("Prefix")), //
	suffix(iConfig.getParameter < std::string > ("Suffix"))
{
	produces<double>(prefix + "Ex" + suffix);
	produces<double>(prefix + "Ey" + suffix);
	produces<double>(prefix + "ET" + suffix);
	produces<double>(prefix + "Phi" + suffix);
	produces<double>(prefix + "Significance" + suffix);
}

void BristolNTuple_RecoMET::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
    edm::Handle < std::vector<reco::PFMET> > recomets;
    iEvent.getByToken(inputTag, recomets);

    const reco::PFMET recoPFMET(recomets->at(0));

    std::auto_ptr<double> px(new double(recoPFMET.px()));
    std::auto_ptr<double> py(new double(recoPFMET.py()));
    std::auto_ptr<double> met(new double(recoPFMET.pt()));
    std::auto_ptr<double> phi(new double(recoPFMET.phi()));
    std::auto_ptr<double> significance(new double(recoPFMET.significance()));

	iEvent.put(px, prefix + "Ex" + suffix);
	iEvent.put(py, prefix + "Ey" + suffix);
	iEvent.put(met, prefix + "ET" + suffix);
	iEvent.put(phi, prefix + "Phi" + suffix);
	iEvent.put(significance, prefix + "Significance" + suffix);
}
