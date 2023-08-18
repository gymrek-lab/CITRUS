"""
Estimates broad-sense (H^2) and narrow-sense (h^2) heritability
for a given phenotype simulation.
"""

import copy

import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn import linear_model
from sklearn import model_selection
from tqdm.autonotebook import tqdm, trange


def sample_vals_dict(vals_dict, n_samples=1.0):
	"""Subsample individuals in vals dict.
	
	If n_samples is less than 1, will use that fraction of samples. If
	n_samples is greater than 1, will use that number of samples. If 
	n_samples is 1 (default), will return the same vals dict.
	
	Args:
		vals (dict): Dictionary of values.
		n_samples (default 1.0): The fraction or number of samples to
			use when estimating heritability. If value is less than or
			equal to 1, will use that fraction of samples. If value is
			greater than 1, will use that number of samples. Samples
			will be randomly selected from the input samples.
	"""
	vals_dict = copy.deepcopy(vals_dict)
	
	# Get number of sample in input.
	input_item = vals_dict[list(vals_dict.keys())[0]]
	if isinstance(input_item, tuple):
		n_input_samples = input_item[0].shape[-1]
	else:
		n_input_samples = input_item.shape[-1]

	# Shuffle and possibly subsample input data
	if n_samples > 1:
		selected_idx = np.random.choice(
			n_input_samples,
			n_samples,
			replace=False
		)
		
		for key, val in vals_dict.items():
			if isinstance(val, tuple):
				vals_dict[key] = (
					val[0][..., selected_idx], val[1][..., selected_idx]
				)
			else:
				vals_dict[key] = val[..., selected_idx]
	elif n_samples < 1:
		selected_idx = np.random.choice(
			n_input_samples,
			int(n_samples * n_input_samples),
			replace=False
		)
		
		for key, val in vals_dict.items():
			if isinstance(val, tuple):
				vals_dict[key] = (
					val[0][..., selected_idx], val[1][..., selected_idx]
				)
			else:
				vals_dict[key] = val[..., selected_idx]

	return vals_dict


def sum_dataframe_haplotypes(vals_df):
	"""Sum haplotype values in a vals_dict type DataFrame into single cols."""
	vals_df = vals_df.copy()
	
	collapsed_name_map = {}
	
	for col in vals_df.columns:
		col_name_parts = col.split('*-*')
		key = col_name_parts[0]

		if len(col_name_parts) == 1:
			collapsed_name_map[key] = [col]
		elif len(col_name_parts) == 2:
			if col_name_parts[1] == 'a' or col_name_parts[1] == 'b':
				if key not in collapsed_name_map:
					collapsed_name_map[key] = []
				collapsed_name_map[key].append(col)
			else:
				key = col
				collapsed_name_map[key] = [col]
		elif len(col_name_parts) == 3:
			if col_name_parts[1] == 'a' or col_name_parts[1] == 'b':
				key = col_name_parts[0] + '*-*' + col_name_parts[2]
				if key not in collapsed_name_map:
					collapsed_name_map[key] = []
				collapsed_name_map[key].append(col)
			else:
				raise ValueError(
					'Invalid column name: {}'.format(col)
				)
		else:
			raise ValueError(
				'Invalid column name: {}'.format(col)
			)

	# Collapse haplotypes
	for key, cols in collapsed_name_map.items():
		if len(cols) > 1:
			vals_df[key] = vals_df[cols].sum(axis=1)
			vals_df = vals_df.drop(columns=cols)

	return vals_df


