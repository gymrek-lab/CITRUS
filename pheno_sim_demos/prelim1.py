""" Preliminary testing """

import os
import inspect

import numpy as np

from pheno_sim import PhenoSimulation
from pheno_sim import func_nodes

# define custom class and pass to PhenoSimulation 

if __name__ == "__main__":
    
    # Create an input ValuesDict
	input_vals = {
		"SNP1": (
			np.array([0] * 10 + [1] * 10),
			np.array([0] * 5 + [1] * 5 + [0] * 5 + [1] * 5)
		),
		"SNP2": (np.ones(20), np.zeros(20)),
		"SNP3": (np.zeros(20), np.ones(20))
	}

    # Create a PhenoSimulation object from a list of steps
	simulator = PhenoSimulation.from_sim_steps_list([
		func_nodes.Identity('identity_1', 'SNP1'),
		func_nodes.Identity('identity_2', 'SNP2'),
		func_nodes.Identity('identity_3', 'SNP3'),
		func_nodes.AdditiveCombine('SNP1_combine', 'identity_1'),
		func_nodes.MeanCombine(
			'SNP2_combine', 'identity_2', mean_type='arithmetic'
		),
	])

	# Run the simulation
	output_vals = simulator.run_simulation_steps(input_vals)
	print(output_vals)
