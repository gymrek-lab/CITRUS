""" Input source object and nodes using the Hail engine.

Combatibile with the following file formats:
	- VCF
"""

from abc import ABC
import inspect

import numpy as np
import hail as hl

from .base_input_source import BaseInputSource
from ..data_types import Values, HaplotypeValues

class HailInputSource(BaseInputSource):
	""" Hail input source object.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)

		# Initialize matrix table
		self.hail_mt = self.load_matrix_table(input_config)

		# TODO - optionally load all node values
		# to disk: https://github.com/gymrek-lab/CITRUS/blob/main/pheno_sim/input_nodes/hail_input.py#L132

		# Set list of samples
		self.input_sample_ids = np.array(
			self.hail_mt[self.input_config['sample_id_field']].collect()
		).astype(str)

	def load_matrix_table(self, input_config):
		"""Load file as a hail MatrixTable object.

		Defines following defaults for loading:

		- 'file_format': 'vcf'
		- 'reference_genome': 'GRCh38'

		VCF specifc defaults:

		- 'force_bgz': False
		
		Args:
			input_config: The dictionary from the input section of the
				simulation config file that defines this input source.
		
		Returns:
			A hail MatrixTable object.
		"""

		# Set overall defaults
		if 'file_format' not in input_config:
			input_config['file_format'] = 'vcf'
		if 'reference_genome' not in input_config:
			input_config['reference_genome'] = 'GRCh38' # TODO seems dangerous

		# Set filetype specific defaults
		if input_config['file_format'].lower() == 'vcf':
			if 'force_bgz' not in input_config:
				input_config['force_bgz'] = False

		# Set sample field
		if 'sample_id_field' not in self.input_config:
			self.input_config['sample_id_field'] = 's'

		# Load and retrun data as a MatrixTable
		if input_config['file_format'].lower() == 'vcf':
			possible_kwargs = set(
				inspect.signature(hl.import_vcf).parameters.keys()
			).difference('path')
			return hl.import_vcf(
				input_config['file'],
				**{k: v for k, v in input_config.items() if k in possible_kwargs}
			)
		else:
			raise ValueError(
				'Invalid file format: {}'.format(input_config['file_format'])
			)

	def load_input_node(self, node_name, sample_ids=None):
		"""
		Loads data for a single input node from the 
		    source file. Optionally pass a list of sample_ids to subset and
		    reorder according to that sample list
		"""

		# Get config
		input_node_config = [item for item in self.input_config["input_nodes"] \
			if item["alias"] == node_name][0] # TODO make function

		# Subset to loci required by this input node
		required_loci = self.get_required_loci_for_node(input_node_config)

		# Get genotype data
		hap_1_rows = []
		hap_2_rows = []

		for locus in required_loci:
			# Filter to row
			row_data = self.hail_mt.filter_rows(
				(self.hail_mt.locus.contig == locus[0]) 
				& (self.hail_mt.locus.position == locus[1])
			)

			# Assert only one row
			row_count = row_data.count_rows()
			if row_count > 1:
				raise ValueError(
					f"{locus[0]}:{locus[1]} has "
					f"{row_data.count_rows()} rows. Can only have one row."
				)
			if row_count == 0:
				raise ValueError(
					f"{locus[0]}:{locus[1]} has no rows."
				)

			# Assert all calls are phased
			assert np.all(
				row_data.GT.phased.collect()
			)

			# Get values for each haplotype
			hap_1_rows.append(
				(np.array(row_data.GT[0].collect()) >= 1).astype(int)
			)
			hap_2_rows.append(
				(np.array(row_data.GT[1].collect()) >= 1).astype(int)
			)

		# If more that one locus, stack the rows and return as a tuple
		if len(required_loci) > 1:
			input_node_vals = (
				np.vstack(hap_1_rows),
				np.vstack(hap_2_rows)
			)
		else:
			input_node_vals = (
				hap_1_rows[0],
				hap_2_rows[0]
			)

		# Reorder by samples
		if sample_ids is None:
			return input_node_vals
		else:
			return self.subset_and_order_samples(input_node_vals, sample_ids)

	def get_required_loci_for_node(self, input_node_config):
		chrom = input_node_config["chr"]
		pos = input_node_config["pos"]

		# If chr is a list, pos must be a list of the same length
		if isinstance(chrom, list):
			if not isinstance(pos, list):
				raise ValueError(f"pos must be a list if chr is a list.")
			if len(chrom) != len(pos):
				raise ValueError(
					f"chr and pos must be the same length if chr is a list."
				)
			
			# Cast chr to str
			required_loci_list = list(zip(map(str, chrom), pos))
		elif isinstance(pos, list):
			required_loci_list = [(str(chrom), p) for p in pos]
		else:
			required_loci_list = [(str(chrom), pos)]
		return required_loci_list