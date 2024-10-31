"""Compute Shapley fraction per loci so can be used to evaluate
feature selection.

Args:
	-s, --shapley: CSV with Shapley values per loci per haplotype
	-c, --simulation-config: JSON with simulation configuration
	-o, --output-dir: Directory to save output files.
"""

import argparse
import os
import json

import numpy as np
import pandas as pd


s='../output/shap/mult_pheno_1/shap_vals.csv'
c='../pheno_sim/citrus_output/mult_pheno_1_config.json'


def parse_args():
	parser = argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-s', '--shapley', required=True)
	parser.add_argument('-c', '--simulation-config', required=True)
	parser.add_argument('-o', '--output-dir', required=True)
	return parser.parse_args()


if __name__ == '__main__':
	args = parse_args()

	# Load Shapley values
	shap_vals = pd.read_csv(
		args.shapley
	).set_index('sample_id')

	# Load simulation configuration
	with open(args.simulation_config, 'r') as f:
		input_config = json.load(f)['input']

	# Get absolute Shapley values, then combine loci on both haplotypes
	shap_vals = shap_vals.abs()

	comb_shap_vals = pd.DataFrame(
		index=shap_vals.index
	)

	# Find which columns correspond to the same loci
	loci_to_cols = dict()
	for col_name in shap_vals.columns:
		split_name = col_name.split('*-*')
		if len(split_name) == 3:
			input, strand, idx = split_name
		elif len(split_name) == 2:
			input, strand = split_name
			idx = '0'

		if input not in loci_to_cols:
			loci_to_cols[input] = dict()

		if idx not in loci_to_cols[input]:
			loci_to_cols[input][idx] = []

		loci_to_cols[input][idx].append(col_name)

	# Combine loci
	for input in loci_to_cols:
		for idx in loci_to_cols[input]:
			# Assert two columns per loci
			assert len(loci_to_cols[input][idx]) == 2

			# Combine Shapley values
			comb_shap_vals[input + '*-*' + idx] = shap_vals[
				loci_to_cols[input][idx]
			].sum(axis=1)

	# Rename loci to position
	col_to_pos_map = dict()
	input_node_map = dict()

	for input_node in input_config[0]['input_nodes']:
		input_node_map[input_node['alias']] = input_node['pos']

	for col in comb_shap_vals.columns:
		input, idx = col.split('*-*')
		col_to_pos_map[col] = input_node_map[input][int(idx)]

	comb_shap_vals = comb_shap_vals.rename(columns=col_to_pos_map)

	# Scale so each row sums to 1
	comb_shap_vals = comb_shap_vals.div(
		comb_shap_vals.sum(axis=1),
		axis=0
	)

	# Save combined Shapley values
	comb_shap_vals.reset_index().to_csv(
		os.path.join(args.output_dir, 'comb_shap_vals.csv'),
		index=False
	)
