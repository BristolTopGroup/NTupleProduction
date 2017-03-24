#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_RecoMET.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"


BristolNTuple_RecoMET::BristolNTuple_RecoMET(const edm::ParameterSet& iConfig) :
    inputTag( consumes< reco::METCollection > (iConfig.getParameter<edm::InputTag>("InputTag"))),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix"))
{
    produces <double> ( prefix + "Ex" + suffix );
    produces <double> ( prefix + "Ey" + suffix );
    produces <double> ( prefix + "ET" + suffix );
    produces <double> ( prefix + "Phi" + suffix );

}

void BristolNTuple_RecoMET::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr <double> px(new double());
    std::auto_ptr <double> py(new double());
    std::auto_ptr <double> ET(new double());
    std::auto_ptr <double> Phi(new double());

    //-----------------------------------------------------------------
    if (!iEvent.isRealData()) {
        edm::Handle < reco::METCollection > mets;
        iEvent.getByToken(inputTag, mets);

        if (mets.isValid()) {
            const reco::MET MET(mets->at(0));
            *px  = MET.px();
            *py  = MET.py();
            *ET  = MET.pt();
            *Phi = MET.phi();
        }
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put( px, prefix + "Ex" + suffix );
    iEvent.put( py, prefix + "Ey" + suffix );
    iEvent.put( ET, prefix + "ET" + suffix );
    iEvent.put( Phi, prefix + "Phi" + suffix );
}
