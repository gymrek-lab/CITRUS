# Outline of classes for executing the pheno_sim

## PhenoSimulation Class

Object that runs the simulation. It is constructed from a JSON specification
file. The specification file contains the inputs, the function nodes, and the
output.

### Attributes

input_step: InputStep
	The input step of the simulation

simulation_steps: List[SimulationStep(s), OutputStep]
	The simulation steps of the simulation

output_step: OutputStep

### Methods

constructor(specification_dict: Dict)
	Constructs the PhenoSimulation object from a specification dictionary.

from_JSON_spec(JSON_path: str)
	Constructs the PhenoSimulation object from a JSON specification file.

run_input_step(input_files: str, List[str], or Dict[str, str])
	Runs the input step of the simulation. The input files can be a single
	file, a list of files, or a dictionary of files where the key is some alias
	for the path. Returns a Dict of HaplotypeValues (and maybe also values)
	that will be used as input for the simulation steps.

run_simulation_steps(input_values: Dict[str, HaplotypeValues or Values])
	Runs the function node steps of the simulation. The input values are the
	output Dict from the input step. The last simulation step should be an 
	OutputStep, and it's output will be returned.

run_simulation(input_files: str, List[str], or Dict[str, str])
	Runs the entire simulation (run_input_step then run_simulation_steps).


## Data Types

I'm on the fence as to if these have to be classes or not.

HaplotypeValues: Tuple[numpy.ndarray, numpy.ndarray]
	A tuple of two numpy arrays, each representing one of the two copies of
	the chromosome. These values should be indexed such that for two
	HaplotypeValues on the same chromosome, which index corresponds to which
	copy of the chromosome is the same. 
	e.g.:
		hap_val1 = (vals_from_chr9_copy1_loci1, vals_from_chr9_copy2_loci1)
		hap_val2 = (vals_from_chr9_copy1_loci2, vals_from_chr9_copy2_loci2)

Values: numpy.ndarray
	A numpy array of values. One dimension should be length the number of
	samples, and the other dimension should be length the number of 
	values for each sample (e.g. the alt allele counts over 5 LOF loci for
	50 samples, a single cumulative value representing the effect of some gene
	for the 50 samples being simulated).

This will also refer to the ValueDict, which is a Dict[str, Values or
HaploypeValues] that gets passed between the simulation steps. The keys are
alias of the node the values are from.


## Nodes

Nodes fall into three categories: input, function, and output.


