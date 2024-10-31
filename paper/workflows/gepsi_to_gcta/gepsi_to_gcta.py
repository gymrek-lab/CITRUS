"""Create GCTA simulation config from GEPSi sim info.

Args:
	-g, --gepsi-out-dir: Directory containing GEPSi output files.
	-d, --gepsi-out-desc: Description part of GEPSi output file names.
	-h, --herit: Heritability
	-v, --variant-info: Variant info file
	-o, --output-dir: Directory to write simulation config to.
"""

import argparse
import os
import json
import math

import numpy as np
import pandas as pd


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--gepsi-out-dir", required=True)
	parser.add_argument("-d", "--gepsi-out-desc", required=True)
	parser.add_argument("-h2", "--herit", required=True)
	parser.add_argument("-v", "--variant-info", required=True)
	parser.add_argument("-o", "--output-dir", required=True)
	return parser.parse_args()


if __name__ == '__main__':

	args = parse_args()
	print(args)

	# Load GEPSi SNP info
	causal_snps = pd.read_csv(
		os.path.join(
			args.gepsi_out_dir, f"{args.gepsi_out_desc}_causal_snps_info.csv"
		)
	)

	# Load variant info
	var_info = pd.read_csv(args.variant_info)[[
		'locus', 'variant_qc.AF'
	]]
	var_info['Position'] = var_info['locus'].str.split(':').apply(lambda x: x[1]).astype(int)
	var_info['p_0'] = var_info['variant_qc.AF'].str.strip('[]').str.split(',').apply(
		lambda x: float(x[0].strip())
	)
	var_info['p_1'] = var_info['variant_qc.AF'].str.strip('[]').str.split(',').apply(
		lambda x: float(x[1].strip())
	)
	var_info['2p(1-p)'] = var_info['p_0'] * var_info['p_1'] * 2
	var_info['sqrt(2p(1-p))'] = var_info['2p(1-p)'].apply(
		lambda x: math.sqrt(x)
	)

	# Join
	causal_snps = causal_snps.merge(
		var_info,
		on='Position',
		how='left',
	)

	# Rescale effect size
	causal_snps['GCTA_u'] = (
		# causal_snps['effect_size'] * causal_snps['sqrt(2p(1-p))'] * -1
		(causal_snps['effect_size'] * causal_snps['sqrt(2p(1-p))'] * -1) / 2 * 0.7763515390547042
	)

	# Output
	gcta_output = causal_snps[['ID', 'GCTA_u']]

	h = str(args.herit).split('.')[-1]
	gcta_output.to_csv(
		os.path.join(
			args.output_dir, f"{args.gepsi_out_desc}_gcta.csv"
		),
		sep='\t',
		header=False,
		index=False,
	)