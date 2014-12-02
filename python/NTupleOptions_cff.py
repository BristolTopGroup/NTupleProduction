from FWCore.ParameterSet.VarParsing import VarParsing
import sys

def getOptions( options ):
      options.register ('tagAndProbe',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Use tag and probe selection")

      options.register ('jetSelectionInTaggingMode',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Apply jet selection requirements (last 6 selection steps) in tagging mode")

      options.parseArguments()

      if options.tagAndProbe and not options.jetSelectionInTaggingMode:
            print 'Error : Do not run tag and probe studies without jet selection in tagging mode.'
            sys.exit()

