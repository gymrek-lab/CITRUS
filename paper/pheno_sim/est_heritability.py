"""Estimate heritability of simulated CITRUS phenotypes."""

import json
import os

from pheno_sim import PhenoSimulation
from pheno_sim.heritability_estimation import broad_sense_heritability


if __name__ == '__main__':

	sim_name = 'gepsi_lin_add_hFULL_hFULL'
	config_dir = 'citrus_output'

	print(sim_name)

	# Load simulation config
	with open(os.path.join(config_dir, sim_name + '_config.json'), 'r') as f:
		sim_config = json.load(f)

	# Create simulation
	sim = PhenoSimulation(sim_config)

	# Load genotype data
	input_vals = sim.run_input_step()

	# Compute heritability
	confidence_level = 95

	heritability = broad_sense_heritability(
		sim,
		input_vals=input_vals,
		n_samples=0.1,
		confidence_level=confidence_level/100,
	)

	# Save results
	with open(
		os.path.join(
			config_dir, sim_name + f'_heritability_ci{confidence_level}.json'
		),
		'w'
	) as f:
		json.dump(heritability, f, indent=4)

