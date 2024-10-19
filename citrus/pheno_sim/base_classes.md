# Outline of classes for executing the pheno_sim

## PhenoSimulation Class

Object that runs the simulation. It is constructed from a JSON specification file. The specification file contains the inputs, the function nodes, and the output.

### Attributes

input_step: InputStep
	The input step of the simulation

simulation_steps: List[SimulationStep(s), OutputStep]
	The simulation steps of the simulation

output_step: OutputStep

### Methods

constructor(specification_dict: Dict)
- Constructs the PhenoSimulation object from a specification dictionary.

from_JSON_spec(JSON_path: str)
- Constructs the PhenoSimulation object from a JSON specification file.

run_input_step(input_file_map: None (default) or Dict[str, str])
- Runs the input step of the simulation.
- input_file_map can be None when all input nodes specify their input file paths in the specification file. If you want to use filename alias in the specification file instead, then input_file_map should be a Dict[str, str] where the keys are the aliases and the values are the paths to the files.
- Returns a Dict of HaplotypeValues (and maybe also values) that will be used as input for the simulation steps.

run_simulation_steps(input_values: Dict[str, HaplotypeValues or Values])
- Runs the function node steps of the simulation. The input values are the output Dict from the input step. The last simulation step should be an OutputStep, and it's output will be returned.

run_simulation(input_file_map: None (default) or Dict[str, str])
- Runs the entire simulation (run_input_step then run_simulation_steps).


## Data Types

I'm on the fence as to if these have to be classes or not.

#### HaplotypeValues: Tuple[numpy.ndarray, numpy.ndarray]
A tuple of two numpy arrays, each representing one of the two copies of
the chromosome. These values should be indexed such that for two
HaplotypeValues on the same chromosome, which index corresponds to which
copy of the chromosome is the same. 

e.g.:

	hap_val1 = (vals_from_chr9_copy1_loci1, vals_from_chr9_copy2_loci1)
	hap_val2 = (vals_from_chr9_copy1_loci2, vals_from_chr9_copy2_loci2) # but this would limit to two loci...?

#### Values: numpy.ndarray
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

- Input nodes are the first nodes in the simulation. They read in genotype data
  from files and convert them into HaplotypeValues or Values. They are all ran
  by the run_input_step method of the PhenoSimulation class.

- Function nodes apply some function to some values from the ValueDict and
  return a Values/HaplotypeValues object of the result. These nodes are ran by
  SimluationStep objects, which pass them the proper input from the ValuesDict
  and add the output to the ValuesDict.

- Output nodes are the last nodes in the simulation. They take some values from
  the ValueDict and write them to files and/or return them in a dict.

### Input Nodes

Input nodes read in genotype values from some file and convert them into
HaplotypeValues or Values. They are all ran by the run_input_step method of
the PhenoSimulation class.

There may be some room for optimization by doing this all in a smarter way.

#### AbstractBaseInputNode

Abstract base class for all input nodes.

##### Attributes

alias: str
- The alias of the node. This is used to refer to the node in the specification file and in the ValueDict.

##### Methods

load_vals(input_files: Dict[str, str]) -> Values or HaplotypeValues
- Loads the values from the input files. Returns a Values or HaplotypeValues object.


### Function Nodes

Functions can be divided into combine functions (which combine values from
the two haplotypes into a single np.array) and general functions which apply
some function to one of the following:

- A single Values object or multiple Values objects. Returns a single Values
  object.

- A single HaplotypeValues object or multiple HaplotypeValues objects. Returns
  a single HaplotypeValues object.

- One or more Values objects and one or more HaplotypeValues objects. Returns
  a single HaplotypeValues object.

#### AbstractBaseFunctionNode

Abstract base class for all function nodes. Defines the interface for all
function nodes.

##### Attributes

alias: str
- The alias of the node. This is used to refer to the node in the
specification file and in the ValueDict.

input_mapping: Dict[str, str or List[str]]
- Mapping from the name of the input args of the function to the alias(es) of the node(s) that comprise that input. This is used to get the input values from the ValueDict and pass them to the function.

##### Methods

constructor(alias: str, **kwargs)
- Constructs the AbstractBaseFunctionNode object.

\_\_call\_\_(input_dict: Dict[str, Values or HaplotypeValues]) -> Values or HaplotypeValues
- Runs the function node on the values passed from the ValueDict. Returns the resulting Values or HaplotypeValues object.

#### AbstractBaseCombineFunctionNode

Abstract base class for all combine function nodes. Differs in the type
checking of the \_\_call\_\_ method.

##### Methods

\_\_call\_\_(input_dict: Dict[str, HaplotypeValues]) -> Values
- Runs the function node on the HaplotypeValues passed from the ValueDict.
- Returns the resulting Values object.


### Output Nodes

TODO


## Steps

Steps are the objects that run the nodes.

### InputStep

Runs the input nodes. Returns a Dict of HaplotypeValues (and maybe also Values).

#### Attributes

input_nodes: List[InputNode]
- The input nodes of the simulation.

#### Methods

constructor(input_nodes: List[InputNode])
- Constructs the InputStep object.

from_spec_dict(spec_dict: Dict)
- Constructs the InputStep object from a specification dictionary 'input'
key's value.

\_\_call\_\_(input_files: str, List[str], or Dict[str, str]) -> Dict[str, HaplotypeValues or Values]
- Runs the input nodes. The input files can be a single file, a list of files,
or a dictionary of files where the key is some alias for the path. Returns
a Dict of HaplotypeValues (and maybe also Values).


### SimulationStep

Each SimulationStep contains a single function node. SimulationStep objects execute the function node and add the output to the ValueDict with the following two steps:

1. Call the function node with the proper input from the ValueDict. The input is determined by the input_mapping attribute of the function node.

2. Add the output of the function node to the ValueDict with the alias of the function node as the key. If required_output attribute of the SimulationStep is not None, then the ValueDict is filtered to only contain the required_output keys. The ValueDict is then returned. The rquired_output attribute is set by the PhenoSimulation object.

NOTE: The second step is not required and may be an unnecessary optimization. For now the plan is to keep it None for everything and not implement the setting of the required_output attribute by the PhenoSimulation object.

#### Attributes

function_node: FunctionNode

required_output: List[str] or None

#### Methods

constructor(function_node: FunctionNode, required_output: List[str] or default None)

from_spec(spec_dict: Dict) -> SimulationStep

\_\_call\_\_(input_dict: Dict[str, Values or HaplotypeValues]) -> Dict[str, Values or HaplotypeValues]
- Runs the function node on the values passed from the ValueDict. Returns the resulting Values or HaplotypeValues object.


### OutputStep

TODO
