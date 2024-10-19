""" Input source object and nodes using the Hail engine.

Includes following input nodes types:
	- SNP
	
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

	Attributes:
		input_config: The dictionary from the input section of the simulation
			config file that defines this input source. Input sources with
			random selection update this to what is selected for
			reproducibility.
		input_nodes: A list of input nodes that use the input source.
		input_sample_ids: A list of sample ids from the input source.

	Input config keys:
		file: Path to the VCF file, hadoop glob pattern, or list of paths
			to VCF files.
		file_format: The file format of the input file(s). Defaults to 'vcf'.
			Must be one of 'vcf' (TODO add more).
		input_nodes: A list of dictionaries defining the input nodes that use
			this input source. See input_nodes_README.md for more details.
		force_bgz: If True, forces hail to read the input file(s) as bgzipped
			files despite thier extension. Defaults to False.
		reference_genome: The reference genome to use. Defaults to 'GRCh38'.
		sample_id_field: The name of the sample ID field in the file(s).
			Defaults to 's'.

	Methods:
		__init__(input_config): Constructor. Ignores the 'engine' key in the
			input_source_config dictionary and uses hail.
		load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		subset_and_order_samples(sample_ids): See BaseInputSource.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)

		# Create input nodes
		self.input_nodes = []

		for input_node_config in self.input_config['input_nodes']:
			self.input_nodes.append(
				BaseHailInputNode.create_input_node(input_node_config)
			)

	@staticmethod
	def load_matrix_table(input_config):
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
			input_config['reference_genome'] = 'GRCh38'

		# Set filetype specific defaults
		if input_config['file_format'].lower() == 'vcf':
			if 'force_bgz' not in input_config:
				input_config['force_bgz'] = False

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

	def load_inputs(self):
		"""Loads the input data from the source file and sets the input_nodes
		and input_sample_ids attributes.
		"""
		geno_data = self.load_matrix_table(self.input_config)

		if 'sample_id_field' not in self.input_config:
			self.input_config['sample_id_field'] = 's'
		
		# Subset to loci required by input nodes
		required_loci = []
		for input_node in self.input_nodes:
			required_loci.extend(input_node.get_required_loci())

		required_set = hl.literal(set(required_loci))

		geno_data = geno_data.filter_rows(
			required_set.contains(
				hl.tuple([
					hl.str(geno_data.locus.contig), 
					geno_data.locus.position
				])
			)
		).persist()

		# Get sample ids
		self.input_sample_ids = np.array(
			geno_data[self.input_config['sample_id_field']].collect()
		).astype(str)

		# Get input node values
		input_node_vals = dict()

		for input_node in self.input_nodes:
			input_node_vals[input_node.alias] = input_node.get_node_values(
				geno_data
			)

		return input_node_vals


class BaseHailInputNode(ABC):
	""" Base input node class.

	Attributes:
		alias: The alias of the input node.
		
	Methods:
		__init__(alias, **kwargs): Constructor.
		required_loci(): Returns a list of the required loci for this
			input node. Used by the HailInputSource object to load subset
			of the input data.
		get_node_values(geno_data): Returns the input node values
			from the geno_data hail MatrixTable object.

	Class methods:
		create_input_node(input_node_config): Returns an input node object
			given a dictionary defining the input node. This function
			will return the proper subclass of BaseHailInputNode initialized
			with the key-value pairs from the input_node_config dictionary
			(except for the 'type' key) as its keyword arguments.
	"""

	def __init__(self, alias, **kwargs):
		self.alias = alias

	def get_required_loci(self):
		""" Returns a list of the required loci for this input node. Used by
		the HailInputSource object to load subset of the input data.
		"""
		pass

	def get_node_values(self, geno_data):
		""" Returns the input node values from the geno_data hail
		MatrixTable object.
		"""
		pass

	@classmethod
	def create_input_node(cls, input_node_config):
		""" Returns an input node object given a dictionary defining the
		input node. This function will return the proper subclass of
		BaseHailInputNode initialized with the key-value pairs from the
		input_node_config dictionary (except for the 'type' key) as its
		keyword arguments.

		Currently supported input node types (case insensitive):
			- 'SNP'
		"""
		input_node_config = input_node_config.copy()
		
		input_node_type = input_node_config.pop('type').lower()

		if input_node_type == 'snp':
			return SNPInputNode(**input_node_config)
		else:
			raise ValueError(f"Invalid input node type: {input_node_type}")


class SNPInputNode(BaseHailInputNode):
	""" Class defining SNP(s) from a file loaded with Hail that will
	be part of one input node.

	See BaseHailInputNode.

	Attributes:
		alias: The alias of the input node.
		required_loci_list: A list of tuples of (chromosome (str), position
			(int)) representing the required loci for this input node.

	Args:
		alias: The alias of the input node.
		chr: The chromosome of the SNP(s). May be a string or integer 
			representing a single chromosome all positions in 'pos' are on,
			or a list of strings or integers representing multiple
			chromosomes. If a list, the length of the list must be the same
			as the length of 'pos'.
		pos: The position(s) of the SNP(s). May either be:
			- An integer representing a single position on 'chr'.
			- A list of integers representing multiple positions on 'chr'
				if 'chr' is a single chromosome.
			- A list of integers the same length as 'chr' if 'chr' is a list
				of chromosomes, such that each position in 'pos' is on the
				corresponding chromosome in 'chr'.
	"""

	def __init__(self, alias, chr, pos):
		super().__init__(alias)
		
		# Set attribute of position(s) required for this input node as a list
		# of tuples of (chromosome (str), position (int)).

		# If chr is a list, pos must be a list of the same length
		if isinstance(chr, list):
			if not isinstance(pos, list):
				raise ValueError(f"pos must be a list if chr is a list.")
			if len(chr) != len(pos):
				raise ValueError(
					f"chr and pos must be the same length if chr is a list."
				)
			
			# Cast chr to str
			self.required_loci_list = list(zip(map(str, chr), pos))
		elif isinstance(pos, list):
			self.required_loci_list = [(str(chr), p) for p in pos]
		else:
			self.required_loci_list = [(str(chr), pos)]

	def get_required_loci(self):
		""" Returns a list of the required loci for this input node. Used by
		the HailInputSource object to load subset of the input data.
		"""
		return self.required_loci_list
	
	def get_node_values(self, geno_data) -> HaplotypeValues:
		""" Get values for the input node from the geno_data MatrixTable.

		Args:
			geno_data: The (optimally filtered and persisted) geno_data
				MatrixTable object.

		Returns:
			HaplotypeValues object containing the values for the input node.
			HaplotypeValues are length 2 tuples of numpy arrays.
		"""

		hap_1_rows = []
		hap_2_rows = []

		for locus in self.required_loci_list:
			# Filter to row
			row_data = geno_data.filter_rows(
				(geno_data.locus.contig == locus[0]) 
				& (geno_data.locus.position == locus[1])
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
		if len(self.required_loci_list) > 1:
			return (
				np.vstack(hap_1_rows),
				np.vstack(hap_2_rows)
			)
		else:
			return (
				hap_1_rows[0],
				hap_2_rows[0]
			)


if __name__ == '__main__':

	# For testing
	sim_config = {
		"input": [
			{
				"file": "../../pheno_sim_demos/1000_genomes_data/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
				"file_format": "vcf",
				"reference_genome": "GRCh37",
				"force_bgz": True,
				"input_nodes": [
					{
						"alias": "LDLR_upstream_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11197261
					},
					{
						"alias": "LDLR_intron_A_variants",
						"type": "SNP",
						"chr": "19",
						"pos": [11202306, 11206575]
					},
					{
						"alias": "LDLR_intron_B_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11216561
					},
					{
						"alias": "LDLR_missense_variants",
						"type": "SNP",
						"chr": "19",
						"pos": [11242133, 11222300]
					}
				]
			}
		]
	}

	# Load with HailInputSource
	input_source = HailInputSource(sim_config['input'][0])

	input_vals = input_source.load_inputs()
	sids = input_source.input_sample_ids

	# Test how to do sample subsetting and putting in same order
	all_sids = [
		sids,
		['HG00096', 'HG00097', 'HG00099', 'HG00100', 'HG00101', 'HG00102'],
		['HG00096', 'HG00099', 'HG00100', 'HG00101', 'HG00102'],
	]

	# Get common sids
	common_sids = list(set(all_sids[0]).intersection(*all_sids[1:]))

	# Subset input vals to match common sids
	subset_idx = [np.where(sids == sid)[0][0] for sid in common_sids]

	# Use subset_idx to subset input_vals
	for key in input_vals.keys():
		if isinstance(input_vals[key], tuple):
			original_vals = input_vals[key]

			if input_vals[key][0].ndim > 1:
				input_vals[key] = (
					original_vals[0][:, subset_idx],
					original_vals[1][:, subset_idx]
				)
			else:
				input_vals[key] = (
					original_vals[0][subset_idx],
					original_vals[1][subset_idx]
				)
		elif isinstance(input_vals[key], np.ndarray):
			if input_vals[key].ndim > 1:
				input_vals[key] = input_vals[key][:, subset_idx]
			else:
				input_vals[key] = input_vals[key][subset_idx]

	print(input_vals)
