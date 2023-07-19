# CITRUS User Guide

TODO Overview. Mention designed for use with existing genotype data.

# Defining a Simulation

![Example GM](example_gm.png "Example Graphical Model")

In CITRUS, simulations are defined by a graphical model. The directed graph is composed of input nodes, representing genetic variants, and operator nodes, which represent intermediate operations their resulting values. The edges represent the flow of values from the input nodes to the final operator node, who's resulting value represents the phenotype being simulated.

Users define these graphic models in a configuration JSON file. Simulation configuration JSON files define a dictionary with keys 'input' and 'simulation_steps'. The 'input' key maps to a list of input sources and their resulting input nodes. The 'simulation_steps' key maps to a list of operator or nodes and their input edges, which defines the rest of the graph.

## Input

CITRUS uses phased genetic data in one of several VCF-like file formats (VCF, TODO BGEN, GEN) as input. The 'input' section of the JSON config file defines a list of input sources represented by dictionaries. Each input source represents a file or multiple files and defines the input nodes who's values are derived from that data. An example input section defining a single input source with two input nodes is below. All input sources must include sample IDs, and phenotypes will only be generated for samples in all input sources.

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
				},
				...
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

#### Engine Specific Keys

Based on the engine being used to load the data, there are additional optional keys that may be provided:

#### Hail

* reference_genome (optional str, default "GRCh38"): The reference genome to use when reading the data file. Must be one of: GRCh37, GRCh38, GRCm38, or CanFam3.

When using file_format "vcf", the force_bgz key may also be used:

* force_bgz (optional bool, default false): If true, force hail to read the file as bgzipped, even if the file extension is not .bgz. See [Hail import_vcf](https://hail.is/docs/0.2/methods/impex.html#hail.methods.import_vcf) for more information.


### Defining Input Nodes

Input nodes are defined in the 'input_nodes' list of dictionaries. Each dictionary defines a single input node, but nodes may contain multiple variants (as with the "LDLR_missense_variants" node in the example above).

The typical behavior of input nodes is to treat the reference allele as a 0 and any alternate alleles as a 1. Nodes may specify other behavior to handle things like multi-allelic sites or other features like SNP copy number.

All dictionaries defining input nodes must have the following keys:

* alias: The alias for the input node. This is used to refer to the node in the simulation configuration.
* type: The type of the input node. See [Input Node Types](#input-node-types) for more information. Values in that section's headers in parentheses are the values for the 'type' key (e.g. "snp" for single nucleotide polymorphism input nodes).

They may also have additional arguments specific to the input node type.

### Input Node Types

#### Single nucleotide polymorphisms (SNPs): "snp"

A single SNP (SNP, indel, deletion, or other feature with a single position defined with a single line of a VCF like file) or a list of SNPs.

Reference alleles will become 0 values and any alternate alleles will become 1 values.

SNPs are specified using the 'chr' and 'pos' keys.

Arguments:

* chr: The chromosome(s) of the SNP(s). May either be:
	* A string representing a single chromosome all positions are on.
	* A list of strings the same length as the number of positions, such that each position is on the corresponding chromosome.
	NOTE: The string specifying the chromosome must be exactly what
		is used in the source file (e.g. for GRCh37, '1' not 'chr1').
* pos: The position(s) of the SNP(s). May either be:
	* An integer representing a single position.
	* A list of integers. Positions will either be all on the same chromosome or mapped to the corresponding chromosome in the 'chr' argument.



