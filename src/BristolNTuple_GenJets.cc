#include "BristolAnalysis/NTupleTools/interface/BristolNTuple_GenJets.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"


BristolNTuple_GenJets::BristolNTuple_GenJets(const edm::ParameterSet& iConfig) :
    inputTag(iConfig.getParameter<edm::InputTag>("InputTag")),
    prefix  (iConfig.getParameter<std::string>  ("Prefix")),
    suffix  (iConfig.getParameter<std::string>  ("Suffix")),
    minPt (iConfig.getParameter<double> ("minPt")),
    maxAbsoluteEta (iConfig.getParameter<double> ("maxAbsoluteEta")),
    maxSize (iConfig.getParameter<unsigned int> ("MaxSize"))
{
	produces < std::vector<double> > (prefix + "Px" + suffix);
	produces < std::vector<double> > (prefix + "Py" + suffix);
	produces < std::vector<double> > (prefix + "Pz" + suffix);
	produces < std::vector<double> > (prefix + "Energy" + suffix);
	produces < std::vector<double> > (prefix + "Charge" + suffix);
	produces < std::vector<double> > (prefix + "Mass" + suffix);

	produces < std::vector<int> > (prefix + "pdgId" + suffix);

	produces < std::vector<double> > (prefix + "EMF" + suffix);
	produces < std::vector<double> > (prefix + "HADF" + suffix);
}

void BristolNTuple_GenJets::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {

	std::auto_ptr < std::vector<double> > px(new std::vector<double>());
	std::auto_ptr < std::vector<double> > py(new std::vector<double>());
	std::auto_ptr < std::vector<double> > pz(new std::vector<double>());
	std::auto_ptr < std::vector<double> > energy(new std::vector<double>());
	std::auto_ptr < std::vector<double> > charge(new std::vector<double>());
	std::auto_ptr < std::vector<double> > mass(new std::vector<double>());

	std::auto_ptr < std::vector<int> > pdgId(new std::vector<int>());

	std::auto_ptr < std::vector<double> > emf(new std::vector<double>());
	std::auto_ptr < std::vector<double> > hadf(new std::vector<double>());

	//-----------------------------------------------------------------
	if (!iEvent.isRealData()) {
		edm::Handle < reco::GenJetCollection > genJets;
		iEvent.getByLabel(inputTag, genJets);

		if (genJets.isValid()) {
			edm::LogInfo("BristolNTuple_GenJetsExtraInfo") << "Total # GenJets: " << genJets->size();

			for (reco::GenJetCollection::const_iterator it = genJets->begin(); it != genJets->end(); ++it) {
				// exit from loop when you reach the required number of GenJets
				if (px->size() >= maxSize)
					break;

				if (it->pt() < minPt || fabs(it->eta()) > maxAbsoluteEta)
					continue;

				// fill in all the vectors
				px->push_back(it->px());
				py->push_back(it->py());
				pz->push_back(it->pz());
				energy->push_back(it->energy());
				charge->push_back(it->charge());
				mass->push_back(it->mass());

				pdgId->push_back(it->pdgId());

				emf->push_back(it->emEnergy() / it->energy());
				hadf->push_back(it->hadEnergy() / it->energy());
			}
		} else {
			edm::LogError("BristolNTuple_GenJetsExtraError") << "Error! Can't get the product " << inputTag;
		}
	}

	//-----------------------------------------------------------------
	// put vectors in the event
	iEvent.put(px, prefix + "Px" + suffix);
	iEvent.put(py, prefix + "Py" + suffix);
	iEvent.put(pz, prefix + "Pz" + suffix);
	iEvent.put(energy, prefix + "Energy" + suffix);
	iEvent.put(charge, prefix + "Charge" + suffix);
	iEvent.put(mass, prefix + "Mass" + suffix);

	iEvent.put(pdgId, prefix + "pdgId" + suffix);

	iEvent.put(emf, prefix + "EMF" + suffix);
	iEvent.put(hadf, prefix + "HADF" + suffix);
}
