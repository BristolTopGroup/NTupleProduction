#ifndef BristolNTupleGenJetsExtra
#define BristolNTupleGenJetsExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"

class BristolNTuple_GenJets : public edm::EDProducer {
 public:
  explicit BristolNTuple_GenJets(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT<reco::GenJetCollection > inputTag;
  const std::string     prefix,suffix;
  const double minPt, maxAbsoluteEta;
  const unsigned int    maxSize;
};

#endif