def narrow_sense_heritability(
	sim,
	input_vals=None,
	n_samples=1.0,
	n_pheno_per_geno=100,
	n_folds=5,
	n_iterations=5,
	statistic_fn=np.mean,
	confidence_level=0.95,
	phenotype_alias='phenotype'
):
	"""Estimates simulation's narrow-sense heritability for a given simulation.
	
	Estimates narrow-sense heritability (h^2) for a given simulation by
	fitting a linear regression model (that models the additive genetic 
	effect on the phenotype). The model is fit using the genotypes with
	haplotypes summed as the input features and simulated phenotypes
	as the label.

	For each of 'n_iterations' iterations the following procedure is
	followed:

		1. Randomly sample 'n_samples' fraction/number of individuals
			from the input data.
		2. For each individual, simulate 'n_pheno_per_geno' phenotypes.
		3. Split the (genotype, simulated phenotype) pairs into 'n_folds'
			folds, such that each genotype is in exactly one fold. This
			prevents a genotype from being in the training and testing
			data.
		4. For each fold, fit the model on the training data and compute
			the model's R^2 score on the test data.
		5. Add the R^2 score to a list

	The list of R^2 scores is effectively a list of h^2 estimates for
	the given simulation (see narrow sense heritability estimation example
	notebook). An overall statistic (typically mean or median) defined
	by 'statistic_fn' is computed from the list of R^2 scores, as well
	as a bootstrap confidence interval. The confidence interval is
	computed using the 'confidence_level' parameter.

	Args:
		sim (PhenoSimulation): The simulation to estimate narrow-sense
			heritability for.
		input_vals (default None): A ValuesDict containing the input
				values. If None, will run the input step of the simulation.
		n_samples (default 1.0): The fraction or number of samples to
			use when estimating heritability. If value is less than or
			equal to 1, will use that fraction of samples. If value is
			greater than 1, will use that number of samples. Samples
			will be randomly selected from the input samples.
		n_pheno_per_geno (default 100): The number of phenotypes to
			simulate per genotype each iteration.
		n_folds (default 5): The number of folds to divide the simulated
			phenotypes into each iteration. Each genotype will be in
			exactly one fold.
		n_iterations (default 5): The number of times to repeat the
			procedure of sampling individuals, simulating phenotypes,
			and computing the R^2 scores.
		statistic_fn (default np.mean): The statistic to compute from
			the list of R^2 scores. Typically np.mean or np.median.
		confidence_level (default 0.95): The confidence level to use
			when computing the bootstrap confidence interval.
		phenotype_alias (default 'phenotype'): Output phenotype alias
			in simulation.

	Returns:
		Dict with keys:
			- 'h2': The estimated narrow-sense heritability.
			- 'h2_ci_lower': The lower bound of the bootstrap confidence
				interval.
			- 'h2_ci_upper': The upper bound of the bootstrap confidence
				interval.
	"""

	# Get input genotype values.
	if input_vals is None:
		input_vals = sim.run_input_step()

	# Run iterations of the procedure.
	r2_scores = []

	for i in trange(n_iterations):
		# Subsample individuals if n_samples is not 1
		iter_input_vals = sample_vals_dict(input_vals, n_samples)

		# Simulate phenotypes to create labels, tracking genotype
		pheno_vals = []
		geno_idx = []

		for i in range(n_pheno_per_geno):
			gen_phenos = sim.run_simulation_steps(
				copy.deepcopy(iter_input_vals)
			)[phenotype_alias]

			pheno_vals.extend(gen_phenos)
			geno_idx.extend(list(range(len(gen_phenos))))

		# Convert input values to a dataframe and stack to match n_pheno_per_geno
		input_df = sim.vals_dict_to_dataframe(iter_input_vals)
		input_df = sum_dataframe_haplotypes(
			pd.concat([input_df] * n_pheno_per_geno)
		)

		# Create model and cross validation object
		linear_reg = linear_model.LinearRegression(n_jobs=-1)
		strat_group_kfold = model_selection.GroupKFold(
			n_splits=n_folds
		)

		# Get R^2 scores for each fold
		r2_scores.extend(
			model_selection.cross_val_score(
				linear_reg,
				X=input_df,
				y=pheno_vals,
				groups=geno_idx,
				scoring='r2',
				cv=strat_group_kfold,
				n_jobs=-1,
			)
		)

	# Compute bootstrapped confidence intervals
	ci = stats.bootstrap(
		(r2_scores,), 
		statistic_fn,
		confidence_level=confidence_level,
	)

	# Return results
	return {
		'h2': statistic_fn(r2_scores),
		'h2_ci_lower': ci.confidence_interval.low,
		'h2_ci_upper': ci.confidence_interval.high,
	}


