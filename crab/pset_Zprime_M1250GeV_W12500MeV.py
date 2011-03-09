from pset_default_MC import *

# rename output file
proc = 'Zprime_M1250GeV_W12500MeV'
process.TFileService.fileName = 'nTuple_%s.root' %proc
process.out.fileName          = 'pat_%s.root' %proc