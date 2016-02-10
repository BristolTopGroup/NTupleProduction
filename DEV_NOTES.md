Developement Notes
==================

getByLabel() => getByToken()
----------------------------
getByToken is a lot more rigid than getByLabel, where it requires an EDGetToken created from a call to consumes(). 
The call to consumes() requires that the product Type be known.  This method is faster than getByLabel and guarantees 
that you've registered to request the data. getByToken is also multithread enabled unlike getByLabel.

	.h
  	const edm::EDGetTokenT<std::vector<pat::Muon>> inputTag;

	.cc (Initialiser)
  	inputTag(consumes<std::vector<pat::Muon>>(iConfig.getParameter<edm::InputTag>("InputTag"))),			
	
	.cc (call)
	edm::Handle < std::vector<pat::Muon> > muons;
	iEvent.getByToken(inputTag, muons);
