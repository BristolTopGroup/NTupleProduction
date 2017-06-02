#ifndef BristolNTuplePFJetsExtra
#define BristolNTuplePFJetsExtra

#include <string>
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/PFJet.h"

class BristolNTuple_PFJets : public edm::EDProducer {

 public:
  explicit BristolNTuple_PFJets(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT< std::vector < pat::Jet > > inputTag;
  const edm::EDGetTokenT< edm::View< reco::PFJet > > eventJetInputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness1InputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness2InputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness3InputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness4InputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness5InputTag;
  const edm::EDGetTokenT< edm::ValueMap < float > > njettiness6InputTag;

  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const double      minJetPtToStore;
  const bool readJEC;
  const bool doVertexAssociation;
  const bool isRealData;
};

#endif
