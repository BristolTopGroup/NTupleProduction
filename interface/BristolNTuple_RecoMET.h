#ifndef BristolNTupleRecoMETExtra
#define BristolNTupleRecoMETExtra

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"

#include "DataFormats/METReco/interface/METFwd.h"
#include "DataFormats/METReco/interface/MET.h"
class BristolNTuple_RecoMET : public edm::EDProducer {
 public:
  explicit BristolNTuple_RecoMET(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  const edm::EDGetTokenT< reco::METCollection > inputTag;
  const std::string     prefix,suffix;
};

#endif
