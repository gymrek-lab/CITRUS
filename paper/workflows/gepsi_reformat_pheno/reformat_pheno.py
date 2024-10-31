"""Reformat GEPSi output to .pheno file.

Args:
	-g, --gepsi-out-dir: Directory containing GEPSi output files.
	-d, --gepsi-out-desc: Description part of GEPSi output file names.
	-o, --output-dir: Directory to write .pheno files to.
	-p, --pheno-file: Name of .pheno file to write to.
	-s, --snplist-file: Path of CSV file containing SNP list.
	-samp, --sample-file: Header then one ID per line, in the same order
		as the phenotype file.
"""

import argparse
import pickle
import os

import pandas as pd


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", "--gepsi-out-dir", required=True)
	parser.add_argument("-d", "--gepsi-out-desc", required=True)
	parser.add_argument("-o", "--output-dir", required=True)
	parser.add_argument("-p", "--pheno-file", required=True)
	parser.add_argument("-s", "--snplist-file", required=True)
	parser.add_argument("-samp", "--sample-file", required=True)
	return parser.parse_args()


if __name__ == '__main__':

	args = parse_args()

	# Load GEPSi output pickle files
	gene_fname = f"causal_genes_{args.gepsi_out_desc}_phenotype.pkl"
	snp_idx_fname = f"causal_snp_idx_{args.gepsi_out_desc}_phenotype.pkl"
	effect_size_fname = f"effect_size_{args.gepsi_out_desc}_phenotype.pkl"
	pheno_fname = f"phenotype_{args.gepsi_out_desc}_phenotype.pkl"

	with open(os.path.join(args.gepsi_out_dir, gene_fname), 'rb') as f:
		gene_data = pickle.load(f)
	with open(os.path.join(args.gepsi_out_dir, snp_idx_fname), 'rb') as f:
		snp_idx_data = pickle.load(f)
	with open(os.path.join(args.gepsi_out_dir, effect_size_fname), 'rb') as f:
		effect_size_data = pickle.load(f)
	with open(os.path.join(args.gepsi_out_dir, pheno_fname), 'rb') as f:
		pheno_data = pickle.load(f)

	# Load SNP list
	snp_df = pd.read_csv(args.snplist_file, sep='\s+')

	# Load sample list
	sample_df = pd.read_csv(args.sample_file)

	# Create pheno file
	sample_df['IID'] = sample_df['IID'].str.split('_').apply(lambda x: x[0])

	pheno_df = pd.DataFrame({
		'FID': sample_df['IID'].values,
		'IID': sample_df['IID'].values,
		'phenotype': pheno_data
	})

	pheno_df.to_csv(
		os.path.join(args.output_dir, args.pheno_file + '.pheno'),
		sep='\t',
		index=False
	)

	# Get causal SNPs and weights
	snp_df = snp_df.loc[list(snp_idx_data.keys())]

	effect_sizes = [
		effect_size_data[idx][1] for idx in snp_idx_data.keys()
	]

	snp_df['effect_size'] = effect_sizes

	snp_df.to_csv(
		os.path.join(args.output_dir, args.pheno_file + '_causal_snps_info.csv'),
		index=False
	)

	g='../../output/gepsi_sim_out/lin_add_h2'
	d='chr19_None'
	s='../../output/gepsi_fmt_data/snplist_chr19_None.csv'
	samp='../../output/gepsi_fmt_data/sample_ids.txt'