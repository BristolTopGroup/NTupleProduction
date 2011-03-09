#include "BristolAnalysis/NTupleTools/interface/RootTupleMakerV2_PFJets_Extra.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include <iostream>

RootTupleMakerV2_PFJets_Extra::RootTupleMakerV2_PFJets_Extra(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize"))
{
    produces <std::vector<double> > (prefix + "Px" + suffix);
    produces <std::vector<double> > (prefix + "Py" + suffix);
    produces <std::vector<double> > (prefix + "Pz" + suffix);
    produces <std::vector<double> > (prefix + "Charge" + suffix);
    produces <std::vector<double> > (prefix + "Mass" + suffix);
    produces <std::vector<double> > ( prefix + "ChargedEmEnergyFractionRAW"  + suffix );
    produces <std::vector<double> > ( prefix + "ChargedHadronEnergyFractionRAW"  + suffix );
    produces <std::vector<double> > ( prefix + "NeutralEmEnergyFractionRAW"  + suffix );
    produces <std::vector<double> > ( prefix + "NeutralHadronEnergyFractionRAW"  + suffix );
}

void RootTupleMakerV2_PFJets_Extra::
produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

    std::auto_ptr < std::vector<double> > px(new std::vector<double>());
    std::auto_ptr < std::vector<double> > py(new std::vector<double>());
    std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
    std::auto_ptr < std::vector<double> > charge(new std::vector<double>());
    std::auto_ptr < std::vector<double> > mass(new std::vector<double>());
    std::auto_ptr < std::vector<double> > chargedEmEnergyFractionRAW  ( new std::vector<double>()  ) ;
    std::auto_ptr < std::vector<double> > chargedHadronEnergyFractionRAW  ( new std::vector<double>()  ) ;
    std::auto_ptr < std::vector<double> > neutralEmEnergyFractionRAW  ( new std::vector<double>()  ) ;
    std::auto_ptr < std::vector<double> > neutralHadronEnergyFractionRAW  ( new std::vector<double>()  ) ;


  edm::Handle<std::vector<pat::Jet> > jets;
  iEvent.getByLabel(inputTag, jets);

  if(jets.isValid()) {
    edm::LogInfo("RootTupleMakerV2_PFJetsInfo") << "Total # PFJets: " << jets->size();

    for( std::vector<pat::Jet>::const_iterator it = jets->begin(); it != jets->end(); ++it ) {
      // exit from loop when you reach the required number of jets
      if(px->size() >= maxSize)
        break;

      // fill in all the vectors
      px->push_back( it->px() );
      py->push_back( it->py() );
      pz->push_back( it->pz() );

      chargedEmEnergyFractionRAW->push_back( it->correctedJet("Uncorrected").chargedEmEnergyFraction() );
      chargedHadronEnergyFractionRAW->push_back( it->correctedJet("Uncorrected").chargedHadronEnergyFraction() );
      neutralEmEnergyFractionRAW->push_back( it->correctedJet("Uncorrected").neutralEmEnergyFraction() );
      neutralHadronEnergyFractionRAW->push_back( it->correctedJet("Uncorrected").neutralHadronEnergyFraction() );
      charge->push_back( it->jetCharge() );
      mass->push_back( it->mass() );


    }
  } else {
    edm::LogError("RootTupleMakerV2_PFJetsError") << "Error! Can't get the product " << inputTag;
  }

  //-----------------------------------------------------------------
  // put vectors in the event
  iEvent.put(px, prefix + "Px" + suffix);
    iEvent.put(py, prefix + "Py" + suffix);
    iEvent.put(pz, prefix + "Pz" + suffix);
    iEvent.put(charge, prefix + "Charge" + suffix);
    iEvent.put(mass, prefix + "Mass" + suffix);
    iEvent.put( chargedEmEnergyFractionRAW,  prefix + "ChargedEmEnergyFractionRAW"  + suffix );
    iEvent.put( chargedHadronEnergyFractionRAW,  prefix + "ChargedHadronEnergyFractionRAW"  + suffix );
    iEvent.put( neutralEmEnergyFractionRAW,  prefix + "NeutralEmEnergyFractionRAW"  + suffix );
    iEvent.put( neutralHadronEnergyFractionRAW,  prefix + "NeutralHadronEnergyFractionRAW"  + suffix );
}
