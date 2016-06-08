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
if entries:
    print entries
else:
    print -1
