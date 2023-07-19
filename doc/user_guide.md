# CITRUS User Guide

TODO Overview. Mention designed for use with existing genotype data.

# Defining a Simulation

![Example GM](example_gm.png "Example Graphical Model")

In CITRUS, simulations are defined by a graphical model. The directed graph is composed of input nodes, representing genetic variants, and operator nodes, which represent intermediate operations their resulting values. The edges represent the flow of values from the input nodes to the final operator node, who's resulting value represents the phenotype being simulated.

Users define these graphic models in a configuration JSON file. Simulation configuration JSON files define a dictionary with keys 'input' and 'simulation_steps'. The 'input' key maps to a list of input sources and their resulting input nodes. The 'simulation_steps' key maps to a list of operator or nodes and their input edges, which defines the rest of the graph.

## Input

CITRUS uses phased genetic data in one of several VCF-like file formats (VCF, TODO BGEN, GEN) as input. The 'input' section of the JSON config file defines a list of input sources represented by dictionaries. Each input source represents a file or multiple files and defines the input nodes who's values are derived from that data. An example input section defining a single input source with two input nodes is below. All input sources must include sample IDs, and phenotypes will only be simulated for samples in all input sources.

```json
{
	"input": [
		{
			"file": "../pheno_sim_demos/1000_genomes_data/genotypes_chr19.vcf.gz",
			"file_format": "vcf",
			"reference_genome": "GRCh37",
			"force_bgz": true,
			"input_nodes": [
				{
					"alias": "LDLR_intron_variant",
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
```

### Defining Input Sources

Each input source is represented by a dictionary with the following keys:

* file (optional, otherwise provided by command line argument): Path to the data file, list of file paths (if not using CLI), or hadoop glob pattern matching file(s).
* engine (optional str, default "hail"): The engine to use to read the data file. Currently only hail is supported.
* file_format (optional str, default "vcf"): The format of the data file. Currently only VCF is supported.
* input_nodes (optional list of dicts): A list of dictionaries that define the input nodes that use this data source.

#### Engine and File Format Specific Keys

Additional keys are used based on the engine being used to load the data and the file format. See the [Input Sources documentation](input_sources.md) for more information.


### Defining Input Nodes

Input nodes are defined in the 'input_nodes' list of dictionaries. Each dictionary defines a single input node, but nodes may contain multiple variants (as with the "LDLR_missense_variants" node in the example above). 

The typical behavior of input nodes is to treat the reference allele as a 0 and any alternate alleles as a 1. Nodes may specify other behavior to handle things like multi-allelic sites or other features like SNP copy number.

All dictionaries defining input nodes must have the following keys:

* alias: The alias for the input node. This is used to refer to the node in the simulation configuration.
* type: The type of the input node. See [Input Node Types](input_nodes.md#input-node-types) for more information. Values in that section's headers in parentheses are the values for the 'type' key (e.g. "snp" for single nucleotide polymorphism input nodes).

They may also have additional arguments specific to the input node type (e.g. to specify a locus). For more information, see the [Input Nodes documentation](input_nodes.md#input-node-types).






