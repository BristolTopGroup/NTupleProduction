"""
    calculate systematics:
        This command produces several results for the three channels (electron, muon, combined):
        1) central measurement with error =  sqrt([combined systematic uncertainties]^2 + [unfolding]^2)
        2) all systematics evaluated with respect to central: up & down shifts, MET summary, PDF summary, Total up & down
        3) additional result for MET systematics
        4) additional result for PDF systematics
        5) additional result for TTJet theory systematic (so we can compare to them!)
        
    Usage:
        calculate systematics [--variable=<>]\
                              [--centre_of_mass_energy=<>]\
                              [--symmetrise_errors]
        
    Flags:
        symmetrise_errors:
            Instead of showing up- and down-uncertainties independently, the
            maximum of both values is shown as both up- and down-uncertainty.

        visiblePS:
            Unfold to visible phase space (instead of full phase space)

    Parameters:
        variable:
            set the variable to analyse ({variables}). Default is MET.

        centre_of_mass_energy: 
            set the centre of mass energy for analysis. Default = 13 [TeV]
            
"""
import logging
import os

from hepshell.interpreter import time_function

from ntp.commands.run import Command as C
from ntp.commands.setup import DPS_RESULTDIR

from dps.config.xsection import XSectionConfig
from dps.utils.systematic import append_PDF_uncertainties, print_dictionary,\
    get_symmetrised_systematic_uncertainty, generate_covariance_matrices,\
    get_measurement_with_total_systematic_uncertainty,\
    write_normalised_xsection_measurement, get_normalised_cross_sections
from dps.utils.file_utilities import make_folder_if_not_exists
from dps.config.variable_binning import bin_edges_vis

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
        'visiblePS': False,
        'symmetrise_errors': False,
    }

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        self.__config = None

    @time_function('calculate systematics', LOG)
    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "Running calculate systematics"
        centre_of_mass_energy = self.__variables['centre_of_mass_energy']

        self.__config = XSectionConfig(centre_of_mass_energy)

        translate_options = self.__config.translate_options
        met_specific_systematics = self.__config.met_specific_systematics
        met_type = translate_options[self.__variables['metType']]
        variables_no_met = self.__config.variables_no_met
        symmetrise_errors = self.__variables['symmetrise_errors']
        variable = self.__variables['variable']
        topMasses = self.__config.topMasses
        topMassUncertainty = self.__config.topMassUncertainty
        method = 'TUnfold'

        phase_space = 'VisiblePS'
        if not self.__variables['visiblePS']:
            phase_space = 'FullPS'

        path_to_JSON = '{path}/{com}TeV/{variable}/{phase_space}'.format(
            path=self.__variables['json_path'],
            com=centre_of_mass_energy,
            variable=self.__variables['variable'],
            phase_space=phase_space,
        )

        number_of_bins = len(bin_edges_vis[variable]) - 1

        # List of options to pass to systematic functions
        opts = {
            'met_specific_systematics': met_specific_systematics,
            'met_type': met_type,
            'variables_no_met': variables_no_met,
            'symmetrise_errors': symmetrise_errors,
            'path_to_JSON': path_to_JSON,
            'method': method,
            'variable': variable,
            'number_of_bins': number_of_bins,
            'topMasses': topMasses,
            'topMassUncertainty': topMassUncertainty
        }

        # Get list of all systematics
        all_systematics = self.__config.list_of_systematics
        # Add in the PDF weights
        all_systematics = append_PDF_uncertainties(all_systematics)

        list_of_systematics = {}
        # Do you want to use different groups of systematics?
        list_of_systematics['all'] = all_systematics

        # Print the systematics if required
        if os.environ.get("DEBUG", False):
            print_dictionary(
                "List of the systematics in use", list_of_systematics)

        for channel in ['electron', 'muon', 'combined', 'combinedBeforeUnfolding']:
            LOG.info("Channel in use is {0} : ".format(channel))

            # Output folder of covariance matrices
            covariance_matrix_output_path = 'plots/covariance_matrices/{phase_space}/{channel}/{variable}/'
            covariance_matrix_output_path = covariance_matrix_output_path.format(
                variable=variable,
                channel=channel,
                phase_space=phase_space,
            )
            make_folder_if_not_exists(covariance_matrix_output_path)

            # Add channel specific options to list of options
            opts['channel'] = channel
            opts[
                'covariance_matrix_output_path'] = covariance_matrix_output_path

            # Retreive the normalised cross sections, for all groups in
            # list_of_systematics.
            systematic_normalised_uncertainty, unfolded_systematic_normalised_uncertainty = get_normalised_cross_sections(
                opts, list_of_systematics)

            # Get and symmetrise the uncertainties
            x_sec_with_symmetrised_systematics = get_symmetrised_systematic_uncertainty(
                systematic_normalised_uncertainty, opts)
            unfolded_x_sec_with_symmetrised_systematics = get_symmetrised_systematic_uncertainty(
                unfolded_systematic_normalised_uncertainty, opts)

            # Create covariance matrices
            generate_covariance_matrices(
                opts, x_sec_with_symmetrised_systematics)
            generate_covariance_matrices(
                opts, unfolded_x_sec_with_symmetrised_systematics)

            # Combine all systematic uncertainties for each of the groups of
            # systematics
            full_measurement = get_measurement_with_total_systematic_uncertainty(
                opts, x_sec_with_symmetrised_systematics)
            full_unfolded_measurement = get_measurement_with_total_systematic_uncertainty(
                opts, unfolded_x_sec_with_symmetrised_systematics)

            # Write central +- error to JSON. Group of systematics in question
            # is included in outputfile name.
            for keys in list_of_systematics.keys():
                write_normalised_xsection_measurement(
                    opts, full_measurement[keys], full_unfolded_measurement[keys], summary=keys)
        return True
