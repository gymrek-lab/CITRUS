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

import click

# @click.command()
# @click.option('--count', default=1, help='number of greetings')
# @click.argument('name')
# def hello(count, name):
#     for x in range(count):
#         click.echo(f"Hello {name}!")
        
@click.group()
@click.version_option(message="%(version)s")
def citrus():
	pass

@citrus.command()
@click.option(
	'-c', '--config_file', 
	type=str, 
	required=True, 
	help="File defining the location of input data and the simulation steps"
)
@click.option(
	'-o', '--output_dir', 
	required=True, 
	help="Path to store output file"
)
@click.option(
    '-f', '--output_file_name', 
    help="Name of output file"  
)
@click.option(
    '--output_config_json',
    help="Name of output config file"
)
@click.option(
    '--tsv', 
    is_flag=True, 
    show_default=True, 
    default=False,
    help="Set column separator to <TAB>"
)
def simulate(
    config_file: str,  
	output_dir: str, 
	output_file_name: str, 
	output_config_json: str,
    tsv: bool
):
	"""
	Simulates phenotypes by modeling cis, inheritance, and trans effects across the genome. 
	Creates a set of phenotypes from a set of genotypes.

	GENOTYPES can be formatted as a VCF or PGEN file.

	"""
    
	from json import load
	from pheno_sim import PhenoSimulation

	with open(config_file, "r") as f:
		config = load(f)

	# # If genotype files were provided, replace paths in config file
	# if genotype_files:
	# 	assert len(genotype_files) == len(config["input"]), \
	# 		"Number of genotype files provided does not match number of input " \
	# 		"source files in configuration file"
		
	# 	for i, path in enumerate(genotype_files):
	# 		config["input"][i]["file"] = path


	# Create simulation
	sim = PhenoSimulation(config)
	
	# Run simulation
	sim_vals = sim.run_simulation()

	
	# Save output
	sim.save_output(
		sim_vals,
		output_dir=output_dir,
		output_file_name=output_file_name,
		output_config_name=output_config_json,
		sep="\t" if tsv else ","
	)

@citrus.command()
@click.option(
	'--visualize', 
	help='Visualizes the simulation steps as a graphical model'
)
@click.option(
	'--output_file_name',
	
)
def plot():
	"""
	Visualizes the simulation steps as a graphical model.

	Note: Colors correspond to cis-, inheritance, and trans- effects
	"""
	pass

@citrus.command()
def shap():
	"""
	Computes the local and global shapley values of a model.

	"""

	pass

@citrus.command()
def generate():
	"""
	Generates a random graphical model given a set of parameters.

	"""
	pass

# @click.option(
# 	'--genotype_files', 
# 	type=str,  
# 	help="path to where genotype files are stored"	
# )