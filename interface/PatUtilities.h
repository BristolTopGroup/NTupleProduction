#ifndef LQ_PatUtilities_h
#define LQ_PatUtilities_h

#include "DataFormats/MuonReco/interface/MuonFwd.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrackFwd.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"

reco::TrackRef pmcTrack(const pat::Muon& mu, int & refit_id);

reco::TrackRef tevOptimized(const reco::TrackRef& trackerTrack, const reco::TrackRef& gmrTrack,
		const reco::TrackRef& fmsTrack, const reco::TrackRef& pmrTrack, int & refit_id);

//------------------------------------------------------------------
// The code below does the work of TrackBase::validFraction()
// TrackBase::validFraction() is implemented in CMSSW_4_2_0 and later
// This function is intended for use in release prior to CMSSW_4_2_0
// When working with CMSSW_4_2_0 and later, 
//     use TrackBase::validFraction(), not this function
//------------------------------------------------------------------

template<class T>
double validFraction(const T & track) {

	if (track.isNull())
		return -2;

	int valid = track->hitPattern().numberOfValidTrackerHits();
	int lost = track->hitPattern().numberOfLostTrackerHits();
	int lostIn = track->trackerExpectedHitsInner().numberOfLostTrackerHits();
	int lostOut = track->trackerExpectedHitsOuter().numberOfLostTrackerHits();

	if ((valid + lost + lostIn + lostOut) == 0)
		return -1;
	return valid / (1.0 * (valid + lost + lostIn + lostOut));

}

/**
 If the directional parameter is set, computes directional isolation, i.e. an
 (angular-)disperson weighted sum of pT of the provided isoParticles. Otherwise
 computes a simple scalar sum of isoParticles. In both cases the pT of the
 particles involved can be weighted or not by a gaussian fall-off instead of
 a strict use-it-or-not cone.
 @note   The probe particle is always omitted from the considered isoParticles
 (if they are from the same collection, of course).
 from:
 http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/lowette/SandBox/Skims/interface/SAKLooseLepton.h?revision=1.1&view=markup
 */
template<typename Particle, typename IsoParticle>
double customIsolation(const Particle& particle, const edm::Handle<std::vector<IsoParticle> >& isoParticles,
		double coneDR, bool directional, bool falloff, reco::PFCandidate::ParticleType lepton) {

	const double maxDR = (falloff ? 5 * coneDR : coneDR);
	double isoSum = 0;
	math::XYZVector isoAngleSum;
	std::vector < math::XYZVector > coneParticles;
	bool matched = false;
	for (unsigned int particleIndex = 0; particleIndex < isoParticles->size(); ++particleIndex) {
		if (lepton == reco::PFCandidate::mu && (*isoParticles)[particleIndex].muonRef().isNonnull()
				&& (*isoParticles)[particleIndex].trackRef() == particle.track()) {
			matched = true;
			continue;
		}
		if (lepton == reco::PFCandidate::e && (*isoParticles)[particleIndex].gsfTrackRef().isNonnull()
				&& (*isoParticles)[particleIndex].gsfTrackRef() == particle.gsfTrack()) {
			matched = true;
			continue;
		}
		const IsoParticle& isoParticle = (*isoParticles)[particleIndex];
		const double dR = reco::deltaR(isoParticle, particle);
		if (dR > maxDR)
			continue;
		if (isoParticle.particleId() == reco::PFCandidate::gamma && isoParticle.pt() < 0.5)
			continue;
		if (isoParticle.particleId() == reco::PFCandidate::h0 && isoParticle.pt() < 0.5)
			continue;
		const double weight = falloff ? TMath::Gaus(dR, 0, coneDR, true) : 1;

		//.........................................................................
		if (directional) {
			math::XYZVector transverse(isoParticle.eta() - particle.eta(),
					reco::deltaPhi(isoParticle.phi(), particle.phi()), 0);
			transverse *= weight * isoParticle.pt() / transverse.rho();
			if (transverse.rho() > 0) {
				isoAngleSum += transverse;
				coneParticles.push_back(transverse);
			} //else if (lepton == reco::PFCandidate::e)
//				edm::LogDebug("PatUtilitiesError") << "ZERO! " << (*isoParticles)[particleIndex].muonRef().isNonnull()
//						<< " " << (*isoParticles)[particleIndex].gsfTrackRef().id() << " " << particle.gsfTrack().id()
//						<< " " << (*isoParticles)[particleIndex].gsfTrackRef().key() << " " << particle.gsfTrack().key();
		}
		//.........................................................................
		else {
			isoSum += weight * isoParticle.pt();
		}
	} // end loop over PF candidates

//	if (!matched)
//		edm::LogDebug("PatUtilitiesError") << "AAAH a non-matched lepton! " << (int) (lepton == reco::PFCandidate::mu)
//				<< " " << (int) (lepton == reco::PFCandidate::e) << " " << isoSum << " " << particle.pt();

	if (directional) {
		double directionalPT = 0;
		for (unsigned int particleIndex = 0; particleIndex < coneParticles.size(); ++particleIndex)
			directionalPT += pow(
					TMath::ACos(
							coneParticles[particleIndex].Dot(isoAngleSum) / coneParticles[particleIndex].rho()
									/ isoAngleSum.rho()), 2) * coneParticles[particleIndex].rho();
		return directionalPT;
	}
	return isoSum;

}

#endif 