def broad_sense_heritability(
	sim,
	input_vals=None,
	n_samples=1.0,
	n_pheno_per_geno=250,
	n_iterations=10,
	statistic_fn=np.mean,
	confidence_level=0.95,
	phenotype_alias='phenotype'
):
	"""Estimates simulation's broad-sense heritability for a given simulation.
	
	See broad sense heritability estimation example notebook for more details
	on the procedure.

	Args:
		sim (PhenoSimulation): The simulation to estimate narrow-sense
			heritability for.
		input_vals (default None): A ValuesDict containing the input
				values. If None, will run the input step of the simulation.
		n_samples (default 1.0): The fraction or number of samples to
			use when estimating heritability. If value is less than or
			equal to 1, will use that fraction of samples. If value is
			greater than 1, will use that number of samples. Samples
			will be randomly selected from the input samples.
		n_pheno_per_geno (default 250): The number of phenotypes to
			simulate per genotype each iteration.
		n_folds (default 5): The number of folds to divide the simulated
			phenotypes into each iteration. Each genotype will be in
			exactly one fold.
		n_iterations (default 5): The number of times to repeat the
			procedure of sampling individuals, simulating phenotypes,
			and computing the R^2 scores.
		statistic_fn (default np.mean): The statistic to compute from
			the list of R^2 scores. Typically np.mean or np.median.
		confidence_level (default 0.95): The confidence level to use
			when computing the bootstrap confidence interval.
		phenotype_alias (default 'phenotype'): Output phenotype alias
			in simulation.

	Returns:
		Dict with keys:
			- 'H2': The estimated broad-sense heritability.
			- 'H2_ci_lower': The lower bound of the bootstrap confidence
				interval.
			- 'H2_ci_upper': The upper bound of the bootstrap confidence
				interval.
	"""

	assert n_pheno_per_geno > 1, 'n_pheno_per_geno must be greater than 1'

	# Get input genotype values.
	if input_vals is None:
		input_vals = sim.run_input_step()

	# Run iterations of the procedure.
	H2_vals = []

	for i in trange(n_iterations):
		# Subsample individuals if n_samples is not 1
		iter_input_vals = sample_vals_dict(input_vals, n_samples)

		# Step 1: Simulate for each genotype n_pheno_per_geno times
		pheno_vals = []

		for i in range(n_pheno_per_geno):
			pheno_vals.append(
				sim.run_simulation_steps(
					copy.deepcopy(iter_input_vals)
				)[phenotype_alias]
			)

		# Convert to matrix where columns are samples and rows are replicates
		pheno_vals = np.vstack(pheno_vals).astype(float)

		# Step 2: Compute total variance
		total_var = np.var(pheno_vals)

		# Step 3: Compute E[Var(E)] with average intra-genotype variance
		intra_geno_var = np.var(pheno_vals, axis=0).mean()

		# Step 4: Compute inter-genotype variance (the variance of the mean
		# phenotype for each genotype).
		var_g = total_var - intra_geno_var

		# Step 5: Compute broad-sense heritability
		H2_vals.append(var_g / total_var)

	# Compute bootstrapped confidence intervals
	ci = stats.bootstrap(
		(H2_vals,),
		statistic_fn,
		confidence_level=confidence_level,
	)

	# Return results
	return {
		'H2': statistic_fn(H2_vals),
		'H2_ci_lower': ci.confidence_interval.low,
		'H2_ci_upper': ci.confidence_interval.high,
	}
