import json
import os
from itertools import product

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm


if __name__ == '__main__':

	results_dir = '../../output'
	pheno_name = 'phenotype'

	# sim_names = [
	# 	'lin_add_nvar1000_h2_v1',
	# 	'lin_add_nvar1000_h4_v1',
	# 	'compound_het',
	# 	'compound_het_2',
	# 	'xor_pheno_2',
	# 	'xor_pheno_1',
	# 	'complex_pheno_1_noise',
	# 	'complex_pheno_2',
	# 	'complex_pheno_3',
	# 	'complex_pheno_4',
	# 	'mult_pheno_1',
	# 	'mult_pheno_2',
	# ]
	# sim_names = [
	# 	'lin_add_nvar100_h2_v1',
	# 	'lin_add_nvar100_h4_v1',
	# 	'mult_pheno_1',
	# 	'mult_pheno_2',
	# 	'compound_het',
	# 	'compound_het_2',
	# 	'xor_pheno_2',
	# 	'xor_pheno_1',
	# ]
	# sim_names = [
	# 	'lin_add_nvar100_h05_v1',
	# 	'lin_add_nvar100_h1_v1',
	# 	'lin_add_nvar100_h2_v1',
	# 	'lin_add_nvar100_h4_v1',
	# 	'lin_add_nvar100_h8_v1',
	# 	'gepsi_lin_add_h15',
	# 	'gepsi_lin_add_h15_h15',
	# 	'gepsi_lin_add_h15_gcta',
	# 	'gepsi_lin_add_hFULL',
	# 	'gepsi_lin_add_hFULL_hFULL',
	# 	'gepsi_lin_add_hFULL_gcta',
	# ]
	# sim_names = [
	# 	'mult_pheno_1',				# Multiplicative 1
	# 	'mult_pheno_2',				# Multiplicative 2
	# 	'compound_het',				# Compound het close pair of SNPs
	# 	'compound_het_2',			# Compound het far pair of SNPs
	# 	'xor_pheno_2',				# XOR close
	# 	'xor_pheno_1',				# XOR far
	# 	'lin_add_nvar100_h05_v1',	# CITRUS only lin-add h^2 = 0.05, 100 causal
	# 	'lin_add_nvar100_h1_v1',	# CITRUS only lin-add h^2 = 0.1, 100 causal
	# 	'lin_add_nvar100_h2_v1',	# CITRUS only lin-add h^2 = 0.2, 100 causal
	# 	'lin_add_nvar100_h4_v1',	# CITRUS only lin-add h^2 = 0.4, 100 causal
	# 	'lin_add_nvar100_h8_v1',	# CITRUS only lin-add h^2 = 0.4, 100 causal
	# 	'gepsi_lin_add_h15',		# Common lin-add GEPSI h^2 = 0.15 (100 causal for all)
	# 	'gepsi_lin_add_h15_h15',	# Common lin-add CITRUS  h^2 = 0.15
	# 	'gepsi_lin_add_h15_gcta',	# Common lin-add GCTA  h^2 = 0.15
	# 	'gepsi_lin_add_hFULL',		# Common lin-add GEPSI h^2 = 1.0
	# 	'gepsi_lin_add_hFULL_hFULL',# Common lin-add CITRUS h^2 = 1.0
	# 	'gepsi_lin_add_hFULL_gcta',	# Common lin-add GCTA h^2 = 1.0
	# ]
	sim_names = [
		# 'mult_pheno_1',				# Multiplicative 1
		# 'mult_pheno_2',				# Multiplicative 2
		# 'compound_het',				# Compound het close pair of SNPs
		# 'compound_het_2',			# Compound het far pair of SNPs
		'xor_pheno_2',				# XOR close
		# 'xor_pheno_1',				# XOR far
		# 'gepsi_lin_add_h0625_h0625',# CITRUS lin-add h^2 = 0.0625
		# 'gepsi_lin_add_h0625',		# GEPSi lin-add h^2 = 0.0625
		# 'gepsi_lin_add_h0625_gcta',	# GCTA lin-add h^2 = 0.0625
		# 'gepsi_lin_add_h125_h125',	# CITRUS lin-add h^2 = 0.125
		# 'gepsi_lin_add_h125',		# GEPSi lin-add h^2 = 0.125
		# 'gepsi_lin_add_h125_gcta',	# GCTA lin-add h^2 = 0.125
		# 'gepsi_lin_add_h25_h25',	# CITRUS lin-add h^2 = 0.25
		# 'gepsi_lin_add_h25',		# GEPSi lin-add h^2 = 0.25
		# 'gepsi_lin_add_h25_gcta',	# GCTA lin-add h^2 = 0.25
		# 'gepsi_lin_add_h5_h5',		# CITRUS lin-add h^2 = 0.5
		# 'gepsi_lin_add_h5',			# GEPSi lin-add h^2 = 0.5
		# 'gepsi_lin_add_h5_gcta',	# GCTA lin-add h^2 = 0.5
		# 'gepsi_lin_add_hFULL_hFULL',# CITRUS lin-add h^2 = 1.0
		# 'gepsi_lin_add_hFULL',		# GEPSi lin-add h^2 = 1.0
		# 'gepsi_lin_add_hFULL_gcta',	# GCTA lin-add h^2 = 1.0
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

	# Load heritability data
	herit_data = []

	for sim_name in sim_names:
		herit_json_path = f"{herit_data_dir}/{sim_name}_heritability_ci{ci}.json"

		if not os.path.isfile(herit_json_path):
			continue

		with open(herit_json_path, 'r') as f:
			sim_herit_data = json.load(f)

		herit_data.append({
			"sim_name": sim_name,
			"heritability": sim_herit_data['H2']
		})

	herit_data = pd.DataFrame(herit_data)

	print('Herit')
	print(herit_data.head(20))
	herit_data.to_csv('herit.csv', index=False)

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

	# Make point plots
	sns.set_style("whitegrid", {"axes.yaxis.grid": True})

	# Save results df as csv
	res_df.to_csv('results.csv', index=False)

	palette_prof_2 = [
		'#4E9A06',  # Olive Green (Group C - C-A)
		'#EFB73E',  # Sun Yellow (Group C - C-B)
		'#8AE234',  # Light Green (Group C - C-A)
		'#FFCE56',  # Lighter Sun Yellow (Group C - C-B)
		'#3465A4',  # Royal Blue (Group A)
		'#729FCF',  # Light Royal Blue (Group A)
		'#A40000',  # Red (Group B)
		'#EF2929'   # Bright Red (Group B)
	]

	palette = palette_prof_2

	print(res_df)

	g = sns.catplot(
		kind='point',
		data=res_df,
		col='Simulation Name',
		x='Model',
		y='R^2',
		hue='Model',
		dodge=True,
		hue_order=model_names,
		# palette=palette,
		sharey=True,
		legend_out=False,
		aspect=0.6,
		markersize=20,
		linewidth=10,
		markers='_',
	)

	# Set y lims
	y_min = 0
	y_max = 1.02
	for ax in g.axes.flat:
		ax.set_ylim(y_min, y_max)

	# Make lines transparent
	for ax in g.axes.flat:
		for line in ax.lines:
			line.set_alpha(0.5)

	# Add heritability data as dashed red line
	for ax, sim_name in zip(g.axes.flat, sim_names):
		# Filter herit_data for the current sim_name
		herit_value = herit_data[herit_data["sim_name"] == sim_name]["heritability"].values

		# Check if there is a heritability value for the current sim_name
		if len(herit_value) > 0:
			ax.axhline(
				y=herit_value[0],
				color='#9955BB',
				linestyle='--',
				linewidth=3,
			)
			# Set y-limit to 1.1 times the heritability value
			# ax.set_ylim(0, 1.1 * herit_value[0])
		else:
			print(f"No herit: {sim_name}")

		# Set the title to just the simulation name
		if '_noise' in sim_name:
			ax.set_title(sim_name.replace('_noise', ''))
		elif 'gcta' in sim_name:
			if 'FULL' in sim_name:
				ax.set_title(
					f"GCTA (H^2 = 1.0)"
				)
			else:
				gcta_h2 = sim_name.split('h')[1].split('_')[0]
				ax.set_title(
					f"GCTA (H^2 = 0.{gcta_h2})"
				)
		elif 'gepsi' in sim_name:
			if len(sim_name.split('h')) == 3:
				gep_h2 = sim_name.split('h')[1].strip('_')
				citrus_h2 = sim_name.split('h')[2]

				if gep_h2 == 'FULL':
					gep_h2 = '1.0'
				else:
					gep_h2 = f"0.{gep_h2}"

				if citrus_h2 == 'FULL':
					citrus_h2 = '1.0'
				else:
					citrus_h2 = f"0.{citrus_h2}"

				ax.set_title(
					f"CITRUS (H^2 = {citrus_h2})"
				)

			elif 'FULL' in sim_name:
				ax.set_title(f"GEPSi (H^2 = 1.0)")
			else:
				herit = sim_name.split('h')[1]
				ax.set_title(f"GEPSi (H^2 = 0.{herit})")
		elif 'lin_add' in sim_name:
			herit = sim_name.split('h')[1].split('_')[0]
			ax.set_title(f"Linear Additive (H^2 = 0.{herit})")
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

		# Rotate and left-align x labels
		ax.set_xticklabels(ax.get_xticklabels(), rotation=-25, ha='left')

		# Shift x-tick labels to the left
		from matplotlib.transforms import ScaledTranslation
		dx = -0.10  # Adjust the value as needed
		dy = 0  # No vertical shift
		offset = ScaledTranslation(dx, dy, ax.figure.dpi_scale_trans)
		for label in ax.xaxis.get_majorticklabels():
			label.set_transform(label.get_transform() + offset)

	g.set(ylim=(0, None))
	plt.tight_layout(w_pad=-1.0, rect=(0, 0, 1, 1))
	plt.savefig('r2_pointplot.png', dpi=600)
	plt.close()

	# print(herit_data)
	# print(res_df)