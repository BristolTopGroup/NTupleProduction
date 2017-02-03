/**
 * Produces global variables and similar:
 *  - HT: scalar sum of pT of all jets above a threshold
 *  - ST: HT + MET + signal lepton pT
 *  -
 *
 *  Why do we not include this in BristolNTuple_Event.cc?
 *  BristolNTuple_Event is meant to run once per event,
 *  while this module can run N times (once for each selection, jet energy variation, etc).
 */
// system include files
#include <memory>
#include <vector>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "FWCore/Utilities/interface/StreamID.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include "BristolAnalysis/NTupleTools/interface/PatUtilities.h"

namespace ntp {
namespace userdata {

class EventUserData: public edm::stream::EDProducer<> {
public:
  typedef std::vector<unsigned int> IndexCollection;
  explicit EventUserData(const edm::ParameterSet&);
  ~EventUserData();

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  virtual void beginStream(edm::StreamID) override;
  virtual void produce(edm::Event&, const edm::EventSetup&) override;
  virtual void endStream() override;

  pat::JetCollection getCleanedJets(const pat::JetCollection& jets, const IndexCollection& indices);
  // inputs
  const edm::EDGetTokenT<std::vector<reco::Vertex> > vtxInputTag_;
  edm::EDGetToken electronInputTag_, muonInputTag_, jetInputTag_, bJetInputTag_, metInputTag_;
  bool isElectron_;

  std::string prefix_;
  std::string suffix_;

};

EventUserData::EventUserData(const edm::ParameterSet& iConfig) :
        vtxInputTag_(
            consumes < std::vector<reco::Vertex> > (iConfig.getParameter < edm::InputTag > ("vertexCollection"))),
        electronInputTag_(
            consumes < std::vector<pat::Electron> > (iConfig.getParameter < edm::InputTag > ("electronCollection"))),
        muonInputTag_(consumes < std::vector<pat::Muon> > (iConfig.getParameter < edm::InputTag > ("muonCollection"))),
        jetInputTag_(consumes < std::vector<pat::Jet> > (iConfig.getParameter < edm::InputTag > ("jetCollection"))), //
        bJetInputTag_(consumes < std::vector<pat::Jet> > (iConfig.getParameter < edm::InputTag > ("bJetCollection"))), //
        metInputTag_(consumes < std::vector<pat::MET> > (iConfig.getParameter < edm::InputTag > ("metInputTag"))), //
        isElectron_(iConfig.getParameter<bool>("isElectron")), //
        prefix_(iConfig.getParameter < std::string > ("prefix")), //
        suffix_(iConfig.getParameter < std::string > ("suffix"))
{
  //register your products
  produces<double>(prefix_ + "HT" + suffix_);
  produces<double>(prefix_ + "ST" + suffix_);
  produces<double>(prefix_ + "M3" + suffix_);
  produces<double>(prefix_ + "Mbl" + suffix_);
  produces<double>(prefix_ + "anglebl" + suffix_);
  produces<double>(prefix_ + "MT" + suffix_);
  produces<double>(prefix_ + "WPT" + suffix_);
}

EventUserData::~EventUserData()
{

  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)

}

//
// member functions
//

// ------------ method called to produce the data  ------------
void EventUserData::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  edm::Handle < std::vector<pat::Electron> > electrons;
  iEvent.getByToken(electronInputTag_, electrons);

  edm::Handle < std::vector<pat::Muon> > muons;
  iEvent.getByToken(muonInputTag_, muons);

  edm::Handle < std::vector<pat::Jet> > jetHandle;
  iEvent.getByToken(jetInputTag_, jetHandle);
  const pat::JetCollection& jets = *jetHandle.product();

  edm::Handle < std::vector<pat::Jet> > bJetHandle;
  iEvent.getByToken(bJetInputTag_, bJetHandle);
  const pat::JetCollection& bjets = *bJetHandle.product();

  edm::Handle < std::vector<pat::MET> > mets;
  iEvent.getByToken(metInputTag_, mets);

  const pat::MET & met(mets->at(0));

  const double DEFAULT_VALUE=-999;
  std::auto_ptr<double> ht(new double(utils::ht(jets)));
  std::auto_ptr<double> st(new double(DEFAULT_VALUE));
  std::auto_ptr<double> m3(new double(DEFAULT_VALUE));
  std::auto_ptr<double> m_bl(new double(DEFAULT_VALUE));
  std::auto_ptr<double> angle_bl(new double(-9));
  std::auto_ptr<double> mt(new double(DEFAULT_VALUE));
  std::auto_ptr<double> wpt(new double(DEFAULT_VALUE));

  if (jets.size() >= 3)
    *m3 = utils::m3(jets);

  if ((electrons.isValid() && isElectron_) ||  (muons.isValid() && !isElectron_)) {
    const reco::Candidate* lepton =
        isElectron_ ?
            (reco::Candidate*) &electrons->front() :
            (reco::Candidate*) &muons->front();
    if (lepton) {
      if (bjets.size() > 0) {
        *m_bl = utils::m_bl(bjets, lepton);
        *angle_bl = utils::angle_bl(bjets, lepton);
      }
      *st = utils::st(jets, met, lepton);
      *mt = utils::mt(met, lepton);
      *wpt = utils::wpt(met, lepton);
    }

  }

  iEvent.put(ht, prefix_ + "HT" + suffix_);
  iEvent.put(st, prefix_ + "ST" + suffix_);
  iEvent.put(m3, prefix_ + "M3" + suffix_);
  iEvent.put(m_bl, prefix_ + "Mbl" + suffix_);
  iEvent.put(angle_bl, prefix_ + "anglebl" + suffix_);
  iEvent.put(mt, prefix_ + "MT" + suffix_);
  iEvent.put(wpt, prefix_ + "WPT" + suffix_);

}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void EventUserData::beginStream(edm::StreamID)
{
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void EventUserData::endStream()
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void EventUserData::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE (EventUserData);
} //userdata
} //ntp
