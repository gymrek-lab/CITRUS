# simulate

Simulates a complex trait by computing the phenotypes from a set of genotypes over a network. The user defines the network and 
the set of genotypes as the input in a JSON file as described in the [user guide](https://github.com/gymrek-lab/CITRUS/blob/main/doc/user_guide.md#citrus-simulation-mechanics).

## Usage

```
citrus simulate \
--config_file STR \
--input_file STR \
--output_dir STR \
--output_filename STR \
--output_config_json STR \
--tsv BOOL
```

## Input 

The user specifies the input sources and network consisting of input and operator nodes in a JSON configuration file. 

Note that the input sources defined in the JSON configuration file can be overriden by using the `--input_file` option.

## Output

The output of the command consists of two files: 
- a CSV file with the phenotypes for all samples
- a JSON configuration file with the exact parameters used in the simulation. 

Note that although the network in the JSON configuration file is defined by the user, it can contain nodes that draw values for certain simulation parameters from a distribution. Therefore, the drawn values are saved in a configuration file for reproducability. 

## Examples

The simplest usage is as follows:

```
citrus simulate -c config.json
```
In this case, the input file is defined within config.json. 

If you want to run the same network on one or more files, you can run:
```
citrus simulate -c config.json --input_file pheno_sim_demos/1000_genomes_data/name_of_file1 --input_file pheno_sim_demos/1000_genomes_data/name_of_file2
```

If you'd like to specify the name of the output files, you can run:
```
citrus simulate -c config.json --output_filename myoutput.csv --output_config_file myconfig.json
```

If you'd like to save the file using a TSV format, you can run:
```
citrus simulate -c config.json --tsv
```

