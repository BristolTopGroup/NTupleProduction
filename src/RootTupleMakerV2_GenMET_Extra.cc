#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_GenMET_Extra.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"


RootTupleMakerV2_GenMET_Extra::RootTupleMakerV2_GenMET_Extra(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix"))
{
    produces <std::vector<double> > ( prefix + "METEx" + suffix );
    produces <std::vector<double> > ( prefix + "METEy" + suffix );
}

void RootTupleMakerV2_GenMET_Extra::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());

    //-----------------------------------------------------------------
    if (!iEvent.isRealData()) {
        edm::Handle < reco::GenMETCollection > mets;
        iEvent.getByLabel(inputTag, mets);

        if (mets.isValid()) {
            edm::LogInfo("RootTupleMakerV2_GenMETExtraInfo") << "Total # GenMETs: " << mets->size();

            for (reco::GenMETCollection::const_iterator it = mets->begin(); it != mets->end(); ++it) {

                // fill in all the vectors
                px->push_back(it->px());
                py->push_back(it->py());
            }
        } else {
            edm::LogError("RootTupleMakerV2_GenMETExtraError") << "Error! Can't get the product " << inputTag;
        }
    }

    //-----------------------------------------------------------------
    // put vectors in the event
    iEvent.put( px, prefix + "METEx" + suffix );
    iEvent.put( py, prefix + "METEy" + suffix );
}
