from FWCore.ParameterSet.VarParsing import VarParsing
import sys
import os

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

      options.register ('isTTbarMC',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Is this ttbar MC")

      options.register ('isData',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Is this data")

      options.register ('isLocalRunning',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Is this being run locally?")

      options.register ('isReReco',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Is this rereco data")

      options.register ('isRunC',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Is this RunC rereco data")

      options.register('selectionInTaggingMode',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Apply full selection in tagging mode")
      
      options.register('useJECFromFile',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Apply Jet Energy Corrections from SQLite file.")   
      
      options.register('applyResiduals',
                        True,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        'Application of residual corrections. Have to be set' +
                        ' to True once the 13 TeV residual corrections are ' +
                        'available. False to be kept meanwhile.')
      
      options.register('printEventContent',
                        False,
                        VarParsing.multiplicity.singleton,
                        VarParsing.varType.bool,
                        "Print the event content just before ntuple.")

      options.parseArguments()

      if options.tagAndProbe and not options.jetSelectionInTaggingMode:
            print 'Error : Do not run tag and probe studies without jet selection in tagging mode.'
            sys.exit()

CMSSW_VERSION = os.environ['CMSSW_VERSION']
varray = CMSSW_VERSION.split('_')
CMSSW_MAJOR_VERSION, CMSSW_MINOR_VERSION = varray[1], varray[2]
