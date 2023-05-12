""" Preliminary testing """

import os
import inspect

import numpy as np

from pheno_sim import PhenoSimulation
from pheno_sim import func_nodes


if __name__ == "__main__":
    
	# Create an input ValuesDict
	input_vals = {
		"SNP1": (
			np.array([0] * 10 + [1] * 10),
			np.array([0] * 5 + [1] * 5 + [0] * 5 + [1] * 5)
		),
		"SNP2": (np.ones(20), np.zeros(20)),
	}


	# Create a PhenoSimulation object from a list of steps
	simulator = PhenoSimulation.from_sim_steps_list([
		func_nodes.Identity('identity_1', 'SNP1'),
		func_nodes.Identity('identity_2', 'SNP2'),
		func_nodes.AdditiveCombine('SNP1_combine', 'identity_1'),
		func_nodes.MeanCombine(
			'SNP2_combine', 'identity_2', mean_type='arithmetic'
		),
	])

	# Run the simulation
	output_vals = simulator.run_simulation_steps(input_vals)
	print(output_vals)


	# With a FunctionNodeBuilder (what is being done internally by PhenoSimulation)
	builder = func_nodes.FunctionNodeBuilder()

	steps_from_builder = [
		builder.create_node('Identity', alias='identity_1', input_alias='SNP1'),
		builder.create_node('Identity', alias='identity_2', input_alias='SNP2'),
		builder.create_node(
			'AdditiveCombine', alias='SNP1_combine', input_alias='identity_1'),
		builder.create_node(
			'MeanCombine', alias='SNP2_combine', input_alias='identity_2',
			mean_type='arithmetic'
		),
	]

	simulator_from_builder = PhenoSimulation.from_sim_steps_list(steps_from_builder)

	# Run sim with nodes from builder
	output_vals_from_builder = simulator_from_builder.run_simulation_steps(input_vals)
	print(output_vals_from_builder)


	# With a PhenoSimulation object and a dict specification
	sim_spec = {
		'simulation_steps': [
			{
				'type': 'Identity',
				'alias': 'identity_1',
				'input_alias': 'SNP1',
			},
			{
				'type': 'Identity',
				'alias': 'identity_2',
				'input_alias': 'SNP2',
			},
			{
				'type': 'AdditiveCombine',
				'alias': 'SNP1_combine',
				'input_alias': 'identity_1',
			},
			{
				'type': 'MeanCombine',
				'alias': 'SNP2_combine',
				'input_alias': 'identity_2',
				'mean_type': 'arithmetic',
			},
		]
	}

	simulator_from_spec = PhenoSimulation(sim_spec)

	# Run sim with nodes from spec
	output_vals_from_spec = simulator_from_spec.run_simulation_steps(input_vals)
	print(output_vals_from_spec)