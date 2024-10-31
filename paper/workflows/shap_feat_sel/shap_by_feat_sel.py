"""Compute Shapley fraction captured by each feature selection method.

Args:
	-s, --shap_vals: Path to the file containing the absolute Shapley value
		fraction per loci per sample.
	-b, --basil-filtered-vars: Path to the filtered_vars.json file used by
		the LightGBM model that used BASIL feature selection.
	-p, --prsice-filtered-vars: Path to the filtered_vars.json file used by
		the LightGBM model that used PRSice feature selection.
	-t, --threshold-filtered-vars: Path to the filtered_vars.json file used by
		the LightGBM model that used threshold feature selection.
	-m, --best-model-config: Output best model config for LightGBM model that
		used threshold feature selection.
	-v, --variant-info: Path to the CSV file with variant information. Mainly
		an 'rsid' column and a 'loci' column (chr:bp). Used to map from 
		filtered_vars.json to the Shapley value column names.
	-o, --output-dir: Path to the directory where the output files will be
		written.
"""

import argparse
import json
import os

import pandas as pd
import numpy as np


s='../output/shap_per_loci/mult_pheno_1/comb_shap_vals.csv'
b='../output/aml_filter_vars_basil/mult_pheno_1/filtered_vars.json'
p='../output/aml_filter_vars_prsice/mult_pheno_1/filtered_vars.json'
t='../output/aml_filter_vars/mult_pheno_1/filtered_vars.json'
m='../output/aml_thresh_vars/mult_pheno_1/best_model_config.json'
v='../data/geno_data/chr19_var_info.csv'

def parse_args():

	parser = argparse.ArgumentParser(description="Compute Shapley fraction captured by each feature selection method.")

	parser.add_argument("-s", "--shap-vals", required=True, type=str,
		help="Path to the file containing the absolute Shapley value fraction per loci per sample.")
	parser.add_argument("-b", "--basil-filtered-vars", required=True, type=str,
		help="Path to the filtered_vars.json file used by the LightGBM model that uses BASIL feature selection.")
	parser.add_argument("-p", "--prsice-filtered-vars", required=True, type=str,
		help="Path to the filtered_vars.json file used by the LightGBM model that uses PRSice feature selection.")
	parser.add_argument("-t", "--threshold-filtered-vars", required=True, type=str,
		help="Path to the filtered_vars.json file used by the LightGBM model that uses threshold feature selection.")
	parser.add_argument("-m", "--best-model-config", required=True, type=str,
		help="Output best model config for LightGBM model that uses threshold feature selection.")
	parser.add_argument("-v", "--variant-info", required=True, type=str,
		help="Path to the CSV file with variant information. Mainly an 'rsid' column and a 'loci' column (chr:bp). Used to map from filtered_vars.json to the Shapley value column names.")
	parser.add_argument("-o", "--output-dir", required=True, type=str,
		help="Path to the directory where the output files will be written.")

	return parser.parse_args()


