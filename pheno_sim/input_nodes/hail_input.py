""" Input source object and nodes using the Hail engine.

Includes following input nodes types:
	- SNP
	
Combatibile with the following file formats:
	- VCF
"""

import numpy as np

import hail as hl

from pheno_sim.input_nodes import BaseInputSource


class HailInputSource(BaseInputSource):
	""" Hail input source object.

	Attributes:
		input_config: The dictionary from the input section of the simulation
			config file that defines this input source. Input sources with
			random selection update this to what is selected for
			reproducibility.
		input_nodes: A list of input nodes that use the input source.
		input_sample_ids: A list of sample ids from the input source.

	Methods:
		__init__(input_config): Constructor. Ignores the 'engine' key in the
			input_source_config dictionary and uses hail.
		load_inputs(): Loads the input data from the source file and sets
			the input_nodes and input_sample_ids attributes.
		subset_and_order_samples(sample_ids): See BaseInputSource.		
	"""

	def __init__(self, input_config):
		super().__init__(input_config)

	def load_inputs(self):
		""" Loads the input data from the source file and sets the input_nodes
		and input_sample_ids attributes.
		"""


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
	input_source_config = sim_config['input'][0]

	geno_data = hl.import_vcf(
		input_source_config['file'],
		reference_genome=input_source_config['reference_genome'],
	)