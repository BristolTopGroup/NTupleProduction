#ifndef BristolNTupleElectronsExtra
#define BristolNTupleElectronsExtra

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "DataFormats/PatCandidates/interface/VIDCutFlowResult.h"

class BristolNTuple_Electrons : public edm::EDProducer {
 public:
  explicit BristolNTuple_Electrons(const edm::ParameterSet&);
  virtual bool returnInvertedSelection(const vid::CutFlowResult fullCutFlowData, std::vector<uint> invertedSelection) const;

 private:
  void produce( edm::Event &, const edm::EventSetup & );

  const edm::EDGetToken inputTag;

  const std::string     prefix,suffix;
  const unsigned int    maxSize;
  const bool storePFIsolation_, debugRelease_;

  const edm::EDGetTokenT<std::vector<reco::Vertex>> vtxInputTag;
  const edm::EDGetTokenT<reco::BeamSpot> beamSpotInputTag;
  const edm::EDGetTokenT<std::vector<reco::Conversion>> conversionsInputTag;
  edm::EDGetTokenT<edm::ValueMap<bool> > mediumElectronIDMapToken_;
  edm::EDGetTokenT<edm::ValueMap<vid::CutFlowResult> > eleMediumIdFullInfoMapToken_;
  edm::ValueMap<bool> mediumElectronIDDecisions_;
  edm::ValueMap<vid::CutFlowResult> medium_id_cutflow_data_;
};

#endif

