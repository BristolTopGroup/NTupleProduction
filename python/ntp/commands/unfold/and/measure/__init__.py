"""
    unfold and measure:
        Runs DailyPythonScripts/dps/analysis/xsection/02_unfold_and_measure.py
        
    Usage:
        unfold and measure [--visiblePS] [--test]\
                           [--variable=<>] [--bjetbin=<>] [--metType=<>] \
                           [--unfolding_method=<>]
                           [--centre_of_mass_energy=<>]
                           [--unfolding_error_treatment=<>]

    Flags:
        test:
            Just run the central measurement

        visiblePS:
            Unfold to visible phase space (instead of full phase space)

    Parameters:
        variable:
            set the variable to analyse ({variables}). Default is MET.

        bjetbin:
            set b-jet multiplicity for analysis.
            Options: exclusive: 0-3, inclusive (N or more): 0m, 1m, 2m, 3m, 4m

        metType:
            set MET type for analysis. Default: type1

        centre_of_mass_energy: 
            set the centre of mass energy for analysis. Default = 13 [TeV]
            
        unfolding_error_treatment:
            parameter for error treatment in unfolding procedure.
            Default: {unfolding_error_treatment}

"""
import logging
import os
from copy import deepcopy
import importlib

from hepshell.interpreter import time_function

from ntp.commands.run import Command as C
from ntp.commands.setup import DPS_RESULTDIR

# from dps.config.xsection import XSectionConfig
# import dps.config.RooUnfold as unfoldCfg
# from dps.utils.file_utilities import read_data_from_JSON, write_data_to_JSON
# from dps.utils.Calculation import calculate_xsection, calculate_normalised_xsection, \
#     combine_complex_results

unfold_and_measure = importlib.import_module(
    'dps.analysis.xsection.02_unfold_and_measure', 'dps.analysis.xsection')
get_unfolded_normalisation = unfold_and_measure.get_unfolded_normalisation
calculate_xsections = unfold_and_measure.calculate_xsections
calculate_normalised_xsections = unfold_and_measure.calculate_normalised_xsections

LOG = logging.getLogger(__name__)

JSON_PATH = os.path.join(
    DPS_RESULTDIR, 'normalisation', 'background_subtraction')


class Command(C):
    REQUIRE_GRID_CERT = False
    DEFAULTS = {
        'json_path': JSON_PATH,
        'variable': 'MET',
        'bjetbin': '2m',
        'metType': 'type1',
        'unfolding_method': 'TUnfold',
        'centre_of_mass_energy': 13,
        'combine_before_unfolding': False,
        'test': False,
        'use_ptreweight': False,
        'visiblePS': False,
#         'unfolding_error_treatment': unfoldCfg.error_treatment,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        self.__measurement_config = None
        self.__unfolding_files = {}

    @time_function('unfold and measure', LOG)
    def run(self, args, variables):
        from ntp import NTPROOT
        self.__prepare(args, variables)

        conda_path = os.path.join(NTPROOT, 'external', 'miniconda')
        dps_script_path = os.path.join(
            conda_path, 'envs', 'ntp', 'lib',
            'python2.7', 'site-packages', 'dps', 'analysis', 'xsection',
            '02_unfold_and_measure.py'
        )
        python = os.path.join(conda_path, 'envs', 'ntp', 'bin', 'python')
        params = ' '.join([
            '-v {0}'.format(self.__variables['variable']),
            '--visiblePS',
            '-c {0}'.format(self.__variables['centre_of_mass_energy']),
            '-p {0}'.format(self.__variables['json_path']),
        ])
        if self.__variables['test']:  # temporary solution
            params += ' --test'

        command = '{python} {script} {params}'.format(
            python=python, script=dps_script_path, params=params,
        )
        conda_activate = os.path.join(conda_path, 'bin', 'activate')
        conda_env = 'source {0} ntp'.format(conda_activate)
        command = '{0} && {1}'.format(conda_env, command)
        from hepshell.interpreter import call
        call(command, logger=LOG, shell=True)

        return True
