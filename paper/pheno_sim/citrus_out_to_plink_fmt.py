"""Convert CITRUS output CSV to plink phenotype file format.

Example output:

	#IID	gene1	phenotype
	1110	23.31	22.22
	2202	34.12	18.23
	...
	
"""

import os

import pandas as pd

# # Write a function to replace main
# def citrus_out_to_plink_phenotype(
# 	sample_id_col=''
# )

import argparse


if __name__ == "__main__":
	
	# args
	parser = argparse.ArgumentParser()

	parser.add_argument("desc")

	args = parser.parse_args()

	sample_id_col = 'sample_id'

	pheno_cols = ['phenotype']

	csv_path = f'citrus_output/{args.desc}.csv'
	output_path = f'citrus_phenos/{args.desc}.pheno'

	# function
	df = pd.read_csv(
		csv_path,
		index_col=False
	)

	df = df[[sample_id_col] + pheno_cols]
	
	# Split FID and IID
	df['FID'] = df[sample_id_col].str.split('_').map(lambda x: x[0])
	df['IID'] = df[sample_id_col].str.split('_').map(lambda x: x[1])

	df[['FID', 'IID'] + pheno_cols].to_csv(
		output_path,
		sep='\t',
		index=False
	)


