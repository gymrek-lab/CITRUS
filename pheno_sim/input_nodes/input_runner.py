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

	"input": [
		{
			"file": "data/1kg.vcf.bgz",
			"engine": "hail",
			"file_format": "vcf",
			"input_nodes": [
				{
					"alias": "causal_gene_LOF",
					"type": SNP,
					"chr": "1",
					"pos": [1234500, 1234508]
				},
				{
					"alias": "causal_gene_promoter",
					"type": SNP,
					"chr": "1",
					"pos": 1234567
				}
			]
		}
	]
"""