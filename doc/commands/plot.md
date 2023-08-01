# plot 

Generates a plot of the simulation network specified by the user. 

## Usage

```
citrus plot \
--config_file STR \
--out STR \
--format [jpg|png|svg] 
```

## Input

The user specifies the input sources and network consisting of input and operator nodes in a JSON configuration file. 

## Output

The command outputs one file in the current directory called "plot.png" unless specified otherwise. 

## Examples 

To create a plot of the network given a JSON configuration file, run:

```
citrus plot -c config.file 
```

To specify the output filename and file format, run:

```
citrus plot -c config.file --out example_plot --format png
```

