"""CL interface for running CITRUS phenotype simulations.

The simulation to be ran is defined by a configuration JSON file. 
TODO: Give complete description of the configuration file or 
	point to documentation.
	
This tool can be used to run the simulation based on either:

	1. A single configuration JSON file that specifies paths to genotype
		data files.
		
		CITRUS_sim -c <path_to_config_file> 
		
	2. A single configuration JSON file and a list of paths to genotype
		data files. The list of paths must be the same length as the
		number of input source files in the configuration file (i.e. 
		the length of the list under the 'input' key in the JSON). Any
		paths in the configuration file will be ignored. The -g or
		--genotype_files flag can be used to specify the paths to the
		genotype files.
		
		CITRUS_sim -c <path_to_config_file> -g <path_to_genotype_file> \\
			<path_to_genotype_file> ...
			
		CITRUS_sim -c <path_to_config_file> -g <path_to_genotype_file>

Output:

	If no additional flags are provided, output will be written to the
	current working directory. The output will be a CSV file (output.csv)
	containing sample IDs and all corresponding values from the simulation,
	and a JSON file (sim_config.json) containing the simulation configuration
	(including any random selections made by nodes).

	If the -o or --output_dir flag is provided, if the directory does not
	exist it will be created, and the output files will be saved to it. By
	default the output files will be named output.csv and sim_config.json,
	but these can be changed with the -f or --output_file_name and -j or
	--output_config_json flags, respectively.

	Output file will by default be a comma seperated CSV file. Use -t or
	--tsv flag to instead save as a tab seperated TSV file.

Example Usage:

	CITRUS_sim -c config.json -o sim_results/output_dir

	CITRUS_sim -c config.json -g genotype_file_1 genotype_file_2 \\
		-o sim_results/output_dir -t -f my_output.tsv -j my_sim_config.json
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

	parser.add_argument(
		"-c",
		"--config_file",
		required=True,
		help="Path to configuration file"
	)
	parser.add_argument(
		"-g",
		"--genotype_files",
		nargs="*",
		help="Paths to genotype files (optional)"
	)
	parser.add_argument(
		"-o",
		"--output_dir",
		default=".",
		help="Directory to save output to (default: current working directory)."
			" If directory does not exist it will be created."
	)
	parser.add_argument(
		"-f",
		"--output_file_name",
		default="output.csv",
		help="Name of output file (default: output.csv)"
	)
	parser.add_argument(
		"-j",
		"--output_config_json",
		default="sim_config.json",
		help="Name for saved simulation configuration file (default: "
			"sim_config.json)"
	)
	parser.add_argument(
		"-t",
		"--tsv",
		action="store_true",
		help="Save output as tab seperated TSV file (default: CSV)"
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
	sim_vals = sim.run_simulation()

	# Save output
	sim.save_output(
		sim_vals,
		output_dir=args.output_dir,
		output_file_name=args.output_file_name,
		output_config_name=args.output_config_json,
		sep="\t" if args.tsv else ","
	)


if __name__ == "__main__":
	main()