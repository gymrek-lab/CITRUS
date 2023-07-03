"""CL interface for running CITRUS phenotype simulations.

The simulation to be ran is defined by a configuration JSON file. 
TODO: Give complete description of the configuration file or 
	point to documentation.
	
This tool can be used to run the simulation based on either:

	1. A single configuration JSON file that specifies paths to genotype
		data files.
		
		CITRUS_sim <path_to_config_file>
		
	2. A single configuration JSON file and a list of paths to genotype
		data files. The list of paths must be the same length as the
		number of input source files in the configuration file (i.e. 
		the length of the list under the 'input' key in the JSON). Any
		paths in the configuration file will be ignored.
		
		CITRUS_sim <path_to_config_file> <path_to_genotype_file> \\
			<path_to_genotype_file> ...
			
		CITRUS_sim <path_to_config_file> <path_to_genotype_file>          
"""

import argparse
import json

from pheno_sim import PhenoSimulation


def main():
	
	# Parse arguments
	parser = argparse.ArgumentParser(
		description=__doc__,
		formatter_class=argparse.RawTextHelpFormatter,
	)
	parser.add_argument("config_file", help="Path to configuration JSON file")
	parser.add_argument(
		"genotype_files",
		nargs="*",
		help="Paths to genotype files (optional)"
	)
	args = parser.parse_args()
	
	# Load configuration file
	with open(args.config_file, "r") as f:
		config = json.load(f)
	
	# If genotype files were provided, replace paths in config file
	if args.genotype_files:
		assert len(args.genotype_files) == len(config["input"]), \
			"Number of genotype files provided does not match number of input " \
			"source files in configuration file"
		
		for i, path in enumerate(args.genotype_files):
			config["input"][i]["file"] = path
	
	# Create simulation
	sim = PhenoSimulation(config)
	
	# Run simulation
	sim.run_simulation()


if __name__ == "__main__":
	main()