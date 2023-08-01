# shap 

Compute local and global shapley values of the simulation network specified by the user. 

## Usage

```
citrus shap \
--config_file STR \ 
--input_file STR \
--collapse_haplotypes BOOL \
--save_path STR \
--save_config_path STR
```

## Input

The user specifies the input sources and network consisting of input and operator nodes in a JSON configuration file. 

Note that the input sources defined in the JSON configuration file can be overriden by using the `--input_file` option.

## Output

The output of the command consists of two files: 
- a CSV file with the shapley values across all the input variants/nodes
- a JSON configuration file with the exact parameters used in the simulation

Note that although the network in the JSON configuration file is defined by the user, it can contain nodes that draw values for certain simulation parameters from a distribution. Therefore, the drawn values are saved in a configuration file for reproducability. 

## Examples

The simplest usage is as follows:

```
citrus shap -c config.json 
```

If you want to run the same network on one or more files, you can run:
```
citrus simulate -c config.json --input_file pheno_sim_demos/1000_genomes_data/name_of_file1 --input_file pheno_sim_demos/1000_genomes_data/name_of_file2
```

If you'd like to specify the name of the output files, you can run:
```
citrus simulate -c config.json --save_path example_output.csv --save_config_path example_config.json
```

Note: currently, only CSV files are supported for the output file format.
