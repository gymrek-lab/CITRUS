# Command Line Interface

The CITRUS command line interface allows you to run simulations, visualize phenotype architectures, and use all the other features of CITRUS. The following sections describe the available commands. These commands are run using the command format:

```bash
citrus COMMAND [OPTIONS]
```

The CITRUS tool main help page can be accessed from the command line by running:

```bash
citrus
```


### Table of Contents

- [plot](#plot)
- [simulate](#simulate)
- [shap](#shap)


## plot 

Save a plot of the network defined by the simulation config file. User can specify the output filename and file format, otherwise the default is "plot.png".

### Options

| Option | Description |
| ------ | ----------- |
|-c, --config_file | Path to JSON simulation config file. [required] |
|-o, --out | Output filename (without extension) for saving plot. [default: plot] |
|-f, --format | File format and extension for the output plot. [default: png] |
|--help | Show help message. |


### Example Usage

To save the plot of the network defined by config.json as plot.png:
```
citrus plot -c config.json
```

To save the plot of the network defined by config2.json as config2.svg:
```
citrus plot \
	--config_file config2.json \
	--out config2 \
	--format svg
```


## simulate

Runs CITRUS simulation defined by the JSON configuration file. If '--genotype_files' arguments are provided, the input sources' 'file' values in the config will be overwritten with the provided genotype file paths. If no '--genotype_files' arguments are provided, the input sources in the config file will be used as is. 

The output of the command consists of two files. The first is a CSV or TSV file with all simulation values (including final phenotype, input values, and intermediate values) and sample IDs. The second is an updated JSON configuation file containing the exact parameters used in the simulation. For configurations with random selections, this file will be updated to include the random selections made by nodes. The user can specify the output directory and filenames for these files, otherwise the default is the current directory and "output.csv" and "config.json" respectively. 

### Options

| Option | Description |
| ------ | ----------- |
|-c, --config_file | Path to JSON simulation config file. [required] |
|-g, --genotype_files | Optional path(s) to genotype file(s). Adds 'file' key to input source configs, overwriting existing 'file' values if present. The genotype_files arguments will be assigned to input sources in the order they are provided. (ex: -g genotypes1.vcf -g genotypes2.vcf would assign genotypes1.vcf to the first input source in the config's 'input' list and genotypes2.vcf to the second input source). |
|-o, --output_dir | Path to directory to save output files in. [default: .] |
|-f, --output_filename | Filename for saving output file containing simulation values, including the final phenotype values. Also includes sample IDs. Will be saved as a CSV file unless the -t or --tsv flag is used, in which case it will be saved as a TSV file. [default: output.csv] |
|--output_config_filename | Filename for saving configuration file of the run simulation. For configurations with random selections, this file will be updated to include the random selections made by nodes. Will be saved as a JSON file. [default: config.json] |
|-t, --tsv | Change output file from comma separated CSV to tab separated TSV. |
|--help | Show help message. |

### Example Usage

Run simulation based on configuration JSON. Save output files in current directory as output.csv and config.json:

```bash
citrus simulate -c config.json
```

Run same network, but with a different input genotype file. Save output files in current directory as output2.csv and config2.json:

```bash
citrus simulate -c config.json -g genotypes2.vcf \
	-f output2.csv --output_config_filename config2.json
```

Save as a TSV in a different directory:

```bash
citrus simulate -c config.json -t \
	-o /path/to/output/directory
```


## shap 

Comput local SHAP Shapley value estimates for specified simulation. Output will be a file with the SHAP value for each input variant for each sample. There will be one shapley value per haploid genotype (i.e. 2 values per variant per sample).

### Options

| Option | Description |
| ------ | ----------- |
| -c, --config_file | Path to JSON simulation config file.  [required] |
| -g, --genotype_files | Optional path(s) to genotype file(s). Adds 'file' key to input source configs, overwriting existing 'file' values if present. The genotype_files arguments will be assigned to input sources in the order they are provided. (ex: -g genotypes1.vcf -g genotypes2.vcf would assign genotypes1.vcf to the first input source in the config's 'input' list and genotypes2.vcf to the second input source). |
| -s, --save_path | File path for saving SHAP values. [default: shap_vals.csv] |
| --save_config_path | Filename for saving configuration file of the run simulation. For  configurations with random selections, this file will be updated to  include the random selections made by nodes. Will be saved as a JSON file. If not provided, the config file will not be saved. |

### Example Usage

```
citrus shap -c config.json 
```
