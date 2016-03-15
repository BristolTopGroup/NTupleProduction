#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenMET.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"



BristolNTuple_GenMET::BristolNTuple_GenMET(const edm::ParameterSet& iConfig) :
    inputTag(consumes< std::vector<pat::MET> > (iConfig.getParameter<edm::InputTag>("InputTag"))),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix"))
{
    produces <double> ( prefix + "Ex" + suffix );
    produces <double> ( prefix + "Ey" + suffix );
    produces <double> ( prefix + "ET" + suffix );
    produces <double> ( prefix + "Phi" + suffix );

}

void BristolNTuple_GenMET::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr <double> px(new double());
    std::auto_ptr <double> py(new double());
    std::auto_ptr <double> ET(new double());
    std::auto_ptr <double> Phi(new double());

    //-----------------------------------------------------------------
    if (!iEvent.isRealData()) {

        edm::Handle < std::vector<pat::MET> > mets;
        iEvent.getByToken(inputTag, mets);
        const pat::MET patMET(mets->at(0));
        const reco::GenMET* genMET(patMET.genMET());

        *px = genMET->px();
        *py = genMET->py();
        *ET = genMET->pt();
        *Phi = genMET->phi();
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put( px, prefix + "Ex" + suffix );
    iEvent.put( py, prefix + "Ey" + suffix );
    iEvent.put( ET, prefix + "ET" + suffix );
    iEvent.put( Phi, prefix + "Phi" + suffix );
}
