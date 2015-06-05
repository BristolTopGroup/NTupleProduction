import sys
# import ROOT in batch mode
import ROOT
ROOT.gROOT.SetBatch(True)
# import rootpy stuff
from rootpy.tree import Tree, TreeModel
from rootpy.tree import IntCol, FloatCol, FloatArrayCol, CharCol, CharArrayCol
from rootpy.io import root_open
from random import gauss, choice, sample
from string import letters

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

# import FWlite python objects
from DataFormats.FWLite import Handle, Events

# open file (you can use 
# 'edmFileUtil -d /store/whatever.root' 
# to get the physical file name)
events = Events("/hdfs/TopQuarkGroup/test/TT_Tune4C_13TeV-pythia8-tauola_PU_S14_PAT_miniAOD.root")

f = root_open("test.root", "recreate")
# define the model
class Muon(TreeModel):
    eta = FloatCol(default=-1111.)
    phi = FloatCol(default=-1111.)
    pt = FloatCol()
    
class Event(Muon.prefix('muon1_'), Muon.prefix('muon2_')):
    run_number = IntCol()

tree = Tree("test", model=Event)

for i,event in enumerate(events):
    print "\nEvent", i
    handle  = Handle ('std::vector<pat::Muon>')
    label = ("slimmedMuons")
    event.getByLabel (label, handle)
    muons = handle.product()
    tree.run_number = event.id().run()
    print "Number of muons", len(muons)
    if len(muons) > 1:
        tree.muon1_.pt = muons[0].pt()
        tree.muon2_.pt = muons[1].pt()  
    if i > 10: break
tree.write()
f.close()
