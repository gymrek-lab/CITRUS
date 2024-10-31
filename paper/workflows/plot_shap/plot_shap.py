"""Plot feature selection performance."""

import json
import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':

	sim_names = [
		'mult_pheno_1',
		'mult_pheno_2',
		'compound_het',
		'compound_het_2',
		'xor_pheno_2',
		'xor_pheno_1',
		'gepsi_lin_add_h0625_h0625',
		'gepsi_lin_add_h125_h125',
		'gepsi_lin_add_h25_h25',
		'gepsi_lin_add_h5_h5',
		'gepsi_lin_add_hFULL_hFULL',
	]

	results_dir = '../../output/shap_feat_sel'
	scores_fname = 'feature_selection_scores.json'

	# Load scores
	scores = []
	for sim_name in sim_names:
		with open(os.path.join(results_dir, sim_name, scores_fname), 'r') as f:
			sim_scores = json.load(f)

		for method in sim_scores:
			scores.append({
				'simulation': sim_name,
				'feature_selection_method': method,
				'recall': sim_scores[method]['recall'],
				'precision': sim_scores[method]['precision'],
				# 'f1': sim_scores[method]['f1'],
				'shapley_fraction': sim_scores[method]['shapley_fraction'],
			})

	scores = pd.DataFrame(scores)

	# Melt scores
	melted_scores = pd.melt(
		scores,
		id_vars=['simulation', 'feature_selection_method'],
		value_vars=['recall', 'precision', 'shapley_fraction'],
		var_name='metric',
		value_name='score',
	)

	# Plot
	# Each row is a metric, each column is a simulation
	sns.set_context("talk", font_scale=1.5)
	sns.set_style("whitegrid", {"axes.yaxis.grid": True})

	g = sns.catplot(
		data=melted_scores,
		x='feature_selection_method',
		order=['prsice', 'basil', 'thresholds'],
		y='score',
		row='metric',
		row_order=['shapley_fraction', 'recall', 'precision'],
		col='simulation',
		hue='feature_selection_method',
		kind='bar',
		sharey='row',
		margin_titles=True,
	)

	# Modify titles
	for ax, sim_name in zip(g.axes.flat, sim_names):
		# Set the title to just the simulation name
		if '_noise' in sim_name:
			ax.set_title(sim_name.replace('_noise', ''))
		elif 'lin_add' in sim_name:
			herit = sim_name.split('h')[1].split('_')[0]
			if herit == 'FULL':
				ax.set_title(f"Linear Additive\n(H^2 = 1.0)")
			else:
				ax.set_title(f"Linear Additive\n(H^2 = 0.{herit})")
		elif 'mult_pheno' in sim_name:
			version_num = sim_name.split('_')[-1]
			ax.set_title(f"Multiplicative {version_num}")
		elif sim_name == "compound_het":
			ax.set_title("Compound Het. (close)")
		elif sim_name == "compound_het_2":
			ax.set_title("Compound Het. (far)")
		elif sim_name == "xor_pheno_2":
			ax.set_title("Haplotype XOR (close)")
		elif sim_name == "xor_pheno_1":
			ax.set_title("Haplotype XOR (far)")
		else:
			ax.set_title(sim_name)

	# Set row titles
	row_titles = ["Shapley fraction", "Recall", "Precision"]
	for ax, title in zip(g.axes[:,0], row_titles):
		ax.set_ylabel(title, labelpad=20)

	# Adjust the font size of x-category labels and remove x-axis titles
	g.set(xlabel='')
	for ax in g.axes.flat:
		ax.tick_params(axis='x', labelsize=18)

	plt.savefig('feat_sel.png', dpi=600)
	plt.close()