if __name__ == '__main__':

	args = parse_args()

	# Load Shapley values
	shap_vals = pd.read_csv(args.shap_vals, index_col=0)

	# Load variant information
	variant_info = pd.read_csv(
		args.variant_info,
		usecols=["rsid", "locus"],
	)
	variant_info['pos'] = variant_info['locus'].apply(lambda x: x.split(':')[1])

	# Load filtered_vars.json files
	with open(args.basil_filtered_vars, "r") as f:
		basil_filtered_vars = json.load(f)
	with open(args.prsice_filtered_vars, "r") as f:
		prsice_filtered_vars = json.load(f)
	with open(args.threshold_filtered_vars, "r") as f:
		threshold_filtered_vars = json.load(f)
	
	# Get threshold feature selection threshold
	with open(args.best_model_config, "r") as f:
		best_thresh_config = json.load(f)

	# Get positions included for each feature selection method
	# BASIL
	basil_raw = basil_filtered_vars['basil']['included']
	basil_rsid = []
	basil_pos = []

	for loci in basil_raw:
		if 'rs' in loci:
			loci = loci.split('_')[0]
			basil_rsid.append(loci)
		else:
			assert ':' in loci
			loci = loci.split('_')[0]
			basil_pos.append(loci.split(':')[1])

	basil_pos.extend(
		variant_info[variant_info['rsid'].isin(basil_rsid)].pos.values.tolist()
	)

	# PRSice
	prsice_raw = prsice_filtered_vars['clump']['lead']
	prsice_rsid = []
	prsice_pos = []

	for loci in prsice_raw:
		if 'rs' in loci:
			loci = loci.split('_')[0]
			prsice_rsid.append(loci)
		else:
			assert ':' in loci
			loci = loci.split('_')[0]
			prsice_pos.append(loci.split(':')[1])

	prsice_pos.extend(
		variant_info[variant_info['rsid'].isin(prsice_rsid)].pos.values.tolist()
	)

	# Threshold
	thresh_str = best_thresh_config['best_config']['filter_threshold']
	thresh_pval = thresh_str.split(',')[0].split(':')[1]
	thresh_window = thresh_str.split(',')[1].split(':')[1]

	thresh_raw = threshold_filtered_vars[thresh_pval][thresh_window]
	thresh_rsid = []
	thresh_pos = []

	for loci in thresh_raw:
		if 'rs' in loci:
			loci = loci.split('_')[0]
			thresh_rsid.append(loci)
		else:
			assert ':' in loci
			loci = loci.split('_')[0]
			thresh_pos.append(loci.split(':')[1])

	thresh_pos.extend(
		variant_info[variant_info['rsid'].isin(thresh_rsid)].pos.values.tolist()
	)

	# Compute feature selection recall, precision, and F1 score
	true_pos = shap_vals.columns.tolist()

	basil_tp = len(set(basil_pos).intersection(true_pos))
	basil_fp = len(set(basil_pos).difference(true_pos))
	basil_fn = len(set(true_pos).difference(basil_pos))

	prsice_tp = len(set(prsice_pos).intersection(true_pos))
	prsice_fp = len(set(prsice_pos).difference(true_pos))
	prsice_fn = len(set(true_pos).difference(prsice_pos))

	thresh_tp = len(set(thresh_pos).intersection(true_pos))
	thresh_fp = len(set(thresh_pos).difference(true_pos))
	thresh_fn = len(set(true_pos).difference(thresh_pos))

	scores = {
		'basil': dict(),
		'prsice': dict(),
		'thresholds': dict(),
	}

	# Recall
	scores['basil']['recall'] = basil_tp / (basil_tp + basil_fn)
	scores['prsice']['recall'] = prsice_tp / (prsice_tp + prsice_fn)
	scores['thresholds']['recall'] = thresh_tp / (thresh_tp + thresh_fn)

	# Precision
	scores['basil']['precision'] = basil_tp / (basil_tp + basil_fp)
	scores['prsice']['precision'] = prsice_tp / (prsice_tp + prsice_fp)
	scores['thresholds']['precision'] = thresh_tp / (thresh_tp + thresh_fp)

	# F1 score
	if scores['basil']['recall'] + scores['basil']['precision'] == 0:
		scores['basil']['f1'] = 0
	else:
		scores['basil']['f1'] = 2 * (
			(scores['basil']['recall'] * scores['basil']['precision']) /
			(scores['basil']['recall'] + scores['basil']['precision'])
		)
	
	if scores['prsice']['recall'] + scores['prsice']['precision'] == 0:
		scores['prsice']['f1'] = 0
	else:
		scores['prsice']['f1'] = 2 * (
			(scores['prsice']['recall'] * scores['prsice']['precision']) /
			(scores['prsice']['recall'] + scores['prsice']['precision'])
		)

	if scores['thresholds']['recall'] + scores['thresholds']['precision'] == 0:
		scores['thresholds']['f1'] = 0
	else:
		scores['thresholds']['f1'] = 2 * (
			(scores['thresholds']['recall'] * scores['thresholds']['precision']) /
			(scores['thresholds']['recall'] + scores['thresholds']['precision'])
		)

	# Get average fraction of Shapley value captured
	scores['basil']['shapley_fraction'] = shap_vals[
		list(set(basil_pos).intersection(true_pos))
	].sum(axis=1).mean()
	scores['prsice']['shapley_fraction'] = shap_vals[
		list(set(prsice_pos).intersection(true_pos))
	].sum(axis=1).mean()
	scores['thresholds']['shapley_fraction'] = shap_vals[
		list(set(thresh_pos).intersection(true_pos))
	].sum(axis=1).mean()

	# Save scores as JSON
	with open(os.path.join(args.output_dir, "feature_selection_scores.json"), "w") as f:
		json.dump(scores, f, indent=4)