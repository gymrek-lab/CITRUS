""" Input source object and nodes using the Hail engine.

Combatibile with the following file formats:
	- VCF
"""

import numpy as np
import hail as hl

from .base_input_source import BaseInputSource
from ..data_types import Values, HaplotypeValues
from ...utils import MSG

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

	def check_input_config(self):
		for req_key in ['file_format','reference_genome','force_bgz']:
			if req_key not in self.input_config.keys():
				raise KeyError("Missing key {} in hail config".format(req_key))

	def load_matrix_table(self, input_config):
		"""Load file as a hail MatrixTable object.
		Args:
			input_config: The dictionary from the input section of the
				simulation config file that defines this input source.
		
		Returns:
			A hail MatrixTable object.
		"""
		# Set sample field
		if 'sample_id_field' not in self.input_config:
			self.input_config['sample_id_field'] = 's'

		# Load and retrun data as a MatrixTable
		if input_config['file_format'].lower() == 'vcf':
			return hl.import_vcf(
				input_config['file'],
				reference_genome = input_config["reference_genome"],
				force_bgz = input_config["force_bgz"]
			)
		else:
			raise ValueError(
				'Unsupported file format: {}'.format(input_config['file_format'])
			)

	def load_input_node(self, node_name, sample_ids=None):
		"""
		Loads data for a single input node from the 
		    source file. Optionally pass a list of sample_ids to subset and
		    reorder according to that sample list
		"""

		# Get config
		if node_name not in self.node_configs.keys():
			raise ValueError('Could not load non-existent node {}'.format(node_name))
		input_node_config = self.node_configs[node_name]

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