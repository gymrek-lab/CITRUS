"""CITRUS command line interface.

See CITRUS/doc/CLI.md for more information.

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
        
@click.group()
@click.version_option(package_name="citrus", message="%(version)s")
def citrus():
	pass

@citrus.command(no_args_is_help=True)
@click.option(
	'-c', '--config_file', 
	type=str, 
	required=True, 
	help="Path to JSON simulation config file."
)
@click.option(
	'-g', '--genotype_files',
	type=str,
	multiple=True,
	help=(
		"Optional path(s) to genotype file(s). Adds 'file' key to input source "
		"configs, overwriting existing 'file' values if present. "
		"The genotype_files arguments will be assigned to input sources in "
		"the order they are provided. (ex: -g genotypes1.vcf -g genotypes2.vcf"
		" would assign genotypes1.vcf to the first input source in the config's"
		" 'input' list and genotypes2.vcf to the second input source)."
	)
)
@click.option(
	'-o', '--output_dir',
	default=".",
	show_default=True,  
	help="Path to directory to save output files in."
)
@click.option(
    '-f', '--output_filename', 
    default="output.csv",
    show_default=True,
    help="Filename for saving output file containing simulation values, "
	"including the final phenotype values. Also includes sample IDs. Will be "
	"saved as a CSV file unless the -t or --tsv flag is used, in which case "
	"it will be saved as a TSV file."
)
@click.option(
    '--output_config_filename',
    default="config.json",
    show_default=True,
    help="Filename for saving configuration file of the run simulation. "
    "For configurations with random selections, this file will be updated "
    "to include the random selections made by nodes. Will be saved as a JSON "
    "file."
)
@click.option(
    '-t', '--tsv', 
    is_flag=True, 
    show_default=True, 
    default=False,
    help="Change output file from comma seperated CSV to tab seperated TSV."
)
def simulate(
    config_file: str, 
    genotype_files: str,  
	output_dir: str, 
	output_filename: str, 
	output_config_filename: str,
    tsv: bool
):
	"""
	Simulates phenotypes by modeling cis, inheritance, and trans
	effects across the genome. Creates a set of phenotypes from a
	set of genotypes.

	genotype_files must be VCF files or compressed VCF files.
	"""
    
	from json import load
	from pheno_sim import PhenoSimulation

	with open(config_file, "r") as f:
		config = load(f)

	if genotype_files: 
		for i, path in enumerate(genotype_files):
			config['input'][i]['file'] = path


	# Create simulation
	sim = PhenoSimulation(config)
	
	# Run simulation
	sim_vals = sim.run_simulation()
	
	# Save output
	sim.save_output(
		sim_vals,
		output_dir=output_dir,
		output_file_name=output_filename,
		output_config_name=output_config_filename,
		sep="\t" if tsv else ","
	)

@citrus.command(no_args_is_help=True)
@click.option(
	'-c', '--config_file', 
	type=str, 
	required=True, 
	help="Path to JSON simulation config file."
)
@click.option(
    '-o', '--out', 
    default='plot',
    show_default=True,
    help="Output filename (without extension) for saving plot."
)
@click.option(
	'-f', '--format',
	type=click.Choice(['jpg', 'png', 'svg']),
	default='png', 
	show_default=True, 
	help="File format and extension for the output plot."
)
def plot(config_file: str, out: str, format: str):
	"""
	Save a plot of the network defined by the simulation config file.

	Note: Colors correspond to cis, inheritance, and trans effects
	"""
	
	from pheno_sim import plot
	from json import load

	with open(config_file, "r") as f:
		config = load(f)

	out += "." + format
	
	# Create a plot of the model
	plot.visualize(input_spec=config, filename=out, format=format)

@citrus.command(no_args_is_help=True)
@click.option(
	'-c', '--config_file', 
	type=str, 
	required=True, 
	help="Path to JSON simulation config file."
)
@click.option(
	'-g', '--genotype_files',
	type=str,
	multiple=True,
	help=(
		"Optional path(s) to genotype file(s). Adds 'file' key to input source "
		"configs, overwriting existing 'file' values if present. "
		"The genotype_files arguments will be assigned to input sources in "
		"the order they are provided. (ex: -g genotypes1.vcf -g genotypes2.vcf"
		" would assign genotypes1.vcf to the first input source in the config's"
		" 'input' list and genotypes2.vcf to the second input source)."
	)
)
@click.option(
	'-s', '--save_path', 
	type=str, 
	default="shap_vals.csv",
	show_default=True, 
	help=(
		"File path for saving SHAP values."
	)
)
@click.option(
	'--save_config_path',
	type=str, 
	default=None,
	show_default=True,
	help=(
		"Filename for saving configuration file of the run simulation. For "
		" configurations with random selections, this file will be updated to "
		" include the random selections made by nodes. Will be saved as a JSON "
		"file. If not provided, the config file will not be saved."
	)
)
def shap(
	config_file: str, 
	genotype_files: str, 
	save_path: str, 
	save_config_path: str
):
	"""
	Computes the local and global shapley values of a model.
	"""
	from pheno_sim import PhenoSimulation
	from pheno_sim.shap import run_SHAP
	from json import load

	phenotype_key = 'phenotype'

	simulation = PhenoSimulation.from_JSON_file(config_file)
	
	with open(config_file, "r") as f:
		config = load(f)

	if genotype_files: 
		for i, path in enumerate(genotype_files):
			config['input'][i]['file'] = path

	run_SHAP(
		simulation,
		phenotype_key,
		save_path,
		save_config_path,
	)
