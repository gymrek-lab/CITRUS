import json
import os
from itertools import product

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm
import scipy.stats as stats
import scikit_posthocs as sp


if __name__ == '__main__':

	results_dir = '../../output'
	pheno_name = 'phenotype'

	sim_names = [
		'mult_pheno_1',				# Multiplicative 1
		'mult_pheno_2',				# Multiplicative 2
		'compound_het',				# Compound het close pair of SNPs
		'compound_het_2',			# Compound het far pair of SNPs
		'xor_pheno_2',				# XOR close
		'xor_pheno_1',				# XOR far
		'gepsi_lin_add_h0625_h0625',# CITRUS lin-add h^2 = 0.0625
		'gepsi_lin_add_h0625',		# GEPSi lin-add h^2 = 0.0625
		'gepsi_lin_add_h0625_gcta',	# GCTA lin-add h^2 = 0.0625
		'gepsi_lin_add_h125_h125',	# CITRUS lin-add h^2 = 0.125
		'gepsi_lin_add_h125',		# GEPSi lin-add h^2 = 0.125
		'gepsi_lin_add_h125_gcta',	# GCTA lin-add h^2 = 0.125
		'gepsi_lin_add_h25_h25',	# CITRUS lin-add h^2 = 0.25
		'gepsi_lin_add_h25',		# GEPSi lin-add h^2 = 0.25
		'gepsi_lin_add_h25_gcta',	# GCTA lin-add h^2 = 0.25
		'gepsi_lin_add_h5_h5',		# CITRUS lin-add h^2 = 0.5
		'gepsi_lin_add_h5',			# GEPSi lin-add h^2 = 0.5
		'gepsi_lin_add_h5_gcta',	# GCTA lin-add h^2 = 0.5
		'gepsi_lin_add_hFULL_hFULL',# CITRUS lin-add h^2 = 1.0
		'gepsi_lin_add_hFULL',		# GEPSi lin-add h^2 = 1.0
		'gepsi_lin_add_hFULL_gcta',	# GCTA lin-add h^2 = 1.0
	]

	model_names = [
		'PRSice-2',
		'BASIL',
		'LGBM-Threshold',
		'LGBM-PRSice',
		'LGBM-BASIL',
	]

	feat_sel_dict = {
		'PRSice-2': 'PRSice',
		'BASIL': 'BASIL',
		'LGBM-PRSice': 'PRSice',
		'LGBM-BASIL': 'BASIL',
		'LGBM-Threshold': 'p-val + window'
	}

	ci = "95"
	herit_data_dir = '../../pheno_sim/citrus_output'

	# Load all results
	res_list = []

	n_total = len(sim_names) * len(model_names)

	# Desc to model output dir
	desc_to_outdir = {
		'PRSice-2': 'prsice',
		'BASIL': 'basil',
		'LGBM-PRSice': 'aml_prsice_vars',
		'LGBM-BASIL': 'aml_basil_vars',
		'LGBM-Threshold': 'aml_thresh_vars',
	}

	for sim_name, model_name in tqdm(
		product(sim_names, model_names),
		desc='Loading performance data',
		total=n_total,
		ncols=100
	):
		res_fname = 'scores.json'

		res_path = os.path.join(
			results_dir, desc_to_outdir[model_name], sim_name, res_fname
		)

		# Check that results exist
		if not os.path.isfile(res_path):
			print(f"CANNOT FIND: {res_path}")
			continue

		# Load JSON of results
		with open(res_path, 'r') as f:
			res_data = json.load(f)

		res_data['Simulation Name'] = sim_name
		res_data['Model'] = model_name
		res_data['Feature Selection'] = feat_sel_dict[model_name]

		res_list.append(res_data)

	# Create dataframe of results
	res_df = pd.DataFrame(res_list, )

	# Add R^2 column based on test scores
	res_df['R^2'] = res_df['test'].apply(lambda x: float(x['r2']))

	# Perform Kruskal-Wallis test for Models
	kruskal_model = stats.kruskal(
		*[res_df[res_df['Model'] == model]['R^2'] for model in model_names]
	)
	print('Kruskal-Wallis test result for models:', kruskal_model)

	# Perform Kruskal-Wallis test for Datasets
	kruskal_dataset = stats.kruskal(
		*[res_df[res_df['Simulation Name'] == sim]['R^2'] for sim in sim_names]
	)
	print('Kruskal-Wallis test result for datasets:', kruskal_dataset)

	# Perform post-hoc analysis for models using Dunn's test
	posthoc_model = sp.posthoc_conover(res_df, val_col='R^2', group_col='Model', p_adjust='bonferroni')
	# print(posthoc_model)

	# Perform post-hoc analysis for datasets using Dunn's test
	posthoc_dataset = sp.posthoc_conover(res_df, val_col='R^2', group_col='Simulation Name', p_adjust='bonferroni')
	# print(posthoc_dataset)

	# Visualize with a boxplot and save the plots
	plt.figure(figsize=(10, 6))
	sns.boxplot(x='Simulation Name', y='R^2', hue='Model', data=res_df)
	plt.title('R^2 Scores by Model and Simulation')
	plt.xlabel('Simulation Name')
	plt.ylabel('R^2')
	plt.legend(title='Model')
	plt.xticks(rotation=90)
	plt.tight_layout()
	plt.savefig('r2_scores_by_model_and_simulation.png')
	plt.close()

	plt.figure(figsize=(10, 6))
	sns.boxplot(x='Model', y='R^2', hue='Simulation Name', data=res_df)
	plt.title('R^2 Scores by Simulation and Model')
	plt.xlabel('Model')
	plt.ylabel('R^2')
	plt.legend(title='Simulation Name')
	plt.xticks(rotation=90)
	plt.tight_layout()
	plt.savefig('r2_scores_by_simulation_and_model.png')
	plt.close()

	# Generate and save significance plot for models
	plt.figure(figsize=(10, 6))
	sp.sign_plot(posthoc_model, alpha=0.05)
	plt.title('Significance Plot for Models')
	plt.xlabel('Model')
	plt.ylabel('Significance')
	plt.tight_layout()
	plt.savefig('significance_plot_models.png')
	plt.close()

	# Generate and save significance plot for datasets
	plt.figure(figsize=(10, 6))
	sp.sign_plot(posthoc_dataset, alpha=0.05)
	plt.title('Significance Plot for Datasets')
	plt.xlabel('Simulation Name')
	plt.ylabel('Significance')
	plt.tight_layout()
	plt.savefig('significance_plot_datasets.png')
	plt.close()

	# Generate and save critical difference diagram for models
	
	# Calculate average ranks for models
	res_df['Rank_Model'] = res_df.groupby('Simulation Name')['R^2'].rank(pct=True)
	avg_rank_model = res_df.groupby('Model')['Rank_Model'].mean()
	print('Average ranks for models:', avg_rank_model)

	# Plot critical difference diagram for models
	plt.figure(figsize=(10, 2), dpi=100)
	plt.title('Critical difference diagram of average score ranks for models')
	sp.critical_difference_diagram(avg_rank_model, posthoc_model)
	plt.savefig('critical_difference_diagram_models.png')
	plt.close()

	# Generate and save critical difference diagram for datasets

	# Calculate average ranks for datasets
	res_df['Rank_Sim'] = res_df.groupby('Model')['R^2'].rank(pct=True)
	avg_rank_sim = res_df.groupby('Simulation Name')['Rank_Sim'].mean()
	print('Average ranks for datasets:', avg_rank_sim)

	# Plot critical difference diagram for datasets
	plt.figure(figsize=(10, 2), dpi=100)
	plt.title('Critical difference diagram of average score ranks for datasets')
	sp.critical_difference_diagram(avg_rank_sim, posthoc_dataset)
	plt.savefig('critical_difference_diagram_datasets.png')
	plt.close()