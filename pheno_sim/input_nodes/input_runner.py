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

from typing import Any
import numpy as np

from pheno_sim.input_nodes import BaseInputSource, HailInputSource


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
		print('Loading input data...')
		
		# Simple case of only one input source file
		if len(self.input_sources) == 1:
			input_node_vals = self.input_sources[0].load_inputs()
			sample_ids = self.input_sources[0].input_sample_ids.copy()
		else:
			# Load all values
			input_vals = []
			for input_source in self.input_sources:
				input_vals.append(input_source.load_inputs())

			# Get common subset of sample ids
			sample_ids = set()
			for input_source in self.input_sources:
				sample_ids |= set(input_source.input_sample_ids)
			sample_ids = list(sample_ids)

			# Subset input values to common sample ids
			input_node_vals = {}

			for input_source in self.input_sources:
				input_node_vals.update(
					input_source.subset_inputs(sample_ids, input_vals)
				)
			
		# Return input data
		return sample_ids, input_node_vals
	
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
	
	input_runner = InputRunner(sim_config['input'])

	sample_ids, input_node_vals = input_runner()

	print(input_runner.get_config())