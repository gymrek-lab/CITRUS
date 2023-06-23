""" Abstrract class for input sources (e.i. input data files like a VCF),
which will be used to create input nodes for the simulation.
"""

from abc import ABC, abstractmethod


class BaseInputSource(ABC):
	""" Abstract class for input sources (e.i. input data files like a VCF),
	which will be used to create input nodes for the simulation.
	
	The class implements two main functions:
		- load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		- subset_and_order_samples(sample_ids): Subsets data in input_nodes
			and input_sample_ids to just the sample ids in sample_ids and in
			the same order as sample_ids. Used to get corresponding sample ids
			and data from multiple input sources.
			
	There is also a class method get_input_source(input_config) that returns
	the appropriate input source class based on the dict from the input config.
			
	Attributes:
		input_config: The dictionary from the input section of the simulation
			config file that defines this input source. Input sources with
			random selection update this to what is selected for
			reproducibility.
		input_nodes: A list of input nodes that use the input source.
		input_sample_ids: A list of sample ids from the input source.
		
	Methods:
		load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		subset_and_order_samples(sample_ids): Subsets data in input_nodes
			and input_sample_ids to just the sample ids in sample_ids and in
			the same order as sample_ids. Used to get corresponding sample ids
			and data from multiple input sources.
		get_input_source(input_config): Returns the appropriate input source
			class based on the dict from the input config.
	"""
	
	def __init__(self, input_config):
		self.input_config = input_config
		self.input_nodes = None
		self.input_sample_ids = None
	
	@abstractmethod
	def load_inputs(self):
		""" Loads the input data from the source file and sets the input_nodes
		and input_sample_ids attributes.
		"""
		pass
	
	@abstractmethod
	def subset_and_order_samples(self, sample_ids):
		""" Subsets data in input_nodes and input_sample_ids to just the sample
		ids in sample_ids and in the same order as sample_ids. Used to get
		corresponding sample ids and data from multiple input sources.
		
		Args:
			sample_ids: A list of sample ids to subset to.
		"""
		pass
	
	@classmethod
	@abstractmethod
	def get_input_source(cls, input_config):
		""" Returns the appropriate input source class based on the dict from
		the input config.
		
		Args:
			input_config: The dictionary from the input section of the
				simulation config file that defines this input source.
		"""
		pass


if __name__ == '__main__':

	# For testing
	sim_config = {
		"input": [
			{
				"file": "../../pheno_sim_demos/1000_genomes_data/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
				"file_format": "vcf",
				"reference_genome": "GRCh37",
				"input_nodes": [
					{
						"alias": "LDLR_intron_variants",
						"type": "SNP",
						"chr": "19",
						"pos": [11202306, 11206575]
					},
					{
						"alias": "LDLR_upstream_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11197261
					},
					{
						"alias": "LDLR_intron_variant",
						"type": "SNP",
						"chr": "19",
						"pos": 11216561
					}
				]
			}
		]
	}

	# Open data file with Hail