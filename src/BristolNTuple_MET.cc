#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_MET.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include <iostream>

using namespace std;
BristolNTuple_MET::BristolNTuple_MET(const edm::ParameterSet& iConfig) :
  		inputTag(consumes<std::vector<pat::MET>>(iConfig.getParameter<edm::InputTag>("InputTag"))),			
		storeMETUncertainties_(iConfig.getParameter<bool>("storeMETUncertainties")), //
		nMETUncertainties_(iConfig.getParameter<unsigned int>("nMETUncertainties")), //
		prefix(iConfig.getParameter < std::string > ("Prefix")), //
		suffix(iConfig.getParameter < std::string > ("Suffix")) {
	produces<double>(prefix + "Ex" + suffix);
	produces<double>(prefix + "Ey" + suffix);
	produces<double>(prefix + "ET" + suffix);
	produces<double>(prefix + "Phi" + suffix);
	produces<double>(prefix + "Significance" + suffix);
	produces< std::vector<unsigned int> >(prefix + "METUncertaintyTypes" + suffix );
	produces< std::vector<double> >(prefix + "METUncertaintiesPt" + suffix );
	produces< std::vector<double> >(prefix + "METUncertaintiesPx" + suffix );
	produces< std::vector<double> >(prefix + "METUncertaintiesPy" + suffix );
}

void BristolNTuple_MET::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
	edm::Handle < std::vector<pat::MET> > mets;
	iEvent.getByToken(inputTag, mets);

	// if (!mets.isValid())
	// 	edm::LogError("BristolNTuple_METExtraError") << "Error! Can't get the product " << inputTag;

	const pat::MET & patMET(mets->at(0));

	std::auto_ptr<double> px(new double(patMET.px()));
	std::auto_ptr<double> py(new double(patMET.py()));
	std::auto_ptr<double> met(new double(patMET.pt()));
	std::auto_ptr<double> phi(new double(patMET.phi()));
	std::auto_ptr<double> significance(new double(patMET.significance()));
	std::auto_ptr<std::vector<unsigned int > > METUncertaintyTypes(new std::vector<unsigned int>() );
	std::auto_ptr<std::vector<double> > METUncertaintiesPt(new std::vector<double>() );
	std::auto_ptr<std::vector<double> > METUncertaintiesPx(new std::vector<double>() );
	std::auto_ptr<std::vector<double> > METUncertaintiesPy(new std::vector<double>() );

	// Loop over MET uncertainties and store
	if ( storeMETUncertainties_ ) {
		for ( unsigned int unc = 0; unc < nMETUncertainties_; ++unc ) {
			METUncertaintyTypes->push_back( unc );
			METUncertaintiesPt->push_back( patMET.shiftedPt(pat::MET::METUncertainty(unc) ) );
			METUncertaintiesPx->push_back( patMET.shiftedPx(pat::MET::METUncertainty(unc) ) );
			METUncertaintiesPy->push_back( patMET.shiftedPy(pat::MET::METUncertainty(unc) ) );
		}
		iEvent.put( METUncertaintyTypes, prefix + "METUncertaintyTypes" + suffix );		
		iEvent.put( METUncertaintiesPt, prefix + "METUncertaintiesPt" + suffix );
		iEvent.put( METUncertaintiesPx, prefix + "METUncertaintiesPx" + suffix );
		iEvent.put( METUncertaintiesPy, prefix + "METUncertaintiesPy" + suffix );
	}

	iEvent.put(px, prefix + "Ex" + suffix);
	iEvent.put(py, prefix + "Ey" + suffix);
	iEvent.put(met, prefix + "ET" + suffix);
	iEvent.put(phi, prefix + "Phi" + suffix);
	iEvent.put(significance, prefix + "Significance" + suffix);
}
