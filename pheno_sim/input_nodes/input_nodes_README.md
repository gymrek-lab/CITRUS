# Simiulation Input

pheno_sim simulations use genotypes from phased data file(s) as input.

These source data files may be read using one of the following libraries as the engine:

	hail: Supports VCF.
		TODO:
			- Add support for other file formats (gen, bgen, plink, etc.)

	TODO: Add support for other engines

The sample ids from the source data files will be subset to just those present in all data files. Sample ids will be returned by the simulation along with all other output in corresponding order.

## Defining Input in Simulation Configuration

The definition for the simulation input is part of the config JSON file with the key 'input'. The value for this key is a list of dictionaries. Each of these dictionaries defines a source data file and the input nodes that use it.

Example:

	"input": [
		{
			"file": "1000_genomes_data/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz",
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

### Data Source Arguments

Each dictionary in the 'input' list that defines a data source and its input nodes must have the following keys:

* file: Path to the data file or list of paths to data files.
* engine: The engine to use to read the data file.
* file_format: The format of the data file.
* input_nodes: A list of dictionaries that define the input nodes that use this data source.

### Data Source Engines and Formats

#### Hail

Hail is a Python library for working with genomic data. It supports reading VCF files and other formats. See the [Hail documentation](https://hail.is/docs/0.2/index.html) for more information. 'hail' is the default engine or it may be specified explicitly using the 'engine' key.

Hail specific arguments:

* reference_genome: Reference genome to use. Default is GRCh38. Must be one of: GRCh37, GRCh38, GRCm38, or CanFam3.

##### VCF

VCF files are read using the 'vcf' file_format. See https://hail.is/docs/0.2/methods/impex.html#hail.methods.import_vcf for more information.

Aruments:

* file: Path to the VCF file, hadoop glob pattern, or list of paths to VCF files.
* force_bgz: If True, load .vcf.gz files as blocked gzip files, assuming that they were actually compressed using the BGZ codec.



## Input Nodes

Input nodes are defined in the 'input_nodes' list of dictionaries. Each dictionary defines a single input node, but nodes may contain multiple values.

The typical behavior of input nodes is to treat the reference allele as a 0 and any alternate alleles as a 1. Nodes may specify other behavior to handle things like multi-allelic sites or other features like SNP copy number (TODO).

All dictionaries defining input nodes must have the following keys:

* alias: The alias for the input node. This is used to refer to the node in the simulation configuration.
* type: The type of the input node. See below.
* **kwargs: Additional arguments specific to the input node type.

### Input Node Types

#### SNP

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
