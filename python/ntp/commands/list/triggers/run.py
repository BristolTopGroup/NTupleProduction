# from https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2016#Trigger
# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = ['-b-']
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv
  
c = ROOT.TChain("Events")
c.Add(sys.argv[1])
entries = c.GetEntries()
  
# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so")
ROOT.gSystem.Load("libDataFormatsFWLite.so")
ROOT.FWLiteEnabler.enable()
  
# load FWlite python libraries
from DataFormats.FWLite import Handle, Events
  
triggerBits, triggerBitLabel = Handle(
    "edm::TriggerResults"), ("TriggerResults", "", "HLT")
triggerObjects, triggerObjectLabel = Handle(
    "std::vector<pat::TriggerObjectStandAlone>"), "selectedPatTrigger"
triggerPrescales, triggerPrescaleLabel = Handle(
    "pat::PackedTriggerPrescales"), "patTrigger"
  
events = Events(sys.argv[1])
result = {}
  
for iev, event in enumerate(events):
    event.getByLabel(triggerBitLabel, triggerBits)
    event.getByLabel(triggerObjectLabel, triggerObjects)
    event.getByLabel(triggerPrescaleLabel, triggerPrescales)
  
    result['run'] = event.eventAuxiliary().run()
    result['luminosityBlock'] = event.eventAuxiliary().luminosityBlock()
    result['event'] = event.eventAuxiliary().event()
  
    names = event.object().triggerNames(triggerBits.product())
    triggers = []
    for i in xrange(triggerBits.product().size()):
        name = names.triggerName(i)
        prescale = triggerPrescales.product().getPrescaleForIndex(i)
        triggers.append({'name': name, 'prescale': prescale})
    result['triggers'] = triggers
    break
  
import json
IDENTIFIER = '=============='
print IDENTIFIER
print json.dumps(result, sort_keys=True)
print IDENTIFIER
