""" Steps are the objects that run the nodes.

There are three types:

- InputStep: These are the steps that run the input nodes which read in
	the genotype data from some file and convert them into HaplotypeValues
	or Values.
	
- SimluationStep: These are the steps that run the function nodes which
	apply some function to the values from the ValuesDict and add the
	result to the ValuesDict.
	
- OutputStep: These are the steps that run the output nodes which write
	the values from the ValuesDict to some file and/or return it in some
	format.
	
Steps are ran by the PhenoSimulation class.
"""

from typing import List, Dict

from .base_nodes import AbstractBaseInputNode
from .data_types import HaplotypeValues, Values, ValuesDict

class InputStep:
	""" Runs the input nodes. Returns a Dict of HaplotypeValues
	(and maybe also Values) as specified by the input nodes.
	
	Attributes:
		input_nodes: A list input nodes (subclasses of AbstractBaseInputNode)
			that will be ran by this step.
	
	Methods:
		__init__(self, input_nodes: List[AbstractBaseInputNode]) -> None
			Initializes the InputStep object. This object will create the
				initial ValuesDict that will be passed to the SimulationSteps
				by loading genotype data from files.
				
		from_spec_dict(spec_dict: Dict) -> InputStep
			Alternative constructor. Creates an InputStep from a simulation
				specification dict. Class method.
				
		__call__(self, input_file_map: None (default) or Dict[str, str]) -> ValuesDict
			Run input step and return ValuesDict to be passed to simulation
				steps.
	"""
	
	def __init__(self, input_nodes: List[AbstractBaseInputNode]):
		self.input_nodes = input_nodes
	
	@classmethod
	def from_spec_dict(cls, spec_dict: Dict):
		""" Alternative constructor. Creates an InputStep from a simulation
		specification dict. Class method.
		
		Args:
		
		Returns:
			An InputStep object.

		TODO Implement this method.
		"""
		raise NotImplementedError
	
	def __call__(
		self,
		input_file_map: Dict[str, str] = None,
	) -> ValuesDict:
		""" Run input step and return ValuesDict to be passed to simulation
		steps.
		
		Args:
			input_file_map (default None, otherwise Dict[str, str]): A dict
				where the keys are the aliases of input files and the values
				are the paths to the files. Only used when input nodes do not
				specify their input file paths in the specification file and
				instead use aliases to refer to the files. In this case, the
				specification file should have a key called "input_file_map"
				whose value is this dict.
		
		Returns:
			A ValuesDict object containing the values from the input nodes.
		"""
		vals_dict = {}
		for node in self.input_nodes:
			vals_dict[node.alias] = node.load_vals(input_file_map)
		return vals_dict
	

class SimulationStep:
	""" Each simulation step contains and runs a single function node.
	
	Performs the following steps:
		1. Gets the input values from the ValuesDict.
		2. Runs the function node on the input values.
		3. Adds the output values to the ValuesDict under the alias of the
			function node.
		4. Output filtering (NOT IMPLEMENTED, may not be necessary).
		5. Returns the ValuesDict.

	Attributes:
		function_node: The function node that will be ran by this step.
		required_output: Default None. If None, output of function node
			will be added to ValuesDict under the alias of the function node.
			and the whole dict will be returned. If is instead a list of
			strings, only the values with the specified aliases will be
			returned.
	"""