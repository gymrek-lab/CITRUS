""" Compute SHAP Shapley value estimates for a given simulation. """

import copy
import json
import re

import pandas as pd
import shap

from pheno_sim.shap import SHAPWrapper


def run_SHAP(
	simulation,
	phenotype: str='phenotype',
	save_path=None,
	save_config_path=None,
):
	"""Runs SHAP Shapley value estimation for a given simulation.
	
	Data is read from genotype data files defined in the simulation object.

	Returns a DataFrame and optionally saves it to a CSV file if save_path
	is not None. The DataFrame contains a 'sample_id' column and:
		if collapse_haplotypes is True, one column for each input loci.
		if collapse_haplotypes is False, two columns for each input loci.

	Args:
		simulation (PhenoSimulation): PhenoSimulation object.
		phenotype (str, default 'phenotype'): Phenotype key to use
			for SHAP values.
		save_path (str, optional): Path to save DataFrame to. Defaults to None.
			If None, DataFrame is not saved.
		save_config_path (str, optional): Path to save simulation config to.
			Useful if simulation config contains random elements (like
			RandomConstants) that had not yet been drawn. Defaults to None,
			which does not save simulation config.
	"""

	# Get input data
	input_df = simulation.vals_dict_to_dataframe(
		simulation.run_input_step()
	)

	print(input_df.head())

	# Create SHAP wrapper
	shap_wrapper = SHAPWrapper(simulation, phenotype, input_df.columns)

	# Create SHAP explainer
	explainer = shap.Explainer(
		shap_wrapper,
		input_df,
		algorithm='permutation',
		# algorithm='partition',
	)

	# Calculate SHAP values
	shap_values = explainer(input_df)

	# Create DataFrame from SHAP values
	shap_values = pd.DataFrame(
		shap_values.values,
		columns=input_df.columns,
	)

	# Add sample IDs
	shap_values['sample_id'] = simulation.sample_ids

	# Save SHAP values
	if save_path is not None:
		shap_values.to_csv(save_path, index=False)

	# Save simulation config
	if save_config_path is not None:
		with open(save_config_path, 'w') as f:
			json.dump(simulation.get_config(), f, indent=4)
		
	# return shap_values, explainer


if __name__ == '__main__':
	""" Example of what CL script would look like. """

	from pheno_sim import PhenoSimulation

	sim_config_path = 'test_configs/simple_sim.json'
	phenotype_key = 'phenotype'

	# This would be different for CL to allow for passing
	# genotype files as args. See run_simulation.py for example.
	simulation = PhenoSimulation.from_JSON_file(sim_config_path)

	output = run_SHAP(
		simulation,
		phenotype_key,
		save_path='test_shap.csv',
		save_config_path='test_shap_config.json',
	)

	print(output)
	print(type(output))


	# shap.summary_plot(output)
	print(output.shape)

	

