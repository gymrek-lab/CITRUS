"""Make Manhattan and QQ plots from plink2 GLM output.

Args:
	-p, --pheno: Name of phenotype.
	-g, --gwas-out-dir: Substring after 'h' that gives heritability level.
"""

import argparse
from pprint import pprint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geneview import manhattanplot, qqplot


def parse_args():
	"""Parse command line arguments."""
	parser = argparse.ArgumentParser(
		description='Create Manhattan and QQ plots.'
	)
	parser.add_argument(
		'--herit',
		required=True,
		help='Substring after "h" that gives heritability level.'
	)
	parser.add_argument(
		'-g', '--gwas-out-dir',
		required=True,
		help='Directory with GWAS sumary stats and where plots will be saved.'
	)
	return parser.parse_args()


def prepare_data(file_path):
	"""Read and prepare summary stats."""
	df = pd.read_csv(file_path, sep='\s+')

	# Set 0 p-vals to next lowest
	low_fill_val = df[df.P != 0].P.min()
	df.loc[df.P == 0, 'P'] = low_fill_val

	# Bonferroni correct p-values
	df['P_bonf'] = df['P'] * len(df)
	df['P_bonf'] = df['P_bonf'].clip(upper=1.0)

	return df


if __name__ == '__main__':
	# main()

	# Read args
	args = parse_args()
	print('Args:', flush=True)
	pprint(vars(args))

	# Read summary stats
	citrus_ss = prepare_data(
		f"{args.gwas_out_dir}/gepsi_lin_add_h{args.herit}_h{args.herit}.phenotype.glm.linear"
	)
	gepsi_ss = prepare_data(
		f"{args.gwas_out_dir}/gepsi_lin_add_h{args.herit}.phenotype.glm.linear"
	)
	gcta_ss = prepare_data(
		f"{args.gwas_out_dir}/gepsi_lin_add_h{args.herit}_gcta.phenotype.glm.linear"
	)

	# Create Manhattan plot figure
	herit_str = 1.0 if args.herit == 'FULL' else '0.' + args.herit

	fig, axs = plt.subplots(
		nrows=3, 
		ncols=1,
		figsize=(10, 15),
		sharex=True,
		sharey=True,
	)
	fig.suptitle(f'Linear-additive (H^2={herit_str}) Manhattan Plots', fontsize=16)

	# CITRUS Manhattan Plot
	manhattanplot(data=citrus_ss, pv="P_bonf", CHR="19", xlabel="Chromosome 19", ax=axs[0])
	axs[0].set_title('CITRUS Manhattan Plot')

	# GEPSi Manhattan Plot
	manhattanplot(data=gepsi_ss, pv="P_bonf", CHR="19", xlabel="Chromosome 19", ax=axs[1])
	axs[1].set_title('GEPSi Manhattan Plot')

	# GCTA Manhattan Plot
	manhattanplot(data=gcta_ss, pv="P_bonf", CHR="19", xlabel="Chromosome 19", ax=axs[2])
	axs[2].set_title('GCTA Manhattan Plot')

	plt.tight_layout(rect=[0, 0.03, 1, 0.97])
	plt.savefig(f"{args.gwas_out_dir}/all_lin_add_h{args.herit}_manhattan_plots.png", dpi=400)
	plt.close()

	# Create QQ plot figure
	fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(5, 15), sharex=True)
	fig.suptitle(f'Linear-additive (H^2={herit_str}) QQ Plots', fontsize=16)

	# CITRUS QQ Plot
	qqplot(data=citrus_ss["P_bonf"], ax=axs[0])
	axs[0].set_title('CITRUS QQ Plot')

	# GEPSi QQ Plot
	qqplot(data=gepsi_ss["P_bonf"], ax=axs[1])
	axs[1].set_title('GEPSi QQ Plot')

	# GCTA QQ Plot
	qqplot(data=gcta_ss["P_bonf"], ax=axs[2])
	axs[2].set_title('GCTA QQ Plot')

	plt.tight_layout(rect=[0, 0.03, 1, 0.97])
	plt.savefig(f"{args.gwas_out_dir}/all_lin_add_h{args.herit}_qq_plots.png", dpi=400)
	plt.close()