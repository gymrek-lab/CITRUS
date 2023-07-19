# Input Nodes Guide

The typical behavior of input nodes is to treat the reference allele as a 0 and any alternate alleles as a 1. Nodes may specify other behavior to handle things like multi-allelic sites or other features like SNP copy number.

All dictionaries defining input nodes must have the following keys:

* alias: The alias for the input node. This is used to refer to the node in the simulation configuration.
* type: The type of the input node. See [Input Node Types](#input-node-types) for more information. Values in that section's headers in parentheses are the values for the 'type' key (e.g. "snp" for single nucleotide polymorphism input nodes).

They may also have additional arguments specific to the input node type.

# Input Node Types

## Single nucleotide polymorphisms (SNPs): "snp"

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