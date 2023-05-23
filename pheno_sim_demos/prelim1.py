""" Preliminary testing v1: SNP with masking group 

Description:
	promoter_SNP: Equivalent to drawing from one of two Gaussian
		distributions, where those with the SNP are drawn from the
		distribution with the lower mean.
	LOF_SNPS: SNPS in this group drastically reduce gene function.
		# Gene function will be the following if any LOF_SNPs are
		# present (otherwise it will be function_based_on_promoter_SNP):
		# 	function_based_on_promoter_SNP * sigmoid(-num_LOF_SNPs)

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from pheno_sim import PhenoSimulation
from pheno_sim import func_nodes


if __name__ == "__main__":

	n_samples = 1000
    
	# Create an input ValuesDict
	input_vals = {
		"promoter_SNP": (
			np.random.default_rng().binomial(1, 0.5, size=n_samples),
			np.random.default_rng().binomial(1, 0.5, size=n_samples)
		),
		"LOF_SNPS": (
			np.random.default_rng().binomial(1, 0.01, size=(20, n_samples)),
			np.random.default_rng().binomial(1, 0.01, size=(20, n_samples))
		),
	}

	# Create simulation
	sim_spec = {
		'simulation_steps': [
			# Effect of promoter SNP
			{
				'type': 'Distribution',
				'alias': 'normal_function',
				'dist_name': 'normal',
				'dist_kwargs': {
					'loc': 1.25,
					'scale': 0.2
				},
				'input_match_size': 'promoter_SNP'
			},
			{
				'type': 'Distribution',
				'alias': 'function_wo_promoter',
				'dist_name': 'normal',
				'dist_kwargs': {
					'loc': 0.75,
					'scale': 0.2
				},
				'input_match_size': 'promoter_SNP'
			},
			{
				'type': 'IfElse',
				'alias': 'function_based_on_promoter_SNP',
				'input_cond_vals': 'promoter_SNP',
				'input_if_vals': 'function_wo_promoter',
				'input_else_vals': 'normal_function'
			},
			# Effect of LOF SNPs
			{
				'type': 'AnyReduce',
				'alias': 'gene_LOF',
				'input_alias': 'LOF_SNPS'
			},
			{
				'type': 'Distribution',
				'alias': 'function_w_LOF',
				'dist_name': 'normal',
				'dist_kwargs': {
					'loc': 0.3,
					'scale': 0.2
				},
				'input_match_size': 'promoter_SNP'
			},
			{
				'type': 'IfElse',
				'alias': 'function_based_on_LOF',
				'input_cond_vals': 'gene_LOF',
				'input_if_vals': 'function_w_LOF',
				'input_else_vals': 'function_based_on_promoter_SNP'
			},
			# Combine Haplotype effects
			{
				'type': 'MinCombine',
				'alias': 'gene_level_func',
				'input_alias': 'function_based_on_LOF'
			},
			{
				'type': 'Identity', # I'll use this as an output node
				'alias': 'phenotype',
				'input_alias': 'gene_level_func'
			}
		]
	}

	simulator = PhenoSimulation(sim_spec)

	# Run sim with nodes from spec
	output_vals = simulator.run_simulation_steps(input_vals)

	# Sum haplotypes in output vals to make into a dataframe
	df_dict = {}

	for key in output_vals:
		if isinstance(output_vals[key], tuple):
			val = output_vals[key][0] + output_vals[key][1]
		else:
			val = output_vals[key]

		if val.ndim == 1:
			df_dict[key] = val

	df = pd.DataFrame(df_dict)

	# Do both of the above plots in one figure
	fig, axes = plt.subplots(1, 2, figsize=(10, 5))
	sns.kdeplot(ax=axes[0], data=df, x="phenotype")
	sns.kdeplot(ax=axes[1], data=df, x="phenotype", hue="promoter_SNP")
	plt.show()

	# Do both of the above plots in one figure
	fig, axes = plt.subplots(1, 2, figsize=(10, 5))
	sns.kdeplot(ax=axes[0], data=df, x="phenotype")
	sns.kdeplot(ax=axes[1], data=df, x="phenotype", hue="gene_LOF")
	plt.show()

	# Plot the underlying distributions for when
	# promoter_SNP = 0 and promoter_SNP = 1
	fig, ax = plt.subplots()
	sns.kdeplot(ax=ax, data=df, x="normal_function")
	sns.kdeplot(ax=ax, data=df, x="function_wo_promoter")
	plt.show()
