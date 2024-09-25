"""CITRUS command line interface.

See CITRUS/doc/CLI.md and individual tools for more information.
"""

import click
        
@click.group()
@click.version_option(package_name="citrus", message="%(version)s")
def citrus():
	pass

"""
citrus simulate
"""
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

"""
citrus plot
"""
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
	
	# Create a plot of the model
	plot.visualize(input_spec=config, filename=out, img_format=format)

"""
citrus shap
"""
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
	'-i', '--included_samples',
	type=str,
	default=None,
	show_default=True,
	help=(
		"Path to file containing sample IDs to include in the SHAP analysis. "
		"File should contain one sample ID per line."
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
	included_samples: str,
	save_path: str, 
	save_config_path: str
):
	"""
	Computes the local shapley values of a model.
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

	# Load optional sample IDs
	if included_samples:
		with open(included_samples, "r") as f:
			included_samples = [line.strip() for line in f]	# type: ignore
		run_SHAP(
			simulation,
			phenotype_key,
			included_samples,
			save_path,
			save_config_path,
		)
	else:
		run_SHAP(
			simulation,
			phenotype_key,
			save_path,
			save_config_path,
		)
