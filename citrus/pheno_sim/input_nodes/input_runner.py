""" Runs the input nodes for the simulation based on the input config.

See input_nodes_README.md for more details.

The sample ids from the source data files will be subset to just those
present in all data files. Sample ids will be returned by the simulation
along with all other output in corresponding order.

The definition for the simulation input is part of the config JSON file
with the key 'input'. The value for this key is a list of dictionaries.
Each of these dictionaries defines a source data file and the input nodes
that use it.

Example:
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
			],
			...
		}

"""

import numpy as np
from .hail_input import HailInputSource
from ...utils import MSG

class InputRunner:
	""" Steps up and runs the input nodes step of the simulation.
	"""
	
	def __init__(self, input_config):
		""" Initializes the input runner.
		
		Args:
			input_config: List of dicts defining input sources and their
				respective input nodes. See input_nodes_README.md for more.
		"""
	
		self.input_sources = []

		MSG('Initializing input sources...')
		for input_source_config in input_config:
			if (
				'engine' not in input_source_config
				or input_source_config['engine'] == 'hail'
			):
				self.input_sources.append(
					HailInputSource(input_source_config)
				)
			else:
				raise ValueError(
					'Invalid input engine: ' + input_source_config['engine']
				)

		MSG('Getting samples to use...')
		sample_ids = set()
		for input_source in self.input_sources:
			sample_ids |= set(input_source.input_sample_ids)
		self.sample_ids = list(sample_ids)
		MSG("Loaded {nsamp} ids".format(nsamp=len(self.sample_ids)))
			
	def __call__(self):
		""" Runs the input nodes for the simulation.
		
		Loads the input data and subsets the sample ids to those that are
		present in all input data files.
		
		Returns:
			A tuple of:
				- An array of sample ids that correspond to the input node
					values.
				- A dict of input node values. The keys are the input node
					aliases and the values are numpy arrays of the input
					node values.
		"""
		MSG('Loading input data...')
		input_node_vals = {}
		for input_source in self.input_sources:
			for node in input_source.input_config["input_nodes"]:
				node_alias = node["alias"]
				input_node_vals[node_alias] = \
					input_source.load_input_node(node_alias, self.sample_ids)

		# Return input data
		return np.array(self.sample_ids), input_node_vals

	def get_config(self):
		""" Returns the input config for the simulation.
		
		Returns:
			A list of dicts defining input sources and their respective
			input nodes.
		"""
		return [
			input_source.input_config.copy() 
			for input_source in self.input_sources
		]