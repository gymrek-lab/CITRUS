import json
import os
from itertools import product

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


if __name__ == '__main__':

	citrus_pheno_dir = '../../pheno_sim/citrus_phenos'
	gepsi_pheno_dir = '../../output/gepsi_phenos'
	gcta_pheno_dir = '../../output/gcta_phenos'

	results_dir = '../../output'
	pheno_name = 'phenotype'

	pheno_h2_fnames = (	# CITRUS, GEPSi, GCTA
		'gepsi_lin_add_h5_h5',
		'gepsi_lin_add_h5',
		'gepsi_lin_add_h5_gcta'
	)
	pheno_hfull_fnames = (
		'gepsi_lin_add_hFULL_hFULL',
		'gepsi_lin_add_hFULL',
		'gepsi_lin_add_hFULL_gcta'
	)

	# Load pheno data
	citrus_h2 = pd.read_csv(
		os.path.join(citrus_pheno_dir, pheno_h2_fnames[0] + '.pheno'),
		sep='\s+'
	)
	citrus_hfull = pd.read_csv(
		os.path.join(citrus_pheno_dir, pheno_hfull_fnames[0] + '.pheno'),
		sep='\s+'
	)
	gepsi_h2 = pd.read_csv(
		os.path.join(gepsi_pheno_dir, pheno_h2_fnames[1] + '.pheno'),
		sep='\s+'
	)
	gepsi_hfull = pd.read_csv(
		os.path.join(gepsi_pheno_dir, pheno_hfull_fnames[1] + '.pheno'),
		sep='\s+'
	)
	gcta_h2 = pd.read_csv(
		os.path.join(gcta_pheno_dir, pheno_h2_fnames[2] + '.pheno'),
		sep='\s+'
	)
	gcta_hfull = pd.read_csv(
		os.path.join(gcta_pheno_dir, pheno_hfull_fnames[2] + '.pheno'),
		sep='\s+'
	)

	# Join h2 and hfull for CITRUS and GEPSi on 'FID' and 'IID'. Suffix 
	# columns with CITRUS/GEPSI
	sim_h2 = citrus_h2.merge(
		gepsi_h2, on=['FID', 'IID'], suffixes=('_citrus', '_gepsi')
	)
	sim_h2 = sim_h2.merge(
		gcta_h2, on=['FID', 'IID'], suffixes=('', '_gcta')
	)
	sim_h2 = sim_h2.rename(columns={'phenotype': 'phenotype_gcta'})
	print(sim_h2.head())

	sim_hfull = citrus_hfull.merge(
		gepsi_hfull, on=['FID', 'IID'], suffixes=('_citrus', '_gepsi')
	)
	sim_hfull = sim_hfull.merge(
		gcta_hfull, on=['FID', 'IID'], suffixes=('', '_gcta')
	)
	sim_hfull = sim_hfull.rename(columns={'phenotype': 'phenotype_gcta'})
	print(sim_hfull.head())


	# Plot h2 and hfull as side by side scatter plots pf phenotype_citrus vs
	# phenotype_gepsi
	alpha = 0.5

	fig, ax = plt.subplots(1, 2, figsize=(12, 6))
	g = sns.scatterplot(
		x='phenotype_gepsi',
		y='phenotype_citrus',
		data=sim_h2,
		alpha=alpha,
		ax=ax[0]
	)
	g.set_title('Heritability = 0.5')
	ax[0].set_aspect('equal', adjustable='datalim')

	g = sns.scatterplot(
		x='phenotype_gepsi',
		y='phenotype_citrus',
		data=sim_hfull,
		alpha=alpha,
		ax=ax[1]
	)
	g.set_title('Heritability = 1.0')
	ax[1].set_aspect('equal', adjustable='datalim')

	fig.suptitle('CITRUS vs GEPSi Phenotypes')
	plt.tight_layout()
	plt.savefig(
		'citrus_vs_gepsi_pheno.png',
		dpi=600
	)
	plt.close()

	same_vals = np.isclose(
		sim_hfull['phenotype_citrus'],
		sim_hfull['phenotype_gepsi'],
		rtol=1e-5,
		atol=0.0
	)
	print(np.sum(same_vals))
	print(len(same_vals))
	print(np.sum(same_vals)/len(same_vals))
	print(sim_hfull.loc[~same_vals])
	print(np.all(
		sim_hfull.loc[~same_vals]['IID'].astype(str).str.contains('-')
	))

	# Plot h2 and hfull as side by side scatter plots pf phenotype_citrus vs
	# phenotype_gcta
	fig, ax = plt.subplots(1, 2, figsize=(12, 6))
	g = sns.scatterplot(
		x='phenotype_gcta',
		y='phenotype_citrus',
		data=sim_h2,
		alpha=alpha,
		ax=ax[0]
	)
	g.set_title('Heritability = 0.5')
	ax[0].set_aspect('equal', adjustable='datalim')

	g = sns.scatterplot(
		x='phenotype_gcta',
		y='phenotype_citrus',
		data=sim_hfull,
		alpha=alpha,
		ax=ax[1]
	)
	g.set_title('Heritability = 1.0')
	ax[1].set_aspect('equal', adjustable='datalim')

	fig.suptitle('CITRUS vs GCTA Phenotypes')
	plt.tight_layout()
	plt.savefig(
		'citrus_vs_gcta_pheno.png',
		dpi=600
	)
	plt.close()

	same_vals = np.isclose(
		sim_hfull['phenotype_citrus'],
		sim_hfull['phenotype_gcta'],
		rtol=1e-5,
		atol=0.0
	)
	print(np.sum(same_vals))
	print(len(same_vals))
	print(np.sum(same_vals)/len(same_vals))
	
	# Plot h2 and hfull as side by side scatter plots pf phenotype_gepsi vs
	# phenotype_gcta
	fig, ax = plt.subplots(1, 2, figsize=(12, 6))
	g = sns.scatterplot(
		x='phenotype_gcta',
		y='phenotype_gepsi',
		data=sim_h2,
		alpha=alpha,
		ax=ax[0]
	)
	g.set_title('Heritability = 0.5')
	ax[0].set_aspect('equal', adjustable='datalim')

	g = sns.scatterplot(
		x='phenotype_gcta',
		y='phenotype_gepsi',
		data=sim_hfull,
		alpha=alpha,
		ax=ax[1]
	)
	g.set_title('Heritability = 1.0')
	ax[1].set_aspect('equal', adjustable='datalim')

	fig.suptitle('GEPSi vs GCTA Phenotypes')
	plt.tight_layout()
	plt.savefig(
		'gepsi_vs_gcta_pheno.png',
		dpi=600
	)
	plt.close()

	same_vals = np.isclose(
		sim_hfull['phenotype_gepsi'],
		sim_hfull['phenotype_gcta'],
		rtol=1e-5,
		atol=0.0
	)
	print(np.sum(same_vals))
	print(len(same_vals))
	print(np.sum(same_vals)/len(same_vals))
	