#ifndef BristolNTupleRecoMETExtra
#define BristolNTupleRecoMETExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/METReco/interface/PFMETCollection.h"

class BristolNTuple_RecoMET : public edm::EDProducer {
 public:
  explicit BristolNTuple_RecoMET(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT< std::vector<reco::PFMET> > inputTag;
  const std::string     prefix,suffix;
};

#endif
