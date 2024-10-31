"""Make Manhattan and QQ plots from plink2 GLM output.

Args:
	-p, --pheno: Name of phenotype.
	-g, --gwas-out-dir: Directory with GWAS sumary stats and where plots will
		be saved.
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
		'-p', '--pheno',
		required=True,
		help='Name of phenotype.'
	)
	parser.add_argument(
		'-g', '--gwas-out-dir',
		required=True,
		help='Directory with GWAS sumary stats and where plots will be saved.'
	)
	return parser.parse_args()


if __name__ == '__main__':
	# main()

	# Read args
	args = parse_args()
	print('Args:', flush=True)
	pprint(vars(args))

	# Read summary stats
	ss_df = pd.read_csv(
		f"{args.gwas_out_dir}/{args.pheno}.phenotype.glm.linear",
		sep='\s+'
	)

	# Set 0 p-vals to next lowest
	low_fill_val = ss_df[ss_df.P != 0].P.min()
	ss_df.loc[ss_df.P == 0, 'P'] = low_fill_val

	# Bonferonni correct p-values
	n_tests = len(ss_df)
	print(n_tests)
	ss_df['P_bonf'] = ss_df['P'] * n_tests
	ss_df['P_bonf'] = ss_df['P_bonf'].clip(upper=1.0)

	print(ss_df.P_bonf.min())
	print(-np.log10(ss_df.P_bonf.min()))

	# Plot Manhattan
	ax = manhattanplot(
		data=ss_df,
		pv="P",
		CHR="19",
		xlabel="Chromosome 19"
	)
	plt.title(f"{args.pheno} Manhattan Plot")
	plt.savefig(
		f"{args.gwas_out_dir}/{args.pheno}_manhattan.png",
		dpi=400
	)

	# Plot QQ
	ax = qqplot(
		data=ss_df["P"]
	)
	plt.savefig(
		f"{args.gwas_out_dir}/{args.pheno}_qq.png",
		dpi=400
	)