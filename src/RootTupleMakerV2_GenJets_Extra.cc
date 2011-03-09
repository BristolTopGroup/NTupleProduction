#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_GenJets_Extra.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"


RootTupleMakerV2_GenJets_Extra::RootTupleMakerV2_GenJets_Extra(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize"))
{
    produces <std::vector<double> > ( prefix + "Px" + suffix );
    produces <std::vector<double> > ( prefix + "Py" + suffix );
    produces <std::vector<double> > ( prefix + "Pz" + suffix );
    produces <std::vector<double> > ( prefix + "Charge" + suffix );
    produces <std::vector<double> > ( prefix + "Mass" + suffix );
}

void RootTupleMakerV2_GenJets_Extra::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr<std::vector<double> >  px  ( new std::vector<double>()  );
      std::auto_ptr<std::vector<double> >  py  ( new std::vector<double>()  );
      std::auto_ptr<std::vector<double> >  pz  ( new std::vector<double>()  );
      std::auto_ptr<std::vector<double> >  charge  ( new std::vector<double>()  );
      std::auto_ptr<std::vector<double> >  mass  ( new std::vector<double>()  );

  //-----------------------------------------------------------------
  if( !iEvent.isRealData() ) {
    edm::Handle<reco::GenJetCollection> genJets;
    iEvent.getByLabel(inputTag, genJets);

    if( genJets.isValid() ) {
      edm::LogInfo("RootTupleMakerV2_GenJetsExtraInfo") << "Total # GenJets: " << genJets->size();

      for( reco::GenJetCollection::const_iterator it = genJets->begin(); it != genJets->end(); ++it ) {
        // exit from loop when you reach the required number of GenJets
        if(px->size() >= maxSize)
          break;

        // fill in all the vectors
        px->push_back(it->px());
        py->push_back(it->py());
        pz->push_back(it->pz());
        charge->push_back(it->charge());
        mass->push_back(it->mass());
      }
    } else {
      edm::LogError("RootTupleMakerV2_GenJetsExtraError") << "Error! Can't get the product " << inputTag;
    }
  }

  //-----------------------------------------------------------------
  // put vectors in the event
  iEvent.put( px, prefix + "Px" + suffix );
    iEvent.put( py, prefix + "Py" + suffix );
    iEvent.put( pz, prefix + "Pz" + suffix );
    iEvent.put( charge, prefix + "Charge" + suffix );
    iEvent.put( mass, prefix + "Mass" + suffix );
}
