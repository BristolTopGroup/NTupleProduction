#ifndef BristolNTupleTrigger
#define BristolNTupleTrigger

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

class BristolNTuple_Trigger : public edm::EDProducer {
 public:
  explicit BristolNTuple_Trigger(const edm::ParameterSet&);

 private:
  void produce( edm::Event &, const edm::EventSetup & );
  void beginRun( edm::Run &, const edm::EventSetup & );
  const edm::InputTag   l1InputTag, hltInputTag;
  const std::vector<std::string> hltPathsOfInterest, hltPathsOfInterest_other;
  HLTConfigProvider hltConfig;
  const std::string     prefix,suffix;
};

#endif
