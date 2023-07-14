""" Test SHAP with CITRUS simulations. 

TODO: Replace with a demo for users and remove this file.
"""

import copy

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap

from pheno_sim import PhenoSimulation
from pheno_sim.shap import SHAPWrapper


if __name__ == '__main__':
    
	# Load simulation
	config_path = 'test_configs/simple_sim_rerun.json'
	simulation = PhenoSimulation.from_JSON_file(config_path)

	# Run simulation
	input_vals = simulation.run_input_step()
	pred_vals = simulation.run_simulation_steps(
		copy.deepcopy(input_vals)
	)

	# Create input data DataFrame
	input_df = simulation.vals_dict_to_dataframe(input_vals)

	# Create SHAP wrapper
	shap_wrapper = SHAPWrapper(simulation, 'phenotype', input_df.columns)

	# Create SHAP explainer
	explainer = shap.Explainer(
		shap_wrapper,
		input_df,
		algorithm='permutation',
		# algorithm='partition',
	)

	# Calculate SHAP values
	shap_values = explainer(input_df)


	# Plotting

	# Plot bee swarm plot of SHAP values
	plt.figure(figsize=(20, 6))
	shap.plots.beeswarm(shap_values, max_display=20, show=False)
	plt.title('SHAP values')
	plt.subplots_adjust(left=0.3)
	plt.show()

	# Plot violin plot of SHAP values
	shap.plots.violin(
		shap_values, plot_type='layered_violin', max_display=20, show=False
	)
	plt.title('SHAP values')
	plt.subplots_adjust(left=0.3)
	plt.show()

	# Bar plot of mean absolute SHAP values
	shap.plots.bar(shap_values, show=False)
	# Make extra space on left for long labels
	plt.subplots_adjust(left=0.4)
	plt.title('Mean absolute SHAP values')

	# Plot sum bar plot count of input variants
	count_df = input_df.sum(axis=0).to_frame().reset_index()
	count_df.columns = ['input name', 'count']
	count_df['variant'] = count_df['input name'].map(
		lambda x: x.split('*-*')[0]
	)

	plt.figure()
	sns.barplot(
		x='count',
		y='input name',
		hue='variant',
		data=count_df,
		dodge=False,
		order=count_df.sort_values('count', ascending=False)['input name'],
	)
	plt.title('Count of input variants')
	plt.subplots_adjust(left=0.4)
	plt.show()

	# Plot SHAP values for highest and lowest phenotype values
	max_idx = np.argmax(pred_vals['phenotype'])
	min_idx = np.argmin(pred_vals['phenotype'])

	shap.plots.waterfall(shap_values[max_idx], show=False)
	plt.gca().set_title('Highest phenotype SHAP values')
	plt.subplots_adjust(left=0.4)
	
	plt.figure()
	shap.plots.waterfall(shap_values[min_idx], show=False)
	plt.gca().set_title('Lowest phenotype SHAP values')
	plt.subplots_adjust(left=0.4)

	plt.show()

	# # Plot descision plot
	# mean_pheno = np.mean(pred_vals['phenotype'])
	# shap.plots.decision(
	# 	mean_pheno,
	# 	shap_values.values,
	# 	input_df,
	# 	show=False,
	# 	alpha=0.2,
	# 	feature_order=np.argsort(
	# 		# np.abs(shap_values.values).max(0),
	# 		# np.mean(shap_values.values, axis=0),
	# 		input_df.sum(axis=0).values
	# 	),
	# 	ignore_warnings=True,
	# )
	# plt.subplots_adjust(left=0.4)
	# plt.show()
