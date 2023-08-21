"""Utility functions related to variants/genes in source data files."""

import hail as hl
import pandas as pd

from pheno_sim.input_nodes import HailInputSource


class InputVariantInfo:
	"""For getting information about variants in the input files.
	
	Args:
		input_config (dict): 'input' key from a simulation config
	"""

	def __init__(
		self,
		input_config,
		compute_variant_info=True,
	):
		self.input_config = input_config

		# Get reference genome
		if 'reference_genome' in input_config[0]:
			self.reference_genome = input_config[0]['reference_genome']
		else:
			self.reference_genome = 'GRCh38'

		# Load all input sources with Hail
		all_mts = [
			HailInputSource.load_matrix_table(conf) for conf in input_config
		]
		
		if len(all_mts) == 1:
			var_data = all_mts[0]
		else:
			var_data = all_mts[0].union_rows(*all_mts[1:])
		
		# Compute variant info (optional)
		if compute_variant_info:
			var_data = hl.variant_qc(var_data)

		# Drop entries
		self.var_data = var_data.rows().persist()

	def get_variants_in_interval(self, intervals):
		"""Get variants in input data in genomic interval(s)
		
		Args:
			intervals (str or list of str): Genomic interval(s) in format
				'chr:start-end'. See
				hail.is/docs/0.2/functions/genetics.html#hail.expr.functions.parse_locus_interval
		
		Returns:
			hail.Table: Variants in the interval
		"""
		if isinstance(intervals, str):
			intervals = [intervals]
		intervals = [hl.parse_locus_interval(x) for x in intervals]
		return hl.filter_intervals(self.var_data, intervals).to_pandas()
