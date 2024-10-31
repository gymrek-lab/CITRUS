"""Score and plot PRS predictions.

Outputs scores.json and plots.

Args:

* -v, --val-preds: Path to validation set predictions CSV file.
* -t, --test-preds: Path to test set predictions CSV file.
* -p, --pheno-file: Path to ground true phenotype file.
* --wb: Split file for white British samples.
* -o, --out-dir: Path to output directory.
"""

import argparse
import json
import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn import metrics


def parse_args():
	parser = argparse.ArgumentParser()

	parser.add_argument("-v", "--val-preds", required=True)
	parser.add_argument("-t", "--test-preds", required=True)
	parser.add_argument("-p", "--pheno-file", required=True)
	parser.add_argument("--wb", required=True)
	parser.add_argument("-o", "--out-dir", required=True)

	return parser.parse_args()


def score_and_plot_preds(
	y_true,
	y_pred,
	out_dir,
	desc=None,
	plot_prefix=''
):
	"""Score regression predictions and plot pred v true jointplot.
	
	Returns dict with the following keys:
		- mse: Mean squared error
		- r2: R-squared
		- mae: Mean absolute error
		- mape: Mean absolute percentage error
		- pearson_r: Pearson correlation coefficient
		- spearman_r: Spearman correlation coefficient		

	Args:
		y_true: Ground truth.
		y_pred: Predictions.
		desc: Description for plot title. If None, no title.
		plot_prefix: Prefix for plot filename.
	"""

	# Score predictions
	mse = metrics.mean_squared_error(y_true, y_pred)
	r2 = metrics.r2_score(y_true, y_pred)
	mae = metrics.mean_absolute_error(y_true, y_pred)
	mape = metrics.mean_absolute_percentage_error(y_true, y_pred)
	pearson_r = stats.pearsonr(y_true, y_pred).statistic	# type: ignore
	spearman_r = stats.spearmanr(y_true, y_pred).statistic	# type: ignore

	# Plot predictions vs ground truth
	g = sns.jointplot(
		x=y_true,
		y=y_pred, 
		kind='scatter', 
		joint_kws={'marker': '.', 'alpha': 0.3}
	)
	g.ax_joint.set_aspect('equal', adjustable='box')

	# Get the overall min/max of the data
	min_val = min(y_true.min(), y_pred.min())
	max_val = max(y_true.max(), y_pred.max())

	# Set the limits
	g.ax_joint.set_xlim(min_val, max_val)
	g.ax_joint.set_ylim(min_val, max_val)

	# Add dashed line for x=y
	g.ax_joint.plot([min_val, max_val], [min_val, max_val], 'k--')

	g.ax_joint.set_xlabel('True')
	g.ax_joint.set_ylabel('Predicted')
	if desc is not None:
		g.ax_joint.set_title(desc)
	else:
		g.ax_joint.set_title('Pred v True Phenotype')
	plt.tight_layout()

	# Save plot
	if plot_prefix != '':
		plot_prefix = plot_prefix + '_'
	plt.savefig(
		os.path.join(out_dir, f'{plot_prefix}jointplot.png'),
		dpi=300
	)
	plt.close()

	return {
		'mse': mse,
		'r2': r2,
		'mae': mae,
		'mape': mape,
		'pearson_r': pearson_r,
		'spearman_r': spearman_r
	}


if __name__ == '__main__':

	args = parse_args()

	# Load predictions
	val_preds = pd.read_csv(args.val_preds)
	test_preds = pd.read_csv(args.test_preds)

	# Load phenotype
	pheno = pd.read_csv(args.pheno_file, sep='\s+')
	pheno_col = pheno.columns.difference(['IID']).values[0]
	pheno = pheno.rename(columns={pheno_col: 'true'})

	# Format pheno IID
	if '_' not in str(pheno['IID'].values[0]):
		pheno['IID'] = pheno['IID'].apply(lambda x: str(x) + '_' + str(x))
	if '_' not in str(val_preds['IID'].values[0]):
		val_preds['IID'] = val_preds['IID'].apply(lambda x: str(x) + '_' + str(x))
	if '_' not in str(test_preds['IID'].values[0]):
		test_preds['IID'] = test_preds['IID'].apply(lambda x: str(x) + '_' + str(x))

	# print('pheno')
	# print(pheno)
	# print('val_preds')
	# print(val_preds)
	# print('test_preds')
	# print(test_preds)

	# Join predictions with ground truth
	val_preds = val_preds.merge(pheno, on='IID', how='inner')
	test_preds = test_preds.merge(pheno, on='IID', how='inner')

	# Load white British split
	wb_iids = pd.read_csv(args.wb, sep='\s+', header=None).values.flatten()
	wb_iids = [str(i) + '_' + str(i) for i in wb_iids]

	# print('wb_iids')
	# print(wb_iids)

	# Get pred-true sets for WB and non-WB for test set
	test_wb = test_preds[test_preds['IID'].isin(wb_iids)]
	test_nwb = test_preds[~test_preds['IID'].isin(wb_iids)]

	# Score and plot
	val_scores = score_and_plot_preds(
		val_preds['true'],
		val_preds['pred'],
		args.out_dir,
		desc='Validation',
		plot_prefix='val'
	)

	test_all_scores = score_and_plot_preds(
		test_preds['true'],
		test_preds['pred'],
		args.out_dir,
		desc='Test',
		plot_prefix='test'
	)

	test_wb_scores = score_and_plot_preds(
		test_wb['true'],
		test_wb['pred'],
		args.out_dir,
		desc='Test White British',
		plot_prefix='test_wb'
	)

	test_nwb_scores = score_and_plot_preds(
		test_nwb['true'],
		test_nwb['pred'],
		args.out_dir,
		desc='Test not White British',
		plot_prefix='test_nwb'
	)

	# Save scores
	scores = {
		'val': val_scores,
		'test': test_all_scores,
		'test_wb': test_wb_scores,
		'test_nwb': test_nwb_scores
	}

	with open(os.path.join(args.out_dir, 'scores.json'), 'w') as f:
		json.dump(scores, f, indent=4)


