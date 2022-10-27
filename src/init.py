#!/usr/bin/env python
"""Initialize the project's data space.

Iterates over all defined state points and initializes
the associated job workspace directories.
The result of running this file is the creation of a signac workspace:
    - signac.rc file containing the project name
    - signac_statepoints.json summary for the entire workspace
    - workspace/ directory that contains a sub-directory of every individual statepoint
    - signac_statepoints.json within each individual statepoint sub-directory.

"""

import signac
import logging
from collections import OrderedDict
from itertools import product


def get_parameters():
    ''''''
    parameters = OrderedDict()

    ### SYSTEM GENERATION PARAMETERS ###
    parameters["system_type"] = [
            "pack",
            #"stack",
    ]
    parameters["density"] = [1.35] #g/cm^3
    parameters["n_chains"] = [25] # int
    parameters["chain_lengths"] = [10] # int
    parameters["bead_mass"] = [100] #amu
    parameters["bond_length"] = [0.01] # nm
    parameters["forcefield"] = ["gaff"]
    parameters["box_constraints"] = [
            {"x": None, "y": None, "z": None}
	]
    parameters["kwargs"] = [
            {"expand_factor": 10},
           #{"n": 4, "a": 1.5, "b": 1.5}
	]

    ### SIMULATION PARAMETERS ###
    parameters["tau_kt"] = [0.1]
    parameters["dt"] = [0.0003]
    parameters["r_cut"] = [2.5]
    parameters["sim_seed"] = [42]
    parameters["neighbor_list"] = ["Cell"]
    parameters["init_shrink_kT"] = [7]
    parameters["final_shrink_kT"] = [7]
    parameters["shrink_steps"] = [1e6]
    parameters["shrink_period"] = [1]
    parameters["procedure"] = [
            "quench",
            #"anneal"
        ]

    ### Quench related parameters ###
    parameters["kT_quench"] = [7]
    parameters["n_steps"] = [2e5]

    ### Anneal related parameters ###
    # List of [initial kT, final kT] Reduced Temps
    #parameters["kT_anneal"] = [
    #        [6.0, 2.0]
    #    ]
    # List of lists of number of steps
    #parameters["anneal_sequence"] = [
    #        [2e5, 1e5, 3e5, 5e5, 5e5, 1e5]
    #    ]
    #parameters["schedule"] = [None]
    return list(parameters.keys()), list(product(*parameters.values()))


def main():
    project = signac.init_project("polyellipsoid") # Set the signac project name
    param_names, param_combinations = get_parameters()
    # Create the generate jobs
    for params in param_combinations:
        parent_statepoint = dict(zip(param_names, params))
        parent_job = project.open_job(parent_statepoint)
        parent_job.init()
        parent_job.doc.setdefault("done", False)

    project.write_statepoints()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
